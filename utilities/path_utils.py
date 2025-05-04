"""
FILE: utilities/path_utils.py
DESCRIPTION:
    Provides utilities for consistent path handling across the application.
"""

import os
import sys
import logging
from typing import Optional, List

# Set up logger for this module
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def get_project_root() -> str:
    """
    Get the project root directory.

    This looks for common project markers like setup.py, pyproject.toml,
    or .git directory to locate the project root.

    Returns:
        str: Absolute path to the project root directory
    """
    # Start with the directory of the current file
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Look for project root markers
    root_markers = [
        "setup.py",
        "pyproject.toml",
        ".git",
        "README.md",
        "requirements.txt",
    ]

    # First check if we're already at the root
    for marker in root_markers:
        if os.path.exists(os.path.join(current_dir, marker)):
            logger.debug("Project root detected at current directory: %s", current_dir)
            return current_dir

    # If not at root, try parent directories (up to 3 levels)
    parent_dir = current_dir
    for _ in range(3):
        parent_dir = os.path.dirname(parent_dir)
        for marker in root_markers:
            if os.path.exists(os.path.join(parent_dir, marker)):
                logger.debug("Project root detected at: %s", parent_dir)
                return parent_dir

    # If no root markers found, default to current directory
    logger.warning("Could not detect project root, using current directory")
    return current_dir


def resolve_path(relative_path: str, base_dir: Optional[str] = None) -> str:
    """
    Resolve a relative path to an absolute path.

    Args:
        relative_path: Path relative to base_dir
        base_dir: Base directory (defaults to project root if None)

    Returns:
        str: Absolute path
    """
    if os.path.isabs(relative_path):
        return relative_path

    if base_dir is None:
        base_dir = get_project_root()

    absolute_path = os.path.abspath(os.path.join(base_dir, relative_path))
    return absolute_path


def find_file(
    filename: str,
    search_dirs: Optional[List[str]] = None,
    base_dir: Optional[str] = None,
) -> Optional[str]:
    """
    Find a file in multiple possible directories.

    Args:
        filename: Name of the file to find
        search_dirs: List of directories to search in (relative to base_dir)
        base_dir: Base directory for relative paths (defaults to project root)

    Returns:
        Optional[str]: Absolute path to the file if found, None otherwise
    """
    if base_dir is None:
        base_dir = get_project_root()

    # If no search dirs specified, use common locations
    if search_dirs is None:
        search_dirs = [
            ".",  # Project root
            "lib",  # Libraries
            "docs",  # Documentation
            os.path.join("utilities", "lib"),  # Module-specific libraries
            "resources",  # Resources
        ]

    # Check each search directory
    for directory in search_dirs:
        path = os.path.join(base_dir, directory, filename)
        if os.path.exists(path):
            logger.debug("Found file %s at %s", filename, path)
            return os.path.abspath(path)

    # Also check the directory of the current file
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(current_dir, filename)
    if os.path.exists(path):
        logger.debug("Found file %s at %s", filename, path)
        return os.path.abspath(path)

    logger.warning("File %s not found in any search directories", filename)
    return None


def ensure_directory(directory: str, base_dir: Optional[str] = None) -> str:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        directory: Directory path (absolute or relative to base_dir)
        base_dir: Base directory (defaults to project root if None)

    Returns:
        str: Absolute path to the directory
    """
    if not os.path.isabs(directory) and base_dir is not None:
        directory = os.path.join(base_dir, directory)

    absolute_dir = os.path.abspath(directory)

    if not os.path.exists(absolute_dir):
        try:
            os.makedirs(absolute_dir, exist_ok=True)
            logger.debug("Created directory: %s", absolute_dir)
        except Exception as e:
            logger.error("Failed to create directory %s: %s", absolute_dir, e)

    return absolute_dir
