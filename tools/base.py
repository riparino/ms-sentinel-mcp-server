"""
Base classes and interfaces for MCP tools.

Defines MCPToolBase, the abstract base class for all MCP server tools. 
Provides standard output wrapping, logging, error handling,
and context extraction utilities. 
All custom MCP tools should inherit from MCPToolBase.
"""

import os
import logging  # For type hinting of logger attribute
import warnings
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import Context
from utilities.api_utils import AzureApiClient
from utilities.task_manager import run_in_thread
from utilities.logging import get_tool_logger


class MCPToolBase(ABC):
    """
    Abstract base class for all MCP tools.

    Provides standard output wrapping, logging,
    error handling, and context extraction utilities.
    Tool authors should subclass this and implement the core logic in `run`.

    IMPORTANT:
    All Azure SDK client initialization (LogsQueryClient, SecurityInsights, etc.)
    MUST be performed via the provided methods in this class:
      - get_logs_client_and_workspace
      - get_loganalytics_client
      - get_securityinsight_client
    Tool implementations must NOT import or initialize Azure SDK clients directly.
    This enforces maintainability, security, and testability.

    Azure SDK for Python emits a warning when deserializing
    datetime objects with no timezone (tzinfo):
        'Datetime with no tzinfo will be considered UTC.'
    This is safe to suppress for all MCP tools, as Azure datetimes
    are UTC by default and the SDK's behavior is correct.
    We suppress this warning here globally to avoid log noise,
    following project best practices.
    """

    name: str = ""
    description: str = ""
    logger: logging.Logger = None

    def __init__(self):
        """
        Initialize the MCPToolBase instance and set up the logger.
        Also suppress Azure SDK tzinfo warnings globally for all MCP tools.
        """
        # Suppress Azure SDK tzinfo warning (see class docstring)
        warnings.filterwarnings(
            "ignore",
            message="Datetime with no tzinfo will be considered UTC.",
            module="azure.core.serialization",
        )
        if not self.logger:
            self.logger = get_tool_logger(self.__class__.__name__)

    def get_logs_client_and_workspace(self, ctx: Context):
        """
        Get a LogsQueryClient and workspace ID for querying Log Analytics tables.

        Supports both server (MCP) and direct invocation (integration tests).

        Args:
            ctx (Context): The MCP context object.
        Returns:
            tuple: (logs_client, workspace_id)
        Raises:
            ImportError: If Azure SDK is not installed.
        """
        try:
            # pylint: disable=import-outside-toplevel
            # ruff: noqa: C0415
            from azure.identity import DefaultAzureCredential
            from azure.monitor.query import LogsQueryClient
        except ImportError as e:
            raise ImportError(
                "Azure SDK is required for Log Analytics operations."
            ) from e
        # Server (MCP) invocation
        if (
            hasattr(ctx, "request_context")
            and getattr(ctx, "request_context", None) is not None
        ):
            services_ctx = ctx.request_context.lifespan_context
            logs_client = getattr(services_ctx, "logs_client", None)
            workspace_id = getattr(services_ctx, "workspace_id", None)
            return logs_client, workspace_id
        # Direct invocation (integration tests)
        workspace_id = os.environ["AZURE_WORKSPACE_ID"]
        # Use DefaultAzureCredential for all environments
        credential = DefaultAzureCredential()
        logs_client = LogsQueryClient(credential)
        return logs_client, workspace_id

    def get_azure_context(self, ctx: Context):
        """
        Get Azure workspace name, resource group, and subscription ID.

        Returns values from environment variables or, if not set, from the context object.

        Args:
            ctx (Context): The MCP context object.
        Returns:
            tuple: (workspace_name, resource_group, subscription_id)
        """
        workspace_name = os.getenv("AZURE_WORKSPACE_NAME") or getattr(
            ctx, "workspace_name", None
        )
        resource_group = os.getenv("AZURE_RESOURCE_GROUP") or getattr(
            ctx, "resource_group", None
        )
        subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID") or getattr(
            ctx, "subscription_id", None
        )
        return workspace_name, resource_group, subscription_id

    def get_loganalytics_client(self, subscription_id):
        """
        Get an authenticated LogAnalyticsManagementClient for the given subscription ID.

        Args:
            subscription_id (str): Azure subscription ID.
        Returns:
            LogAnalyticsManagementClient: Authenticated client instance.
        """
        # pylint: disable=import-outside-toplevel
        # ruff: noqa: C0415
        from azure.identity import DefaultAzureCredential
        from azure.mgmt.loganalytics import LogAnalyticsManagementClient

        # pylint: disable=import-outside-toplevel
        credential = DefaultAzureCredential()
        return LogAnalyticsManagementClient(credential, subscription_id)

    def get_securityinsight_client(self, subscription_id):
        """
        Get an authenticated SecurityInsights client for the given subscription ID.

        Args:
            subscription_id (str): Azure subscription ID.
        Returns:
            SecurityInsights: Authenticated client instance.
        """
        # pylint: disable=import-outside-toplevel
        # ruff: noqa: C0415
        from azure.identity import DefaultAzureCredential
        from azure.mgmt.securityinsight import SecurityInsights

        # pylint: disable=import-outside-toplevel
        credential = DefaultAzureCredential()
        return SecurityInsights(credential, subscription_id)

    def get_authorization_client(self, subscription_id):
        """
        Get an authenticated AuthorizationManagementClient for the given subscription ID.

        Args:
            subscription_id (str): Azure subscription ID.
        Returns:
            AuthorizationManagementClient: Authenticated client instance.
        """
        try:
            # pylint: disable=import-outside-toplevel
            # ruff: noqa: C0415
            from azure.identity import DefaultAzureCredential
            from azure.mgmt.authorization import AuthorizationManagementClient
        except ImportError as e:
            raise ImportError(
                "Azure SDK is required for AuthorizationManagementClient operations."
            ) from e
        credential = DefaultAzureCredential()
        return AuthorizationManagementClient(credential, subscription_id)

    def get_api_client(self, ctx: Context):
        """
        Get an AzureApiClient for making direct REST API calls to Azure services.

        Reuses the credential from the context if available, otherwise creates a new one.

        Args:
            ctx (Context): The MCP context object.
        Returns:
            AzureApiClient: Authenticated API client.
        """
        credential = None

        # Try to get credential from context first
        if hasattr(ctx, "request_context") and ctx.request_context:
            credential = ctx.request_context.lifespan_context.credential

        # If no credential in context, create a new one
        if not credential:
            # pylint: disable=import-outside-toplevel
            # ruff: noqa: C0415
            from azure.identity import DefaultAzureCredential

            credential = DefaultAzureCredential()

        # Create and return the API client
        return AzureApiClient(credential)

    async def call_api(
        self,
        ctx: Context,
        method: str,
        url: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        body: Optional[dict] = None,
        timeout: Optional[float] = 30.0,
        name: Optional[str] = None,
    ):
        """
        Make a direct REST API call using AzureApiClient and task_manager.

        Args:
            ctx (Context): The MCP context.
            method (str): HTTP method (GET, POST, etc.).
            url (str): The full URL for the API call.
            params (dict, optional): Query parameters.
            headers (dict, optional): HTTP headers.
            body (dict, optional): Request body (for POST/PUT/PATCH).
            timeout (float, optional): Timeout in seconds (default: 30).
            name (str, optional): Name for the task for debugging.
        Returns:
            Any: The first page of results from the API call.
        Raises:
            StopIteration: If no results are returned.
            Exception: Any exception raised by the API call.
        """
        # Get the API client
        api_client = self.get_api_client(ctx)

        # Define a function to make the API call and get the first page
        def make_api_call():
            # The call_azure_rest_api method returns a generator
            generator = api_client.call_azure_rest_api(
                method, url, params=params, headers=headers, body=body
            )
            # Get the first page of results
            return next(generator)

        # Run the API call in a thread with the task manager
        task_name = name or f"api_call_{method}_{url.split('/')[-1]}"
        return await run_in_thread(make_api_call, timeout=timeout, name=task_name)

    def validate_azure_context(
        self,
        sdk_available,
        workspace_name,
        resource_group,
        subscription_id,
        logger=None,
    ):
        """
        Check if all required Azure context is present and SDK is available.

        Logs a warning and returns False if not valid, otherwise returns True.

        Args:
            sdk_available (bool): Whether the Azure SDK is available.
            workspace_name (str): Azure workspace name.
            resource_group (str): Azure resource group.
            subscription_id (str): Azure subscription ID.
            logger (logging.Logger, optional): Logger for warnings.
        Returns:
            bool: True if all required context is present, False otherwise.
        """
        if not (
            sdk_available and workspace_name and resource_group and subscription_id
        ):
            if logger:
                logger.warning(
                    "Missing Azure SDK or workspace details; returning minimal info."
                )
            return False
        return True

    def _extract_param(self, kwargs, name, default=None):
        """
        Extract a parameter value from kwargs, supporting both direct and nested patterns.

        This function will look for the parameter 'name' in kwargs. If not found, it will also
        look for 'name' in a nested 'kwargs' dictionary inside kwargs. If the parameter is not
        found in either, the provided default is returned.

        Args:
            kwargs (dict): The keyword arguments dictionary.
            name (str): The parameter name to extract.
            default (Any, optional): The default value to return if not found. Defaults to None.

        Returns:
            Any: The value of the parameter, or the default if not found.
        """
        value = kwargs.get(name, None)
        if value is None and "kwargs" in kwargs:
            nested_kwargs = kwargs["kwargs"]
            # Handle the case when nested_kwargs is a string
            if isinstance(nested_kwargs, dict):
                value = nested_kwargs.get(name, default)
            else:
                # If it's not a dict, we can't extract parameters from it
                self.logger.warning(
                    "kwargs['kwargs'] is not a dictionary: %s", type(nested_kwargs)
                )
        return value if value is not None else default

    @abstractmethod
    async def run(self, ctx: Context, **kwargs) -> Any:
        """
        Execute the main tool logic. Should be implemented by subclasses.

        Args:
            ctx (Context): MCP Context object.
            **kwargs: Tool-specific arguments.
        Returns:
            Any: Serializable Python object (dict, list, str, etc.).
        """

    def wrap_result(self, result: Any) -> List[Dict[str, Any]]:
        """
        Wrap the tool result in an MCP-compliant content list.

        - If already a list of content objects, returns as-is.
        - If already MCP-compliant output (has 'valid' and 'results'), returns [result] directly.
        - If dict/list, wraps as JSON content.
        - Otherwise, wraps as text content.

        Args:
            result (Any): The result to wrap.
        Returns:
            List[Dict[str, Any]]: MCP-compliant content list.
        """
        if isinstance(result, list) and all(
            isinstance(x, dict) and "type" in x for x in result
        ):
            return result
        # If already MCP-compliant output, do not wrap
        if isinstance(result, dict) and "valid" in result and "results" in result:
            return [result]
        if isinstance(result, (dict, list)):
            return [{"type": "json", "json": result}]
        return [{"type": "text", "text": str(result)}]

    async def __call__(self, ctx: Context, **kwargs) -> Dict[str, Any]:
        """
        Entrypoint for MCP tool execution.

        Handles logging, error handling, and output wrapping.
        Returns MCP-compliant result dict with content and isError.

        Args:
            ctx (Context): MCP context object.
            **kwargs: Tool-specific arguments.
        Returns:
            Dict[str, Any]: MCP-compliant result dict.
        """
        self.logger.info("Running tool: %s", self.name)
        try:
            result = await self.run(ctx, **kwargs)
            content = self.wrap_result(result)
            return {"content": content, "isError": False}
        except Exception as e:
            self.logger.exception("Error in tool '%s': %s", self.name, e)
            return {
                "content": [{"type": "text", "text": f"Error: {str(e)}"}],
                "isError": True,
            }

    @classmethod
    def register(cls, mcp):
        """
        Register the tool with the MCP server.

        Subclasses should override the name and description attributes.

        Args:
            mcp: MCP server object.
        """
        instance = cls()

        @mcp.tool(instance.name, instance.description)
        async def tool_entrypoint(ctx: Context, **kwargs):
            return await instance(ctx, **kwargs)
