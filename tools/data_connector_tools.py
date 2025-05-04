"""
MCPToolBase-compliant tools for managing Sentinel data connectors in the MCP server.

This module provides tools for listing and retrieving Azure Sentinel data connectors. 
Tools are compatible with both MCP server context and direct invocation for integration testing.
"""

from mcp.server.fastmcp import Context
from tools.base import MCPToolBase


class SentinelConnectorsListTool(MCPToolBase):
    """
    MCP tool for listing Sentinel data connectors.

    This tool supports both MCP server context (using ctx.request_context) and
    direct invocation for integration tests.
    If ctx.request_context is not present, Azure credentials and context are
    loaded from environment variables, as required by project architecture guidelines.
    """

    name = "sentinel_connectors_list"
    description = "List data connectors"

    async def run(self, ctx: Context, **kwargs):
        """List available Sentinel data connectors in the workspace.

        Args:
            ctx (Context): The MCP server or test context.
            **kwargs: Additional keyword arguments (unused).
        Returns:
            dict: Result containing connector list or error information.
        """
        logger = self.logger
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)
        if not (workspace_name and resource_group and subscription_id):
            logger.error("Missing Azure context for listing data connectors.")
            return {"error": "Missing Azure context for listing data connectors."}
        try:
            client = self.get_securityinsight_client(subscription_id)
            connectors = client.data_connectors.list(
                resource_group_name=resource_group,
                workspace_name=workspace_name,
            )
            connector_list = list(connectors)
            result = []
            for c in connector_list:
                connector_type = getattr(c, "kind", "Unknown")
                result.append(
                    {
                        "name": getattr(c, "name", None),
                        "kind": connector_type,
                        "id": getattr(c, "id", None),
                        "etag": getattr(c, "etag", None),
                        "type": getattr(c, "type", None),
                    }
                )
            return {
                "count": len(result),
                "connectors": result,
                "note": (
                    "⚠️ Connector list may be incomplete. Built-in and gallery-deployed "
                    "connectors are not included due to Azure API limitations. "
                    "Manual verification recommended."
                ),
            }
        except Exception as e:
            logger.error("Error listing data connectors: %s", e)
            return {"error": "Error listing data connectors: %s" % str(e)}


class SentinelConnectorsGetTool(MCPToolBase):
    """
    MCP tool for retrieving a specific Sentinel data connector by ID.

    This tool supports both MCP server context (using ctx.request_context)
    and direct invocation for integration tests.
    If ctx.request_context is not present, Azure credentials and context are
    loaded from environment variables, as required by project architecture guidelines.
    """

    name = "sentinel_connectors_get"
    description = "Get a specific data connector by ID"

    async def run(self, ctx: Context, **kwargs):
        """Retrieve a specific Sentinel data connector by its ID.

        Args:
            ctx (Context): The MCP server or test context.
            **kwargs: Keyword arguments containing 'data_connector_id'.
        Returns:
            dict: Connector details or error information.
        """
        logger = self.logger
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)
        if not (workspace_name and resource_group and subscription_id):
            logger.error("Missing Azure context for getting data connector.")
            return {"error": "Missing Azure context for getting data connector."}
        data_connector_id = self._extract_param(kwargs, "data_connector_id")
        if not data_connector_id:
            logger.error("Missing required parameter: data_connector_id")
            return {"error": "Missing required parameter: data_connector_id"}
        try:
            client = self.get_securityinsight_client(subscription_id)
            connector = client.data_connectors.get(
                resource_group_name=resource_group,
                workspace_name=workspace_name,
                data_connector_id=data_connector_id,
            )
            return {
                "name": getattr(connector, "name", None),
                "type": getattr(connector, "type", None),
                "kind": getattr(connector, "kind", None),
                "id": getattr(connector, "id", None),
                "etag": getattr(connector, "etag", None),
                "properties": getattr(connector, "properties", None),
            }
        except Exception as e:
            logger.error("Error getting data connector: %s", e)
            return {"error": "Error getting data connector: %s" % str(e)}


def register_tools(mcp):
    """Register all data connector tools with the MCP server.

    Args:
        mcp: The MCP server instance.
    """
    SentinelConnectorsListTool.register(mcp)
    SentinelConnectorsGetTool.register(mcp)
