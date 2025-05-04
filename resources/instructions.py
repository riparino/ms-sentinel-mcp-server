"""
FILE: resources/instructions.py
DESCRIPTION:
    Provides onboarding instructions as a resource for the MCP server.
"""

from mcp.server.fastmcp import FastMCP
import os

# Try to load the onboarding instructions from llm_instructions.md
INSTRUCTIONS_PATHS = [
    os.path.join(os.path.dirname(__file__), "..", "docs", "llm_instructions.md"),
    os.path.join(os.path.dirname(__file__), "llm_instructions.md"),
    os.path.join(os.path.dirname(__file__), "..", "resources", "llm_instructions.md"),
]


def load_onboarding_instructions() -> str:
    for path in INSTRUCTIONS_PATHS:
        try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
        except Exception:
            pass
    return "Onboarding instructions not available."


def register_resources(mcp: FastMCP):
    """Register the onboarding instructions resource."""

    @mcp.resource("resource://instructions")
    def get_instructions() -> str:
        return load_onboarding_instructions()
