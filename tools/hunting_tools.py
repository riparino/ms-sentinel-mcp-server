from mcp.server.fastmcp import Context, FastMCP

from tools.base import MCPToolBase

# FILE: tools/hunting_tools.py
# DESCRIPTION:
#     Provides Microsoft Sentinel advanced hunting tools for the MCP server.
#     Refactored for MCPToolBase compliance (class-based, robust context extraction,
#     kwargs handling).


def extract_tags_tactics_techniques(obj):
    """
    Extracts tags, tactics, and techniques from a hunting query object.
    Returns:
        tags: List of {name, value} dicts.
        tactics: List of tactics (from tags or legacy fields).
        techniques: List of techniques (from tags or legacy fields).
    Extraction precedence:
      - Tactics/techniques: Prefer tags with name 'tactics'/'techniques'
        (case-insensitive, split on comma). Fallback to legacy fields.
      - Tags: All tags as {name, value} pairs (robust to SDK object, dict, or string).
    """
    tags = []
    tactics = []
    techniques = []
    # Extract tags as list of {name, value}
    raw_tags = getattr(obj, "tags", None)
    if raw_tags:
        for tag in raw_tags:
            tag_name = None
            tag_value = None
            # Tag as dict
            if isinstance(tag, dict):
                tag_name = tag.get("name") or tag.get("Name")
                tag_value = tag.get("value") or tag.get("Value")
            # Tag as object with .name/.value
            elif hasattr(tag, "name") and hasattr(tag, "value"):
                tag_name = getattr(tag, "name", None)
                tag_value = getattr(tag, "value", None)
            # Tag as string: treat as name only
            elif isinstance(tag, str):
                tag_name = tag
                tag_value = None
            # Fallback: try string conversion
            else:
                try:
                    tag_name = str(tag)
                except Exception:
                    continue
            if tag_name is not None:
                tags.append({"name": tag_name, "value": tag_value})
    # Tactics/techniques from tags (case-insensitive match)
    for tag in tags:
        if tag["name"] and isinstance(tag["name"], str):
            if tag["name"].lower() == "tactics" and tag["value"]:
                tactics += [t.strip() for t in tag["value"].split(",") if t.strip()]
            elif tag["name"].lower() == "techniques" and tag["value"]:
                techniques += [t.strip() for t in tag["value"].split(",") if t.strip()]
    # Fallback: legacy fields
    legacy_tactics = getattr(obj, "tactics", None)
    if legacy_tactics:
        tactics += [
            t.strip() for t in legacy_tactics if isinstance(t, str) and t.strip()
        ]
    legacy_techniques = getattr(obj, "techniques", None)
    if legacy_techniques:
        techniques += [
            t.strip() for t in legacy_techniques if isinstance(t, str) and t.strip()
        ]
    # Deduplicate and preserve order
    tactics = list(dict.fromkeys([t for t in tactics if t]))
    techniques = list(dict.fromkeys([t for t in techniques if t]))
    return tags, tactics, techniques


class SentinelHuntingQueriesListTool(MCPToolBase):
    name = "sentinel_hunting_queries_list"
    description = (
        "List all Sentinel hunting queries (saved searches) with "
        "optional tactic/technique filtering"
    )

    async def run(self, ctx: Context, **kwargs):
        """
        List all Sentinel hunting queries (saved searches) with optional
        tactic/technique filtering.
        Extracts tags, tactics, and techniques using shared utility.
        """
        # Extract parameters using the centralized parameter extraction from MCPToolBase
        tactics = self._extract_param(kwargs, "tactics")
        techniques = self._extract_param(kwargs, "techniques")
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)
        client = self.get_loganalytics_client(subscription_id)
        result = []
        tactic_set = (
            {t.strip().lower() for t in tactics.split(",")} if tactics else None
        )
        technique_set = (
            {t.strip().lower() for t in techniques.split(",")} if techniques else None
        )
        try:
            searches = client.saved_searches.list_by_workspace(
                resource_group, workspace_name
            )
            for s in getattr(searches, "value", []):
                tags, s_tactics, s_techniques = extract_tags_tactics_techniques(s)
                # Filtering
                if tactic_set and not any(t.lower() in tactic_set for t in s_tactics):
                    continue
                if technique_set and not any(
                    t.lower() in technique_set for t in s_techniques
                ):
                    continue
                result.append(
                    {
                        "id": getattr(s, "id", None),
                        "name": getattr(s, "name", None),
                        "display_name": getattr(
                            s, "display_name", getattr(s, "name", None)
                        ),
                        "category": getattr(s, "category", None),
                        "query": getattr(s, "query", None),
                        "tags": tags,
                        "tactics": s_tactics,
                        "techniques": s_techniques,
                        "description": getattr(s, "description", None),
                        "version": getattr(s, "version", None),
                    }
                )
            return {"valid": True, "error": None, "results": result, "errors": []}
        except Exception as e:
            self.logger.error("Error in %s: %s", self.__class__.__name__, str(e))
            return {
                "valid": False,
                "error": str(e),
                "results": None,
                "errors": [str(e)],
            }


class SentinelHuntingQueriesCountByTacticTool(MCPToolBase):
    name = "sentinel_hunting_queries_count_by_tactic"
    description = "Count Sentinel hunting queries (saved searches) by tactic"

    async def run(self, ctx: Context, **_):
        """
        Count Sentinel hunting queries (saved searches) by tactic.
        Extracts tags, tactics, and techniques using shared utility.
        """
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)
        client = self.get_loganalytics_client(subscription_id)
        tactic_map = {}
        try:
            searches = client.saved_searches.list_by_workspace(
                resource_group, workspace_name
            )
            for s in getattr(searches, "value", []):
                _, s_tactics, _ = extract_tags_tactics_techniques(s)
                for tactic in s_tactics or ["Unknown"]:
                    tkey = tactic.lower() or "unknown"
                    if tkey not in tactic_map:
                        tactic_map[tkey] = {"count": 0, "queries": []}
                    tactic_map[tkey]["count"] += 1
                    tactic_map[tkey]["queries"].append(
                        {
                            "id": s.id,
                            "display_name": getattr(s, "display_name", s.name),
                        }
                    )
            return {
                "valid": True,
                "error": None,
                "results": tactic_map,
                "errors": [],
            }
        except Exception as e:
            self.logger.error("Error in %s: %s", self.__class__.__name__, str(e))
            return {
                "valid": False,
                "error": str(e),
                "results": None,
                "errors": [str(e)],
            }


class SentinelHuntingQueryGetTool(MCPToolBase):
    """
    MCP-compliant tool to retrieve the full details of a Sentinel hunting query
    (saved search) by name or ID.

    Parameters:
        query_id (str, optional): The full resource ID or GUID of the saved search.
        name (str, optional): The display name or name of the saved search.

    Returns:
        dict: Details of the hunting query, or error if not found. Output keys:
            - valid (bool): True if successful, False otherwise
            - error (str or None): Error message if any
            - results (dict or None): Full hunting query details if found
            - errors (list): List of error messages

    Error Cases:
        - If neither query_id nor name is provided, returns an error.
        - If no matching hunting query is found, returns an error.
        - Azure API or credential errors are reported in the error field.
    """

    name = "sentinel_hunting_query_get"
    description = (
        "Get full details of a Sentinel hunting query (saved search) by name or ID."
    )

    async def run(self, ctx: Context, **kwargs):
        """
        Get full details of a Sentinel hunting query (saved search) by name or ID.
        Extracts all tags, tactics, and techniques using shared utility.
        """
        # Extract parameters using the centralized parameter extraction from MCPToolBase
        query_id = self._extract_param(kwargs, "query_id")
        name = self._extract_param(kwargs, "name")
        if not query_id and not name:
            return {
                "valid": False,
                "error": (
                    "Must provide either 'query_id' or 'name' to identify "
                    "the hunting query."
                ),
                "results": None,
                "errors": [
                    (
                        "Must provide either 'query_id' or 'name' to identify "
                        "the hunting query."
                    )
                ],
            }
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)
        client = self.get_loganalytics_client(subscription_id)
        try:
            searches = client.saved_searches.list_by_workspace(
                resource_group, workspace_name
            )
            match = None
            for s in getattr(searches, "value", []):
                if (query_id and getattr(s, "id", None) == query_id) or (
                    name and getattr(s, "name", None) == name
                ):
                    match = s
                    break
            if not match:
                return {
                    "valid": False,
                    "error": "No matching hunting query found.",
                    "results": None,
                    "errors": ["No matching hunting query found."],
                }
            tags, tactics, techniques = extract_tags_tactics_techniques(match)
            details = {
                "id": getattr(match, "id", None),
                "name": getattr(match, "name", None),
                "display_name": getattr(
                    match, "display_name", getattr(match, "name", None)
                ),
                "category": getattr(match, "category", None),
                "query": getattr(match, "query", None),
                "tags": tags,
                "tactics": tactics,
                "techniques": techniques,
                "description": getattr(match, "description", None),
                "version": getattr(match, "version", None),
            }
            return {"valid": True, "error": None, "results": details, "errors": []}
        except Exception as e:
            self.logger.error("Error in %s: %s", self.__class__.__name__, str(e))
            return {
                "valid": False,
                "error": str(e),
                "results": None,
                "errors": [str(e)],
            }


def register_tools(mcp: FastMCP):
    SentinelHuntingQueriesListTool.register(mcp)
    SentinelHuntingQueriesCountByTacticTool.register(mcp)
    SentinelHuntingQueryGetTool.register(mcp)
