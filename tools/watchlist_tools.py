"""
Microsoft Sentinel Watchlist tools using the SecurityInsight SDK.

This module provides tools for listing and retrieving Sentinel watchlists and watchlist
items. All tools are implemented as MCPToolBase subclasses for integration with the MCP
server.
"""

# NOTE: Azure client initialization for all MCP tools is centralized in MCPToolBase (tools/base.py).
# All tools must use self.get_securityinsight_client, self.get_logs_client_and_workspace, etc.,
# instead of duplicating credential/client logic.

from mcp.server.fastmcp import Context, FastMCP
from tools.base import MCPToolBase
from utilities.task_manager import run_in_thread


class SentinelWatchlistsListTool(MCPToolBase):
    """
    Tool for listing all Microsoft Sentinel watchlists in the configured workspace.
    """

    name = "sentinel_watchlists_list"
    description = "List all Sentinel watchlists"

    async def run(self, ctx: Context, **kwargs):
        logger = self.logger

        # Get Azure context and SecurityInsights client using MCPToolBase methods
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)
        try:
            client = self.get_securityinsight_client(subscription_id)
        except Exception as e:
            logger.error("Error initializing Azure SecurityInsights client: %s", e)
            return {
                "error": (
                    "Azure SecurityInsights client initialization failed: %s" % str(e)
                )
            }
        if client is None:
            return {"error": "Azure SecurityInsights client is not initialized"}

        try:
            # List all watchlists
            watchlists = await run_in_thread(
                client.watchlists.list,
                resource_group_name=resource_group,
                workspace_name=workspace_name,
            )

            result = []
            for watchlist in watchlists:
                # Log the watchlist object to understand its structure
                logger.debug("Watchlist object: %s", watchlist)

                # Create a basic info dictionary with guaranteed attributes
                watchlist_info = {
                    "id": watchlist.id if hasattr(watchlist, "id") else None,
                    "name": watchlist.name if hasattr(watchlist, "name") else None,
                }

                # Add properties if they exist
                if hasattr(watchlist, "properties"):
                    props = watchlist.properties
                    if hasattr(props, "watchlist_alias"):
                        watchlist_info["alias"] = props.watchlist_alias
                    if hasattr(props, "display_name"):
                        watchlist_info["displayName"] = props.display_name
                    if hasattr(props, "description"):
                        watchlist_info["description"] = props.description
                    if hasattr(props, "provider"):
                        watchlist_info["provider"] = props.provider
                    if hasattr(props, "source"):
                        watchlist_info["source"] = props.source
                    if hasattr(props, "items_search_key"):
                        watchlist_info["itemsSearchKey"] = props.items_search_key
                    if hasattr(props, "created_time_utc"):
                        watchlist_info["created"] = props.created_time_utc
                    if hasattr(props, "updated_time_utc"):
                        watchlist_info["updated"] = props.updated_time_utc
                    if hasattr(props, "items_count"):
                        watchlist_info["itemsCount"] = props.items_count
                result.append(watchlist_info)

            return {"watchlists": result, "count": len(result), "valid": True}
        except Exception as e:
            logger.error("Error retrieving watchlists: %s", e)
            return {"error": f"Error retrieving watchlists: {str(e)}"}


class SentinelWatchlistGetTool(MCPToolBase):
    """
    Tool for retrieving a specific Microsoft Sentinel watchlist by alias.
    """

    name = "sentinel_watchlist_get"
    description = "Get a specific Sentinel watchlist"

    async def run(self, ctx: Context, **kwargs):
        logger = self.logger

        # Extract parameters using the centralized parameter extraction from MCPToolBase
        watchlist_alias = self._extract_param(kwargs, "watchlist_alias")
        if not watchlist_alias:
            return {"error": "watchlist_alias parameter is required"}

        # Get Azure context
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)

        # Get security insights client
        client = None
        try:
            client = self.get_securityinsight_client(subscription_id)
        except Exception as e:
            logger.error("Error initializing Azure SecurityInsights client: %s", e)
            return {
                "error": (
                    "Azure SecurityInsights client initialization failed: %s" % str(e)
                )
            }

        if client is None:
            return {"error": "Azure SecurityInsights client is not initialized"}

        try:
            # Get the specific watchlist
            watchlist = await run_in_thread(
                client.watchlists.get,
                resource_group_name=resource_group,
                workspace_name=workspace_name,
                watchlist_alias=watchlist_alias,
            )

            # Log the watchlist object to understand its structure
            logger.debug("Watchlist object: %s", watchlist)

            # Create a basic info dictionary with guaranteed attributes
            watchlist_details = {
                "id": watchlist.id if hasattr(watchlist, "id") else None,
                "name": watchlist.name if hasattr(watchlist, "name") else None,
            }

            # Try to access properties directly from the watchlist object first
            try:
                # Check for direct properties on the watchlist object
                if hasattr(watchlist, "watchlist_alias"):
                    watchlist_details["alias"] = watchlist.watchlist_alias
                if hasattr(watchlist, "display_name"):
                    watchlist_details["displayName"] = watchlist.display_name
                if hasattr(watchlist, "description"):
                    watchlist_details["description"] = watchlist.description
                if hasattr(watchlist, "provider"):
                    watchlist_details["provider"] = watchlist.provider
                if hasattr(watchlist, "source"):
                    watchlist_details["source"] = watchlist.source
                if hasattr(watchlist, "items_search_key"):
                    watchlist_details["itemsSearchKey"] = watchlist.items_search_key
                if hasattr(watchlist, "created_time_utc"):
                    watchlist_details["created"] = watchlist.created_time_utc
                if hasattr(watchlist, "updated_time_utc"):
                    watchlist_details["updated"] = watchlist.updated_time_utc
                if hasattr(watchlist, "items_count"):
                    watchlist_details["itemsCount"] = watchlist.items_count

                # If we couldn't find any direct properties, try the nested properties approach
                if len(watchlist_details) <= 2 and hasattr(watchlist, "properties"):
                    props = watchlist.properties
                    if hasattr(props, "watchlist_alias"):
                        watchlist_details["alias"] = props.watchlist_alias
                    if hasattr(props, "display_name"):
                        watchlist_details["displayName"] = props.display_name
                    if hasattr(props, "description"):
                        watchlist_details["description"] = props.description
                    if hasattr(props, "provider"):
                        watchlist_details["provider"] = props.provider
                    if hasattr(props, "source"):
                        watchlist_details["source"] = props.source
                    if hasattr(props, "items_search_key"):
                        watchlist_details["itemsSearchKey"] = props.items_search_key
                    if hasattr(props, "created_time_utc"):
                        watchlist_details["created"] = props.created_time_utc
                    if hasattr(props, "updated_time_utc"):
                        watchlist_details["updated"] = props.updated_time_utc
                    if hasattr(props, "items_count"):
                        watchlist_details["itemsCount"] = props.items_count
            except Exception as prop_error:
                # Log the property access error but continue with basic details
                logger.error("Error accessing watchlist properties: %s", prop_error)

            return {"watchlist": watchlist_details, "valid": True}
        except Exception as e:
            logger.error(
                "Error retrieving watchlist details for alias %s: %s",
                watchlist_alias,
                e,
            )
            return {
                "error": "Error retrieving watchlist details for alias %s: %s"
                % (watchlist_alias, e)
            }


class SentinelWatchlistItemsListTool(MCPToolBase):
    """
    Tool for listing all items in a specified Microsoft Sentinel watchlist.
    """

    name = "sentinel_watchlist_items_list"
    description = "List all items in a Sentinel watchlist"

    async def run(self, ctx: Context, **kwargs):
        logger = self.logger

        # Extract parameters using the base class method
        watchlist_alias = self._extract_param(kwargs, "watchlist_alias")
        if not watchlist_alias:
            return {"error": "watchlist_alias parameter is required"}

        # Get Azure context
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)

        # Get security insights client
        client = None
        try:
            client = self.get_securityinsight_client(subscription_id)
        except Exception as e:
            logger.error("Error initializing Azure SecurityInsights client: %s", e)
            return {
                "error": (
                    "Azure SecurityInsights client initialization failed: %s" % str(e)
                )
            }

        if client is None:
            return {"error": "Azure SecurityInsights client is not initialized"}

        try:
            # List all items in the watchlist
            watchlist_items = await run_in_thread(
                client.watchlist_items.list,
                resource_group_name=resource_group,
                workspace_name=workspace_name,
                watchlist_alias=watchlist_alias,
            )

            result = []
            for item in watchlist_items:
                # Log the item object to understand its structure
                logger.debug("Watchlist item object: %s", item)

                # Create a basic info dictionary with guaranteed attributes
                item_info = {
                    "id": item.id if hasattr(item, "id") else None,
                    "name": item.name if hasattr(item, "name") else None,
                }

                # Try to access properties directly from the item object first
                try:
                    # Check for direct properties on the item object
                    if hasattr(item, "items_key_value"):
                        item_info["itemsKeyValue"] = item.items_key_value
                    if hasattr(item, "properties") and isinstance(item.properties, dict):
                        item_info["properties"] = item.properties
                    
                    # If we couldn't find any direct properties, try the nested properties approach
                    if len(item_info) <= 2 and hasattr(item, "properties") and not isinstance(item.properties, dict):
                        props = item.properties
                        if hasattr(props, "items_key_value"):
                            item_info["itemsKeyValue"] = props.items_key_value
                        if hasattr(props, "properties"):
                            item_info["properties"] = props.properties
                except Exception as prop_error:
                    # Log the property access error but continue with basic details
                    logger.error("Error accessing watchlist item properties: %s", prop_error)

                result.append(item_info)

            return {
                "watchlistItems": result,
                "count": len(result),
                "watchlistAlias": watchlist_alias,
                "valid": True,
            }
        except Exception as e:
            logger.error(
                "Error retrieving watchlist items for alias %s: %s", watchlist_alias, e
            )
            return {
                "error": "Error retrieving watchlist items for alias %s: %s"
                % (watchlist_alias, e)
            }


class SentinelWatchlistItemGetTool(MCPToolBase):
    """
    Tool for retrieving a specific item from a Microsoft Sentinel watchlist by alias
    and item ID.
    """

    name = "sentinel_watchlist_item_get"
    description = "Get a specific item from a Sentinel watchlist"

    async def run(self, ctx: Context, **kwargs):
        logger = self.logger

        # Extract parameters using the base class method
        watchlist_alias = self._extract_param(kwargs, "watchlist_alias")
        watchlist_item_id = self._extract_param(kwargs, "watchlist_item_id")

        if not watchlist_alias:
            return {"error": "watchlist_alias parameter is required"}
        if not watchlist_item_id:
            return {"error": "watchlist_item_id parameter is required"}

        # Get Azure context and SecurityInsights client using MCPToolBase methods
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)
        try:
            client = self.get_securityinsight_client(subscription_id)
        except Exception as e:
            logger.error("Error initializing Azure SecurityInsights client: %s", e)
            return {
                "error": (
                    "Azure SecurityInsights client initialization failed: %s" % str(e)
                )
            }
        if client is None:
            return {"error": "Azure SecurityInsights client is not initialized"}

        try:
            # Get the specific watchlist item
            item = await run_in_thread(
                client.watchlist_items.get,
                resource_group_name=resource_group,
                workspace_name=workspace_name,
                watchlist_alias=watchlist_alias,
                watchlist_item_id=watchlist_item_id,
            )

            # Log the item object to understand its structure
            logger.debug("Watchlist item object: %s", item)

            # Create a basic info dictionary with guaranteed attributes
            item_details = {
                "id": item.id if hasattr(item, "id") else None,
                "name": item.name if hasattr(item, "name") else None,
                "watchlistAlias": watchlist_alias,
            }

            # Try to access properties directly from the item object first
            try:
                # Check for direct properties on the item object
                if hasattr(item, "items_key_value"):
                    item_details["itemsKeyValue"] = item.items_key_value
                if hasattr(item, "properties") and isinstance(item.properties, dict):
                    item_details["properties"] = item.properties
                
                # If we couldn't find any direct properties, try the nested properties approach
                if len(item_details) <= 3 and hasattr(item, "properties") and not isinstance(item.properties, dict):
                    props = item.properties
                    if hasattr(props, "items_key_value"):
                        item_details["itemsKeyValue"] = props.items_key_value
                    if hasattr(props, "properties"):
                        item_details["properties"] = props.properties
            except Exception as prop_error:
                # Log the property access error but continue with basic details
                logger.error("Error accessing watchlist item properties: %s", prop_error)

            return {"watchlistItem": item_details, "valid": True}
        except Exception as e:
            logger.error(
                "Error retrieving watchlist item for alias %s, item ID %s: %s",
                watchlist_alias,
                watchlist_item_id,
                e,
            )
            return {
                "error": "Error retrieving watchlist item for alias %s, item ID %s: %s"
                % (watchlist_alias, watchlist_item_id, e)
            }


def register_tools(mcp: FastMCP):
    """
    Register all Sentinel watchlist tools with the MCP server instance.

    Args:
        mcp (FastMCP): The MCP server instance to register tools with.
    """
    SentinelWatchlistsListTool.register(mcp)
    SentinelWatchlistGetTool.register(mcp)
    SentinelWatchlistItemsListTool.register(mcp)
    SentinelWatchlistItemGetTool.register(mcp)
