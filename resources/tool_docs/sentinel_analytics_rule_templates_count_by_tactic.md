# Sentinel Analytics Rule Templates Count By Tactic Tool

**Tool Name:** `sentinel_analytics_rule_templates_count_by_tactic`

## Overview
Counts Microsoft Sentinel analytics rule templates by MITRE ATT&CK tactic. Returns a mapping of each tactic to the count and a list of template summaries.

## Parameters
- None required. Uses workspace context from MCP server or environment variables.

## Output
- `valid` (bool): True if query succeeded.
- `error` (str or None): Error message if any.
- `results` (dict):
    - Each key is a tactic (lowercase string or "unknown").
    - Each value is a dict with:
        - `count` (int): Number of templates for this tactic.
        - `templates` (list): List of dicts with `id` and `display_name` for each template.
- `errors` (list): List of error strings if any.

## Example Output
```
{
  "initialaccess": {
    "count": 115,
    "templates": [
      {"id": "...", "display_name": "Sign-ins from IPs that attempt sign-ins to disabled accounts"},
      ...
    ]
  },
  ...
}
```

## Error Handling
- Returns `error` and `errors` fields if context is missing or SDK/API errors occur.

## MCP Compliance
- Inherits from `MCPToolBase`.
- Implements `async def run(self, ctx, **kwargs)`.
- Registered in `register_tools()`.
- Uses robust Azure context extraction and error handling.
