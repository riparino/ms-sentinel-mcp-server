"""
Log Analytics Saved Searches management tools.

This module provides tools for listing and retrieving saved searches in Azure Log Analytics
workspaces.
"""

from mcp.server.fastmcp import Context, FastMCP

from tools.base import MCPToolBase
from utilities.task_manager import run_in_thread


class LogAnalyticsSavedSearchesListTool(MCPToolBase):
    """
    Tool to list all saved searches in a Log Analytics workspace.
    """

    name = "log_analytics_saved_searches_list"
    description = "List all saved searches in a Log Analytics workspace"

    async def run(self, ctx: Context, **kwargs):
        """
        List all saved searches in the specified Log Analytics workspace.

        Args:
            ctx (Context): The FastMCP context containing authentication and request information.
            **kwargs: Additional keyword arguments (unused).

        Returns:
            dict: Dictionary containing the list of saved searches, count, and validity flag.
        """
        # Get Azure context
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)

        # Validate Azure context
        sdk_available = True
        try:
            # Just check if the module is available
            import importlib.util  # pylint: disable=import-outside-toplevel

            sdk_available = (
                importlib.util.find_spec("azure.mgmt.loganalytics") is not None
            )
        except ImportError:
            sdk_available = False

        if not self.validate_azure_context(
            sdk_available, workspace_name, resource_group, subscription_id, self.logger
        ):
            return {"error": "Missing Azure SDK or workspace details."}

        # Get Log Analytics client
        client = None
        try:
            client = self.get_loganalytics_client(subscription_id)
        except Exception as e:
            self.logger.error("Error initializing Azure LogAnalytics client: %s", e)
            return {"error": "Azure LogAnalytics client initialization failed: %s" % e}

        if client is None:
            return {"error": "Azure LogAnalytics client is not initialized"}

        try:
            # List all saved searches in the workspace
            saved_searches_result = await run_in_thread(
                client.saved_searches.list_by_workspace,
                resource_group_name=resource_group,
                workspace_name=workspace_name,
            )

            # Log the result to understand its structure
            self.logger.info(
                "Saved searches result type: %s", type(saved_searches_result)
            )

            result = []
            # Check if the result has a 'value' attribute which is the actual list
            if hasattr(saved_searches_result, "value"):
                saved_searches = saved_searches_result.value
            else:
                # If not, try to access it as a dictionary
                saved_searches = getattr(saved_searches_result, "saved_searches", [])

            self.logger.info(
                "Processing %s saved searches",
                len(saved_searches) if saved_searches else 0,
            )

            for search in saved_searches:
                # Create a basic info dictionary with guaranteed attributes
                search_info = {
                    "id": search.id if hasattr(search, "id") else None,
                    "name": search.name if hasattr(search, "name") else None,
                    "type": search.type if hasattr(search, "type") else None,
                }

                # Try to access properties directly from the search object first
                try:
                    # Check for direct properties on the search object
                    properties_to_check = [
                        "category",
                        "display_name",
                        "query",
                        "function_alias",
                        "function_parameters",
                        "version",
                        "tags",
                        "etag",
                        "time_created",
                        "time_modified",
                    ]

                    for prop_name in properties_to_check:
                        if hasattr(search, prop_name):
                            value = getattr(search, prop_name)
                            if value is not None:
                                # Convert snake_case to camelCase for consistency in the output
                                key = "".join(
                                    [
                                        x.capitalize() if i > 0 else x
                                        for i, x in enumerate(prop_name.split("_"))
                                    ]
                                )
                                search_info[key] = value

                    # If we couldn't find any direct properties, try the nested properties approach
                    if len(search_info) <= 3 and hasattr(search, "properties"):
                        props = search.properties
                        if hasattr(props, "category"):
                            search_info["category"] = props.category
                        if hasattr(props, "display_name"):
                            search_info["displayName"] = props.display_name
                        if hasattr(props, "query"):
                            search_info["query"] = props.query
                        if hasattr(props, "function_alias"):
                            search_info["functionAlias"] = props.function_alias
                        if hasattr(props, "version"):
                            search_info["version"] = props.version
                        if hasattr(props, "tags"):
                            search_info["tags"] = props.tags
                        if hasattr(props, "etag"):
                            search_info["etag"] = props.etag
                except Exception as prop_error:
                    # Log the property access error but continue with basic details
                    self.logger.error(
                        "Error accessing saved search properties: %s", prop_error
                    )

                result.append(search_info)

            return {"savedSearches": result, "count": len(result), "valid": True}
        except Exception as e:
            self.logger.error("Error retrieving saved searches: %s", e)
            return {"error": "Error retrieving saved searches: %s" % str(e)}


class LogAnalyticsSavedSearchGetTool(MCPToolBase):
    """
    Tool to retrieve a specific saved search from a Log Analytics workspace.
    """

    name = "log_analytics_saved_search_get"
    description = "Get a specific saved search from a Log Analytics workspace"

    async def run(self, ctx: Context, **kwargs):
        """
        Retrieve a specific saved search by ID from the specified Log Analytics workspace.

        Args:
            ctx (Context): The FastMCP context containing authentication and request information.
            **kwargs: Keyword arguments containing 'saved_search_id'.

        Returns:
            dict: Dictionary containing the saved search details and validity flag, or
            error information.
        """
        # Extract saved_search_id parameter using the
        # centralized parameter extraction from MCPToolBase
        saved_search_id = self._extract_param(kwargs, "saved_search_id")

        if not saved_search_id:
            return {"error": "saved_search_id parameter is required"}

        # Get Azure context
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)

        # Validate Azure context
        sdk_available = True
        try:
            # Just check if the module is available
            import importlib.util  # pylint: disable=import-outside-toplevel

            sdk_available = (
                importlib.util.find_spec("azure.mgmt.loganalytics") is not None
            )
        except ImportError:
            sdk_available = False

        if not self.validate_azure_context(
            sdk_available, workspace_name, resource_group, subscription_id, self.logger
        ):
            return {"error": "Missing Azure SDK or workspace details."}

        # Get Log Analytics client
        client = None
        try:
            client = self.get_loganalytics_client(subscription_id)
        except Exception as e:
            self.logger.error("Error initializing Azure LogAnalytics client: %s", e)
            return {
                "error": "Azure LogAnalytics client initialization failed: %s" % str(e)
            }

        if client is None:
            return {"error": "Azure LogAnalytics client is not initialized"}

        try:
            # Get the specific saved search
            search = await run_in_thread(
                client.saved_searches.get,
                resource_group_name=resource_group,
                workspace_name=workspace_name,
                saved_search_id=saved_search_id,
            )

            # Log the search object to understand its structure
            self.logger.debug("Saved search object: %s", search)

            # Create a detailed info dictionary with all available attributes
            search_details = {
                "id": search.id if hasattr(search, "id") else None,
                "name": search.name if hasattr(search, "name") else None,
                "type": search.type if hasattr(search, "type") else None,
            }

            # Based on the log output, the properties are directly accessible
            # as attributes of the search object, not nested under properties
            properties_to_check = [
                "category",
                "display_name",
                "query",
                "function_alias",
                "function_parameters",
                "version",
                "tags",
                "etag",
                "time_created",
                "time_modified",
            ]

            # Check for each property and add it if it exists
            for prop_name in properties_to_check:
                if hasattr(search, prop_name):
                    value = getattr(search, prop_name)
                    if value is not None:
                        # Convert snake_case to camelCase for consistency in the output
                        key = "".join(
                            [
                                x.capitalize() if i > 0 else x
                                for i, x in enumerate(prop_name.split("_"))
                            ]
                        )
                        search_details[key] = value

            # Check for additional_properties if they exist
            if (
                hasattr(search, "additional_properties")
                and search.additional_properties
            ):
                for key, value in search.additional_properties.items():
                    if value is not None and key not in search_details:
                        search_details[key] = value

            return {"savedSearch": search_details, "valid": True}
        except Exception as e:
            self.logger.error(
                "Error retrieving saved search with ID %s: %s", saved_search_id, e
            )
            return {
                "error": "Error retrieving saved search ID %s: %s"
                % (saved_search_id, str(e))
            }


def register_tools(mcp: FastMCP):
    """
    Register Log Analytics saved search tools with the MCP server.

    Args:
        mcp (FastMCP): The FastMCP server instance to register tools with.
    """
    LogAnalyticsSavedSearchesListTool.register(mcp)
    LogAnalyticsSavedSearchGetTool.register(mcp)
