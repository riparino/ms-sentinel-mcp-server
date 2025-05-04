#!/usr/bin/env python3
"""
FILE: register_components.py
DESCRIPTION:
    Automatically registers components with the MCP server on import.
"""

import os
import importlib.util
from typing import List
from utilities.logging import get_component_logger
from utilities.path_utils import resolve_path

# Use centralized logging configuration
logger = get_component_logger()


def load_components(
    mcp, component_dir: str, register_func_name: str = "register_resources"
) -> List[str]:
    """Basic component loader implementation to avoid import issues."""
    logger.info("Attempting to load components from %s", component_dir)

    # Ensure component_dir is an absolute path
    component_dir = resolve_path(component_dir)

    # Return early if directory doesn't exist
    if not os.path.exists(component_dir):
        logger.warning("Component directory not found: %s", component_dir)
        return []

    # List Python files
    try:
        module_files = [
            f
            for f in os.listdir(component_dir)
            if f.endswith(".py") and f != "__init__.py"
        ]
        logger.info(
            "Found %d module files in %s: %s",
            len(module_files),
            component_dir,
            ", ".join(module_files),
        )
    except Exception as e:
        logger.error("Error listing directory %s: %s", component_dir, e)
        return []

    registered_modules = []

    # Load each module
    for file in module_files:
        module_path = os.path.join(component_dir, file)
        module_name = file[:-3]  # Remove .py extension

        try:
            logger.info("Attempting to load %s", module_path)

            # Use importlib to load the module from file path
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Check for registration function
                if hasattr(module, register_func_name):
                    register_func = getattr(module, register_func_name)
                    register_func(mcp)
                    registered_modules.append(module_name)
                    logger.info(
                        "Successfully registered components from %s",
                        module_name,
                    )
                else:
                    logger.warning(
                        "No %s function found in %s",
                        register_func_name,
                        module_name,
                    )
            else:
                logger.error("Failed to create module spec for %s", module_path)

        except Exception as e:
            logger.error("Error loading module %s: %s", module_name, e)

    return registered_modules
