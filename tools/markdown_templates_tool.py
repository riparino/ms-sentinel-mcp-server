"""
Tools for serving available markdown templates and their content for the MCP client.
Provides operations to list and retrieve markdown templates from resources/markdown_templates.
"""

import os
import json
from pathlib import Path
from typing import Any

from tools.base import MCPToolBase

TEMPLATE_DIR = Path(__file__).parent.parent / "resources" / "markdown_templates"


class MarkdownTemplatesListTool(MCPToolBase):
    """
    Tool for listing available markdown templates and their descriptions.
    """

    name = "markdown_templates_list"
    description = "List available markdown templates and their descriptions."

    async def run(self, ctx, **kwargs) -> Any:
        """
        List available markdown templates and their descriptions.

        Args:
            ctx: The context object (unused).
            **kwargs: Optional arguments (unused).

        Returns:
            dict: A dictionary containing a list of templates (with name, uri, description, and
                  content), or an error message if the directory cannot be read.
        """
        if isinstance(kwargs, str):
            try:
                kwargs = json.loads(kwargs)
            except Exception:
                kwargs = {}
        elif kwargs is None:
            kwargs = {}
        elif not isinstance(kwargs, dict):
            kwargs = dict(kwargs)
        try:
            if not TEMPLATE_DIR.exists() or not TEMPLATE_DIR.is_dir():
                return {
                    "error": f"Markdown templates directory does not exist: {TEMPLATE_DIR}"
                }
            templates = []
            for fname in os.listdir(TEMPLATE_DIR):
                if fname.endswith(".md"):
                    template_name = os.path.splitext(fname)[0]
                    path = TEMPLATE_DIR / fname
                    try:
                        with open(path, encoding="utf-8") as f:
                            first_line = f.readline().strip()
                            f.seek(0)
                            content = f.read()
                    except Exception as file_exc:
                        self.logger.error(
                            "Failed to read template %s: %s", fname, file_exc
                        )
                        continue
                    templates.append(
                        {
                            "name": template_name,
                            "uri": f"markdown://templates/{template_name}",
                            "description": (
                                first_line
                                if first_line.startswith("#")
                                else "Markdown template"
                            ),
                            "content": content,
                        }
                    )
            return {"templates": templates}
        except Exception as e:
            self.logger.error("Failed to list markdown templates: %s", e)
            return {"error": f"Failed to list markdown templates: {e}"}


class MarkdownTemplateGetTool(MCPToolBase):
    """
    Tool for retrieving the raw markdown content for a specific template by name.
    """

    name = "markdown_template_get"
    description = "Get the raw markdown content for a specific template by name."

    async def run(self, ctx, **kwargs) -> Any:
        """
        Get the raw markdown content for a specific template by name.

        Args:
            ctx: The context object (unused).
            **kwargs: Arguments containing 'name' (str), the template name (without extension).

        Returns:
            dict: A dictionary containing the template content, or an error message if not found or
                  unreadable.
        """

        if isinstance(kwargs, str):
            try:
                kwargs = json.loads(kwargs)
            except Exception:
                kwargs = {}
        elif kwargs is None:
            kwargs = {}
        elif not isinstance(kwargs, dict):
            kwargs = dict(kwargs)
        # Extract name parameter using the centralized parameter extraction from MCPToolBase
        name = self._extract_param(kwargs, "name")
        if not name or not isinstance(name, str):
            return {"error": "Missing or invalid required parameter: name"}
        try:
            if not TEMPLATE_DIR.exists() or not TEMPLATE_DIR.is_dir():
                return {
                    "error": f"Markdown templates directory does not exist: {TEMPLATE_DIR}"
                }
            path = TEMPLATE_DIR / f"{name}.md"
            path.resolve().relative_to(TEMPLATE_DIR.resolve())
            if not path.exists():
                try:
                    available = [
                        os.path.splitext(f)[0]
                        for f in os.listdir(TEMPLATE_DIR)
                        if f.endswith(".md")
                    ]
                except Exception as list_exc:
                    self.logger.error("Failed to list templates: %s", list_exc)
                    available = []
                return {
                    "error": f"Markdown template not found: {name}",
                    "available_templates": available,
                }
            try:
                content = path.read_text(encoding="utf-8")
            except Exception as file_exc:
                self.logger.error("Failed to read template %s: %s", name, file_exc)
                return {"error": f"Failed to read markdown template: {file_exc}"}
            return {"content": content}
        except Exception as e:
            self.logger.error("Failed to get markdown template '%s': %s", name, e)
            return {"error": f"Failed to get markdown template: {e}"}


def register_tools(mcp):
    """
    Register the markdown templates tools with the MCP server.

    Args:
        mcp: The MCP server or registry to register the tools with.
    """
    MarkdownTemplatesListTool.register(mcp)
    MarkdownTemplateGetTool.register(mcp)
