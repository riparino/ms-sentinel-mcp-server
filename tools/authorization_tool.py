"""
Authorization Tool for Microsoft Sentinel MCP Server

Provides the 'sentinel_authorization_summary' tool for retrieving and summarizing
Azure RBAC role assignments and permissions for the current identity, focusing on
Microsoft Sentinel and Log Analytics access.

Requirements:
- azure-identity
- azure-mgmt-authorization

Usage:
- This tool is registered via register_tools(mcp) and called through the MCP protocol.
- Supports both MCP server invocation and direct invocation for integration tests.

Direct Invocation Support:
- If ctx.request_context is not present, the tool will fall back to environment
  variables for Azure context and credentials.
- Required environment variables: AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET,
  AZURE_SUBSCRIPTION_ID, AZURE_RESOURCE_GROUP, AZURE_WORKSPACE_NAME, AZURE_WORKSPACE_ID.
- This fallback pattern is required for all MCP tools per project
  architecture guidelines.
"""

import re
from typing import Any, Dict

from azure.core.exceptions import (
    AzureError,
    ClientAuthenticationError,
    HttpResponseError,
)
from mcp.server.fastmcp import Context
from tools.base import MCPToolBase

READ_PATTERNS = [r"reader", r"read", r"monitor.*read"]
SENTINEL_READ_ROLES = {"Microsoft Sentinel Reader", "Security Reader"}
LOG_ANALYTICS_READ_ROLES = {"Log Analytics Reader", "Monitoring Reader"}


def _is_read_role(role_name: str, role_description: str) -> bool:
    """
    Detect if a role is a 'read' role by regex pattern matching.

    Args:
        role_name: The name of the Azure role
        role_description: The description of the Azure role

    Returns:
        bool: True if the role appears to be a read-only role based on pattern matching
    """
    for pattern in READ_PATTERNS:
        if re.search(pattern, role_name, re.IGNORECASE) or re.search(
            pattern, role_description, re.IGNORECASE
        ):
            return True
    return False


class SentinelAuthorizationSummaryTool(MCPToolBase):
    """
    Tool for retrieving and summarizing Azure RBAC role assignments for Microsoft
    Sentinel.

    This tool queries the Azure Authorization API to retrieve role assignments at
    various scopes (workspace, resource group, subscription) and analyzes them to
    determine the level of access the current identity has to Microsoft Sentinel
    and Log Analytics resources.
    """

    name = "sentinel_authorization_summary"
    description = (
        "Summarize Azure RBAC role assignments for Sentinel and Log Analytics access."
    )

    async def run(self, ctx: Context, **kwargs) -> Dict[str, Any]:
        """
        Execute the authorization summary tool.

        Retrieves Azure RBAC role assignments for the current identity and analyzes them
        to determine the level of access to Microsoft Sentinel and Log Analytics
        resources.

        Args:
            ctx: The MCP context object containing request context
            **kwargs: Additional parameters (unused but required for MCP compatibility)

        Returns:
            Dict[str, Any]: A dictionary containing:
                - workspace: Information about the Azure workspace
                - role_assignments: List of role assignments with details
                - permissions_assessment: Analysis of permissions
                - summary: Counts and statistics about the role assignments
        """
        logger = self.logger

        # Extract Azure context using MCPToolBase
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)
        # For workspace_id, try to get from context, else None
        workspace_id = getattr(
            getattr(getattr(ctx, "request_context", None), "lifespan_context", None),
            "workspace_id",
            None,
        )
        if not (subscription_id and resource_group and workspace_name and workspace_id):
            logger.error("Missing Azure context for authorization summary.")
            return {"error": "Missing Azure context."}

        # Initialize AuthorizationManagementClient using MCPToolBase
        try:
            client = self.get_authorization_client(subscription_id)
            scope_used = (
                f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}"
                f"/providers/Microsoft.OperationalInsights/workspaces/{workspace_name}"
            )
            rg_scope = (
                f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}"
                if subscription_id and resource_group
                else None
            )
            sub_scope = f"/subscriptions/{subscription_id}" if subscription_id else None
            workspace_scope = (
                scope_used
                if subscription_id and resource_group and workspace_name
                else None
            )
            scopes_to_try = [
                ("workspace", workspace_scope),
                ("resource_group", rg_scope),
                ("subscription", sub_scope),
            ]
            scopes_to_try = [(label, s) for label, s in scopes_to_try if s]
            if not subscription_id or not workspace_scope:
                logger.error(
                    "Missing Azure context: subscription_id or workspace_scope unavailable."
                )
                return {
                    "error": (
                        "Missing Azure context: subscription_id or workspace_scope unavailable."
                    ),
                    "workspace": {
                        "subscription_id": subscription_id,
                        "resource_group": resource_group,
                        "workspace_name": workspace_name,
                        "workspace_id": workspace_id,
                        "scope_used": None,
                        "scopes_tried": [s for _, s in scopes_to_try],
                    },
                    "role_assignments": [],
                    "permissions_assessment": {},
                    "summary": {"errors": ["Missing Azure context"]},
                }
        except Exception as e:
            logger.error("Failed to extract Azure context: %s", e)
            return {
                "error": "Failed to extract Azure context: %s" % type(e).__name__,
                "workspace": {},
                "role_assignments": [],
                "permissions_assessment": {},
                "summary": {"errors": [str(e)]},
            }

        assignments = None
        scope_used = None
        errors = []
        for label, scope in scopes_to_try:
            try:
                logger.info(
                    "Attempting to fetch role assignments at %s scope: %s", label, scope
                )
                result = list(client.role_assignments.list_for_scope(scope))
                if result:
                    assignments = result
                    scope_used = scope
                    logger.info(
                        "Found %d role assignments at %s scope: %s",
                        len(assignments),
                        label,
                        scope,
                    )
                    break
                else:
                    logger.info(
                        "No role assignments found at %s scope: %s", label, scope
                    )
            except Exception as e:
                logger.warning("Error at %s scope (%s): %s", label, scope, e)
                errors.append(
                    "%s scope (%s): %s: %s" % (label, scope, type(e).__name__, e)
                )
        if assignments is None:
            logger.error(
                "Failed to fetch role assignments at any scope. Errors: %s", errors
            )
            return {
                "error": "Failed to fetch role assignments at any scope.",
                "scopes_tried": [s for _, s in scopes_to_try],
                "details": errors,
            }

        results = []
        sentinel_read_count = 0
        log_analytics_read_count = 0
        read_scopes = set()

        for assignment in assignments:
            role_def_id = assignment.role_definition_id.split("/")[-1]
            try:
                role_def = client.role_definitions.get(scope_used, role_def_id)
                role_name = getattr(role_def, "role_name", "")
                description = getattr(role_def, "description", "")
                category = getattr(role_def, "role_type", "")
                assignment_scope = getattr(assignment, "scope", "")
                is_read = _is_read_role(role_name, description)
                is_sentinel_read = role_name in SENTINEL_READ_ROLES
                is_log_analytics_read = role_name in LOG_ANALYTICS_READ_ROLES
                if is_read or is_sentinel_read or is_log_analytics_read:
                    read_scopes.add(assignment_scope)
                if is_sentinel_read:
                    sentinel_read_count += 1
                if is_log_analytics_read:
                    log_analytics_read_count += 1
                results.append(
                    {
                        "role_assignment_id": assignment.id,
                        "principal_id": assignment.principal_id,
                        "scope": assignment_scope,
                        "role_definition_id": role_def_id,
                        "role_name": role_name,
                        "description": description,
                        "category": category,
                        "is_read": is_read,
                        "is_sentinel_read": is_sentinel_read,
                        "is_log_analytics_read": is_log_analytics_read,
                    }
                )
            except (ClientAuthenticationError, HttpResponseError, AzureError) as e:
                logger.warning(
                    "Azure error fetching role definition %s: %s", role_def_id, e
                )
                errors.append(
                    "Azure error fetching role definition %s: %s"
                    % (role_def_id, type(e).__name__)
                )
                continue
            except Exception as e:
                logger.warning(
                    "Unexpected error for role definition %s: %s", role_def_id, e
                )
                errors.append(
                    "Unexpected error for role definition %s: %s"
                    % (role_def_id, type(e).__name__)
                )
                continue

        output = {
            "workspace": {
                "subscription_id": subscription_id,
                "resource_group": resource_group,
                "workspace_name": workspace_name,
                "workspace_id": workspace_id,
                "scope_used": scope_used,
                "scopes_tried": [s for _, s in scopes_to_try],
            },
            "role_assignments": results,
            "permissions_assessment": {
                "has_sentinel_read": sentinel_read_count > 0,
                "has_log_analytics_read": log_analytics_read_count > 0,
                "read_scopes": list(read_scopes),
            },
            "summary": {
                "sentinel_read_roles": sentinel_read_count,
                "log_analytics_read_roles": log_analytics_read_count,
                "total_roles": len(results),
                "scopes_with_read_access": len(read_scopes),
                "errors": errors,
            },
        }
        logger.debug("Authorization summary: %s", output["summary"])
        return output


def register_tools(mcp) -> None:
    """Register all authorization tools with the MCP server.

    Args:
        mcp: The MCP server instance
    """
    SentinelAuthorizationSummaryTool.register(mcp)
