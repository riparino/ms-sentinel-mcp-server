"""
MCP-compliant tool-based documentation provider for Sentinel MCP server tools.

This module provides tools for listing, retrieving, and searching markdown documentation
in the resources/tool_docs directory. It exposes the following tools:
    - ToolDocsListTool: Enumerate available documentation markdown paths.
    - ToolDocsGetTool: Retrieve raw markdown content for a given documentation path.
    - ToolDocsSearchTool: Full-text search across documentation files.
    - LLMInstructionsGetTool: Retrieve LLM usage instructions for the Sentinel MCP Server.
"""

import re
import json
from pathlib import Path
from typing import Any
from tools.base import MCPToolBase

# Path to the documentation root
DOC_ROOT = Path(__file__).parent.parent / "resources" / "tool_docs"


class ToolDocsListTool(MCPToolBase):
    """Tool for enumerating available Sentinel server documentation markdown paths."""

    name = "tool_docs_list"
    description = "Enumerate available Sentinel server documentation markdown paths."

    async def run(self, ctx, **kwargs) -> Any:
        """
        Enumerate available Sentinel server documentation markdown paths.

        Args:
            ctx: The tool context (unused).
            **kwargs: Optional arguments. May include:
                - prefix (str, optional):
                  Only include docs whose relative path starts with this prefix.

        Returns:
            dict: {
                'paths': list of relative markdown doc paths,
                'error': error message if directory cannot be read
            }
        """

        # Defensive: handle string, None, or dict for kwargs

        # Extract prefix parameter using the centralized parameter extraction from MCPToolBase
        prefix = self._extract_param(kwargs, "prefix")
        try:
            paths = [str(p.relative_to(DOC_ROOT)) for p in DOC_ROOT.rglob("*.md")]
            if prefix:
                paths = [p for p in paths if p.startswith(prefix)]
            return {"paths": paths}
        except Exception as e:
            return {"error": f"Failed to list docs: {e}"}


class ToolDocsGetTool(MCPToolBase):
    """Tool for retrieving the raw markdown for a given documentation path."""

    name = "tool_docs_get"
    description = "Return the raw markdown for a given documentation path."

    async def run(self, ctx, **kwargs) -> Any:
        """
        Return the raw markdown for a given documentation path.

        Args:
            ctx: The tool context (unused).
            **kwargs: Should include:
                - path (str): Relative path to the markdown doc (as returned by list_docs).

        Returns:
            dict: {
                'content': raw markdown content of the file,
                'error': error message if file does not exist or is outside the docs directory,
                'available_docs': list of available docs if file not found
            }
        """

        # Defensive: handle string, None, or dict for kwargs

        # Extract path parameter using the centralized parameter extraction from MCPToolBase
        path = self._extract_param(kwargs, "path")

        # Check if path is a string
        if path is not None and not isinstance(path, str):
            return {"error": "Invalid path type. Expected a string."}

        if not path:
            return {"error": "Missing required parameter: path"}

        try:
            file = DOC_ROOT / path
            file.resolve().relative_to(DOC_ROOT.resolve())
            if not file.exists():
                # Suggest available docs
                available = [
                    str(p.relative_to(DOC_ROOT)) for p in DOC_ROOT.rglob("*.md")
                ]
                return {"error": f"Doc not found: {path}", "available_docs": available}
            content = file.read_text(encoding="utf-8")
            return {"content": content}
        except Exception as e:
            return {"error": f"Failed to read doc: {e}"}


class ToolDocsSearchTool(MCPToolBase):
    """Tool for full-text search across documentation; returns matching paths."""

    name = "tool_docs_search"
    description = "Full-text search across documentation; returns matching paths."

    async def run(self, ctx, **kwargs) -> Any:
        """
        Full-text search across documentation; returns matching paths.

        Args:
            ctx: The tool context (unused).
            **kwargs: Should include:
                - query (str): Regex or text to search for in docs.
                - k (int, optional): Max number of results to return (default 10).

        Returns:
            dict: {
                'hits': list of relative doc paths containing a match,
                'error': error message if search fails
            }
        """

        # Defensive: handle string, None, or dict for kwargs

        # Extract parameters using the centralized parameter extraction from MCPToolBase
        query = self._extract_param(kwargs, "query")
        k = self._extract_param(kwargs, "k")
        if not query:
            return {"error": "Missing required parameter: query"}
        try:
            candidates = [str(p.relative_to(DOC_ROOT)) for p in DOC_ROOT.rglob("*.md")]
            pat = re.compile(query, re.I)
            hits = []
            for p in candidates:
                content = (DOC_ROOT / p).read_text(encoding="utf-8")
                if pat.search(content):
                    hits.append(p)
                    if k and len(hits) >= int(k):
                        break
            return {"hits": hits}
        except Exception as e:
            return {"error": f"Failed to search docs: {e}"}


class LLMInstructionsGetTool(MCPToolBase):
    """Tool for retrieving the LLM usage instructions for the Sentinel MCP Server."""

    name = "llm_instructions_get"
    description = (
        "Retrieve the LLM usage instructions for the Sentinel MCP Server. "
        "Use this tool first before all other tools."
    )

    async def run(self, ctx, **kwargs) -> Any:
        """
        Retrieve the LLM usage instructions for the Sentinel MCP Server.

        Args:
            ctx: The tool context (unused).
            **kwargs: Optional arguments (unused).

        Returns:
            dict: {
                'content': raw markdown content of docs/llm_instructions.md,
                'error': error message if file cannot be read
            }
        """

        # Defensive: handle string, None, or dict for kwargs (even if unused)

        # No parameters to extract, but we'll normalize kwargs for consistency
        # using the centralized parameter extraction from MCPToolBase
        _ = self._extract_param(kwargs, "")
        try:
            llm_path = Path(__file__).parent.parent / "docs" / "llm_instructions.md"
            content = llm_path.read_text(encoding="utf-8")
            return {"content": content}
        except Exception as e:
            return {"error": f"Failed to read LLM instructions: {e}"}


def register_tools(mcp):
    """Register all documentation tools with the given MCP server instance."""
    ToolDocsListTool.register(mcp)
    ToolDocsGetTool.register(mcp)
    ToolDocsSearchTool.register(mcp)
    LLMInstructionsGetTool.register(mcp)
