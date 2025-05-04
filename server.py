#!/usr/bin/env python3

"""
FILE: server.py
DESCRIPTION:
    Microsoft Sentinel MCP Server implementation.
"""

# Auto-load .env file for environment variables regardless of runner
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # dotenv is optional; log a warning if needed

import os
import sys
import signal
import asyncio
import tempfile
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Optional, Dict, Any
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, MetricsQueryClient
from azure.mgmt.securityinsight import SecurityInsights
from azure.mgmt.loganalytics import LogAnalyticsManagementClient
from mcp.server.fastmcp import FastMCP
from utilities.path_utils import find_file

# Import and configure logging FIRST
from utilities.logging import get_server_logger

# Configure logging
log_dir = tempfile.gettempdir()
log_file = os.path.join(log_dir, "sentinel_mcp_server.log")
logger = get_server_logger(log_file=log_file)


@dataclass
class AzureServicesContext:
    """Container for Azure service clients and credentials"""

    credential: Optional[DefaultAzureCredential]
    logs_client: Optional[LogsQueryClient]
    metrics_client: Optional[MetricsQueryClient]
    security_insights_client: Optional[SecurityInsights]
    loganalytics_client: Optional[LogAnalyticsManagementClient]
    workspace_id: str
    workspace_name: str
    subscription_id: str
    resource_group: str
    config: Dict[str, Any]


@asynccontextmanager
async def azure_services_lifespan(
    _: FastMCP,
) -> AsyncIterator[AzureServicesContext]:
    """Manage Azure service clients lifecycle with type-safe context"""
    # Initialize on startup
    logger.info("Initializing Azure service clients...")

    # Load configuration from environment variables
    # dotenv will be loaded by MCP CLI when using the -f .env flag
    config = {
        "workspace_id": os.environ.get("AZURE_WORKSPACE_ID", ""),
        "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID", ""),
        "resource_group": os.environ.get("AZURE_RESOURCE_GROUP", ""),
        "tenant_id": os.environ.get("AZURE_TENANT_ID", ""),
        "workspace_name": os.environ.get("AZURE_WORKSPACE_NAME", ""),
    }

    # Log non-secret Azure environment variables on server startup
    logger.info("AZURE_TENANT_ID: %s", os.environ.get("AZURE_TENANT_ID", ""))
    logger.info("AZURE_CLIENT_ID: %s", os.environ.get("AZURE_CLIENT_ID", ""))
    logger.info(
        "AZURE_SUBSCRIPTION_ID: %s", os.environ.get("AZURE_SUBSCRIPTION_ID", "")
    )
    logger.info("AZURE_RESOURCE_GROUP: %s", os.environ.get("AZURE_RESOURCE_GROUP", ""))
    logger.info("AZURE_WORKSPACE_NAME: %s", os.environ.get("AZURE_WORKSPACE_NAME", ""))
    logger.info("AZURE_WORKSPACE_ID: %s", os.environ.get("AZURE_WORKSPACE_ID", ""))
    # Only log presence of secret, not its value
    logger.info(
        "AZURE_CLIENT_SECRET set: %s",
        "yes" if os.environ.get("AZURE_CLIENT_SECRET") else "no",
    )

    # Validate required configuration
    missing_vars = [k for k, v in config.items() if not v]
    if missing_vars:
        logger.warning("Missing environment variables: %s", ", ".join(missing_vars))
        logger.warning("Some functionality may be limited.")

    try:
        # Create the credential once and reuse it
        credential = DefaultAzureCredential()

        # Create the Azure Monitor clients
        logs_client = LogsQueryClient(credential)
        metrics_client = MetricsQueryClient(credential)

        # Create the Security Insights client
        security_insights_client = SecurityInsights(
            credential=credential, subscription_id=config["subscription_id"]
        )

        # Create the Log Analytics Management client if available
        try:
            loganalytics_client = LogAnalyticsManagementClient(
                credential=credential, subscription_id=config["subscription_id"]
            )
            logger.info("Successfully initialized Log Analytics Management client")
        except ImportError:
            logger.warning("Module azure-mgmt-loganalytics not found")
            logger.warning("Skipping LogAnalyticsManagementClient initialization")
            loganalytics_client = None
        except Exception as e:
            msg = "Failed to initialize LogAnalyticsManagementClient: %s"
            logger.error(msg, e)
            loganalytics_client = None

        # Yield the context with all necessary clients
        yield AzureServicesContext(
            credential=credential,
            logs_client=logs_client,
            metrics_client=metrics_client,
            security_insights_client=security_insights_client,
            loganalytics_client=loganalytics_client,
            workspace_id=config["workspace_id"],
            workspace_name=config["workspace_name"],
            subscription_id=config["subscription_id"],
            resource_group=config["resource_group"],
            config=config,
        )
    except Exception as e:
        logger.error("Failed to initialize Azure services: %s", e)
        logger.info("Creating minimal context with empty clients")
        # Yield a minimal context to prevent server crash
        # In this case, the server will run but tools requiring Azure will return errors
        yield AzureServicesContext(
            credential=None,
            logs_client=None,
            metrics_client=None,
            security_insights_client=None,
            loganalytics_client=None,
            workspace_id=config["workspace_id"],
            workspace_name=config["workspace_name"],
            subscription_id=config["subscription_id"],
            resource_group=config["resource_group"],
            config=config,
        )
    finally:
        # Cleanup on shutdown
        logger.info("Shutting down Azure service clients...")

        # Clean up any running tasks
        try:
            # Import here to avoid import errors if not found
            # pylint: disable=import-outside-toplevel
            from utilities.task_manager import cleanup_tasks

            await cleanup_tasks()
        except Exception as e:
            logger.error("Error during task cleanup: %s", e)


def load_instructions() -> str:
    """Load LLM instructions from file using consistent path handling."""
    # Try to find the instructions file in various locations
    instructions_filename = "llm_instructions.md"
    search_dirs = ["docs", ".", "resources"]

    instructions_path = find_file(instructions_filename, search_dirs)

    if instructions_path:
        try:
            logger.info("Loading instructions from: %s", instructions_path)
            with open(instructions_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.error("Error reading instructions file: %s", e)
    else:
        logger.warning(
            "Instructions file '%s' not found in search directories",
            instructions_filename,
        )

        # Default instructions if file not found
    default_instructions = (
        "Welcome to Microsoft Sentinel MCP Server. Use tools and resources to explore this "
        "server's capabilities.\n"
        "Interact with Azure Sentinel data. Run sentinel_logs_tables_list to see available "
        "data tables."
    )
    return default_instructions


# Create the MCP server instance (global for MCP CLI to discover)
mcp = FastMCP(
    "Microsoft Sentinel MCP Server",
    lifespan=azure_services_lifespan,
    dependencies=[
        "azure-identity",
        "azure-monitor-query",
        "azure-mgmt-securityinsight",
        "azure-mgmt-loganalytics",
    ],
    instructions=load_instructions(),
)

# Auto-load components when the module is imported - this will happen with MCP CLI
try:
    # Determine paths to component directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = os.path.join(script_dir, "resources")
    tools_dir = os.path.join(script_dir, "tools")
    prompts_dir = os.path.join(script_dir, "prompts")

    logger.info("Auto-loading components from %s", script_dir)
    logger.info("Resources directory: %s", resources_dir)
    logger.info("Tools directory: %s", tools_dir)
    logger.info("Prompts directory: %s", prompts_dir)

    # Import the component loader
    sys.path.insert(0, script_dir)
    from register_components import load_components

    # Register resources and tools
    if os.path.exists(resources_dir):
        resources = load_components(mcp, resources_dir, "register_resources")
        logger.info("Auto-registered %d resource modules", len(resources))

    if os.path.exists(tools_dir):
        tools = load_components(mcp, tools_dir, "register_tools")
        logger.info("Auto-registered %d tool modules", len(tools))

    if os.path.exists(prompts_dir):
        prompts = load_components(mcp, prompts_dir, "register_prompts")
        logger.info("Auto-registered %d prompt modules", len(prompts))
except Exception as e:
    logger.error("Error during component auto-loading: %s", e, exc_info=True)
    logger.info("Basic tools will still be available")


def main(port: int = 8000, transport: str = None):
    """Main entry point for the MCP server."""

    # Set up signal handlers for graceful shutdown
    def signal_handler(_sig, _frame):
        logger.info("Shutdown signal received, exiting gracefully...")

    # Register the signal handler for SIGINT (CTRL+C)
    signal.signal(signal.SIGINT, signal_handler)

    try:
        # Let MCP CLI handle the transport configuration
        logger.info("Running server... transport=%s, port=%s", transport, port)
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, shutting down...")
        sys.exit(0)
    except asyncio.CancelledError:
        logger.info(
            "Asyncio CancelledError received during shutdown, exiting cleanly..."
        )
        sys.exit(0)
    except Exception as e:
        logger.error("Error starting server: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Microsoft Sentinel MCP Server")
    parser.add_argument(
        "--sse",
        action="store_true",
        help="Run server in SSE (HTTP) mode instead of STDIO",
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=8000,
        help="Port for SSE server (default: 8000)",
    )
    args = parser.parse_args()
    main(port=args.port, transport="sse" if args.sse else None)
