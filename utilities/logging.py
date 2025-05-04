"""
FILE: utilities/logging.py
DESCRIPTION:
    Centralized logging configuration for the MCP server.
"""

import sys
import logging
import os
from typing import Optional

# Define standard log levels
LOG_LEVEL_DEBUG = logging.DEBUG
LOG_LEVEL_INFO = logging.INFO
LOG_LEVEL_WARNING = logging.WARNING
LOG_LEVEL_ERROR = logging.ERROR


def configure_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    format_string: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
) -> logging.Logger:
    """
    Configure and return a logger with consistent formatting.

    Args:
        name: The name of the logger
        level: The logging level
        log_file: Optional path to a log file
        format_string: Format string for the logger

    Returns:
        A configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Always log to stderr
    stderr_handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(format_string)
    stderr_handler.setFormatter(formatter)
    logger.addHandler(stderr_handler)

    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def configure_azure_sdk_logging(level: int = logging.WARNING) -> None:
    """
    Configure Azure SDK libraries to use a higher log level to reduce verbosity.
    
    Args:
        level: The logging level to set for Azure SDK loggers (default: WARNING)
    """
    # Configure specific Azure SDK loggers to use a higher log level
    azure_loggers = [
        "azure",
        "azure.identity",
        "azure.core.pipeline.policies.http_logging_policy",
        "azure.mgmt.loganalytics",
        "azure.mgmt.securityinsight",
        "azure.monitor.query",
        "msal",
    ]
    
    for logger_name in azure_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)


# Pre-configured loggers for common components
def get_server_logger(log_file: str = None) -> logging.Logger:
    """Get the main server logger."""
    # Configure Azure SDK logging to reduce verbosity
    configure_azure_sdk_logging()
    
    # Get environment variable for debug logging, defaulting to INFO
    debug_log = os.environ.get("MCP_DEBUG_LOG", "0")
    log_level = logging.DEBUG if debug_log.lower() in ("1", "true", "yes") else logging.INFO
    
    return configure_logger("sentinel_mcp", level=log_level, log_file=log_file)


def get_component_logger() -> logging.Logger:
    """Get the component loader logger."""
    return configure_logger("component_loader", level=logging.DEBUG)


def get_tool_logger(tool_name: str) -> logging.Logger:
    """Get a logger for a specific tool."""
    return configure_logger(f"tool.{tool_name}")
