"""
Microsoft Entra ID (Azure AD) Tools for MCP Server.

This module provides MCP-compliant tools for listing and retrieving users and groups
from Microsoft Entra ID (Azure AD) using the Microsoft Graph API. All tools enforce
required Microsoft Graph permissions before execution and report missing permissions
in a client-readable way.

Tools implemented:
- EntraIDListUsersTool: List users
- EntraIDGetUserTool: Get user by UPN or object ID
- EntraIDListGroupsTool: List groups
- EntraIDGetGroupTool: Get group by object ID

Conforms to: docs/architecture/tool-architecture-and-implementation-requirements.md
Leverages: utilities/api_utils.py, utilities/cache.py, utilities/task_manager.py
"""

import logging

from mcp.server.fastmcp import Context
import requests
from tools.base import MCPToolBase
from utilities.graph_api_utils import (
    GraphApiClient,
    check_graph_permissions,
    GRAPH_API_BASE,
)
from utilities.task_manager import run_in_thread

logger = logging.getLogger(__name__)


class EntraIDToolBase(MCPToolBase):
    """
    Base class for Entra ID tools with permission checking.
    Uses utilities.graph_api_utils for Graph API access and permission checks.
    """

    def check_graph_permissions(self) -> None:
        """
        Checks if the current identity has required Microsoft Graph permissions using the utility.
        Raises:
            Exception: If required permissions are missing.
        """
        client = GraphApiClient()
        token = client.get_token()
        check_graph_permissions(token)


class EntraIDListUsersTool(EntraIDToolBase):
    """
    Tool to list users in Entra ID (Azure AD) via Microsoft Graph API.
    """

    name = "entra_id_list_users"
    description = "List users in Entra ID (Azure AD) via Microsoft Graph API."

    async def run(self, ctx: Context, **kwargs):
        self.check_graph_permissions()
        client = GraphApiClient()
        url = f"{GRAPH_API_BASE}/users"
        try:

            def fetch():
                users = []
                for page in client.call_azure_rest_api("GET", url):
                    users.extend(page.get("value", []))
                return users

            return await run_in_thread(fetch, name="entra_id_list_users")
        except requests.HTTPError as e:
            if e.response.status_code == 403:
                raise Exception("Permission denied: User.Read.All is required.") from e
            raise


class EntraIDGetUserTool(EntraIDToolBase):
    """
    Tool to get a user by object ID, UPN, or email address from Entra ID (Azure AD).
    Accepts any of: user_id, upn, or email.
    If user_id is not provided, resolves upn/email to user_id.
    """

    name = "entra_id_get_user"
    description = (
        "Get a user from Entra ID (Azure AD) by object ID, UPN, or email address."
    )

    async def run(self, ctx: Context, **kwargs):
        self.check_graph_permissions()
        client = GraphApiClient()
        user_id = self._extract_param(kwargs, "user_id")
        upn = self._extract_param(kwargs, "upn")
        email = self._extract_param(kwargs, "email")

        if not user_id:
            filter_str = None
            if upn:
                filter_str = f"userPrincipalName eq '{upn}'"
            elif email:
                filter_str = f"mail eq '{email}'"
            if filter_str:
                url = f"{GRAPH_API_BASE}/users?$filter={filter_str}"
                try:
                    # Use a unique name for this fetch to avoid duplicate function definition
                    def fetch_user_by_filter():
                        for page in client.call_azure_rest_api("GET", url):
                            users = page.get("value", [])
                            if users:
                                return users[0]
                            return None

                    user = await run_in_thread(
                        fetch_user_by_filter, name="entra_id_get_user_lookup"
                    )
                    if user and user.get("id"):
                        user_id = user["id"]
                    else:
                        logger.error("No user found for filter: %s", filter_str)
                        raise Exception(f"No user found for filter: {filter_str}")
                except requests.HTTPError as e:
                    logger.error("Graph API error during user lookup: %s", e)
                    if e.response.status_code == 403:
                        raise Exception(
                            "Permission denied: User.Read.All is required."
                        ) from e
                    raise
            else:
                logger.error("Missing required parameter: user_id, upn, or email")
                raise Exception("Missing required parameter: user_id, upn, or email")

        url = f"{GRAPH_API_BASE}/users/{user_id}"
        try:

            def fetch():
                for page in client.call_azure_rest_api("GET", url):
                    return page

            return await run_in_thread(fetch, name="entra_id_get_user")
        except requests.HTTPError as e:
            logger.error("Graph API error during user fetch: %s", e)
            if e.response.status_code == 403:
                raise Exception("Permission denied: User.Read.All is required.") from e
            raise


class EntraIDListGroupsTool(EntraIDToolBase):
    """
    Tool to list groups in Entra ID (Azure AD) via Microsoft Graph API.
    """

    name = "entra_id_list_groups"
    description = "List groups in Entra ID (Azure AD) via Microsoft Graph API."

    async def run(self, ctx: Context, **kwargs):
        self.check_graph_permissions()
        client = GraphApiClient()
        url = f"{GRAPH_API_BASE}/groups"
        try:

            def fetch():
                groups = []
                for page in client.call_azure_rest_api("GET", url):
                    groups.extend(page.get("value", []))
                return groups

            return await run_in_thread(fetch, name="entra_id_list_groups")
        except requests.HTTPError as e:
            if e.response.status_code == 403:
                raise Exception("Permission denied: Group.Read.All is required.") from e
            raise


class EntraIDGetGroupTool(EntraIDToolBase):
    """
    Tool to get a group by object ID from Entra ID (Azure AD).
    """

    name = "entra_id_get_group"
    description = "Get a group from Entra ID (Azure AD) by object ID."

    async def run(self, ctx: Context, **kwargs):
        self.check_graph_permissions()
        group_id = self._extract_param(kwargs, "group_id")
        if not group_id:
            raise Exception("Missing required parameter: group_id")
        client = GraphApiClient()
        url = f"{GRAPH_API_BASE}/groups/{group_id}"
        try:

            def fetch():
                for page in client.call_azure_rest_api("GET", url):
                    return page

            return await run_in_thread(fetch, name="entra_id_get_group")
        except requests.HTTPError as e:
            if e.response.status_code == 403:
                raise Exception("Permission denied: Group.Read.All is required.") from e
            raise


def register_tools(mcp):
    """
    Register all Entra ID tools with the MCP server instance.

    Args:
        mcp: The MCP server instance.
    """
    EntraIDListUsersTool.register(mcp)
    EntraIDGetUserTool.register(mcp)
    EntraIDListGroupsTool.register(mcp)
    EntraIDGetGroupTool.register(mcp)
