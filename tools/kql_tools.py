"""
FILE: tools/kql_tools.py

Provides KQL validation and query tools for the MCP server.

This module defines tools for validating KQL (Kusto Query Language) syntax 
in the context of the MCP server. All tools are MCPToolBase compliant and 
are suitable for both server and direct invocation (e.g., integration tests).
"""

from mcp.server.fastmcp import Context, FastMCP

from tools.base import MCPToolBase
from utilities.kql_validator import validate_kql


class KQLValidateTool(MCPToolBase):
    """
    Tool for validating KQL (Kusto Query Language) syntax locally.

    This tool checks the syntax of a provided KQL query without executing it
    against an Azure Log Analytics Workspace. It is intended for both MCP
    server use and direct invocation in integration tests.

    Attributes:
        name (str): The name of the tool.
        description (str): A brief description of the tool.

    Methods:
        run: Validate a KQL query and return the result.
    """

    name = "sentinel_query_validate"
    description = "Validate KQL Query Syntax locally"

    def dummy_public_method(self):
        """
        Dummy public method to satisfy pylint's too-few-public-methods warning.
        """
        return None

    async def run(self, ctx: Context, **kwargs):
        """
        Validate a KQL query and return the result.

        Args:
            ctx (Context): The context of the MCP server.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A dictionary containing the validation result.
        """
        # Extract query using the centralized parameter extraction from MCPToolBase
        query = self._extract_param(kwargs, "query")
        logger = self.logger
        if not query:
            logger.error("Missing required parameter: query")
            return {
                "error": "Missing required parameter: query",
                "valid": False,
                "errors": ["Missing required parameter: query"],
            }
        try:
            is_valid, errors = validate_kql(query)
            if is_valid:
                return {
                    "result": (
                        "Query validation passed. "
                        "The KQL syntax appears to be correct."
                    ),
                    "valid": True,
                    "errors": [],
                }
            error_message = "KQL validation failed:\n" + "\n".join(errors)
            # Warn via context if available
            if hasattr(ctx, "warning") and callable(getattr(ctx, "warning", None)):
                await ctx.warning(error_message)
            # Special handling for initialization error
            if any("KQL validation unavailable" in err for err in errors):
                return {"error": error_message, "valid": False, "errors": errors}
            return {"error": error_message, "valid": False, "errors": errors}
        except Exception as e:
            logger.error("Error validating KQL query: %s", e, exc_info=True)
            return {
                "error": (
                    "An error occurred while validating the query. "
                    "Try validating code by executing a KQL query against the "
                    "workspace instead: %s" % str(e)
                ),
                "valid": False,
                "errors": [str(e)],
            }


def register_tools(mcp: FastMCP):
    """
    Register KQL tools with the MCP server.

    Args:
        mcp (FastMCP): The MCP server instance to register tools with.
    """
    KQLValidateTool.register(mcp)
