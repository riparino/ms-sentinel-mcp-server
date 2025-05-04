# Sentinel Analytics Rules Count By Technique Tool

**Tool Name:** `sentinel_analytics_rules_count_by_technique`

## Overview
Counts Microsoft Sentinel analytics rules by MITRE ATT&CK technique (or comma-separated list of techniques). Returns a mapping of each technique to the count and a list of rule summaries.

## Parameters
- None required. Uses workspace context from MCP server or environment variables.

## Output
- `valid` (bool): True if query succeeded.
- `error` (str or None): Error message if any.
- `results` (dict):
    - Each key is a technique (lowercase string or "unknown").
    - Each value is a dict with:
        - `count` (int): Number of rules for this technique.
        - `rules` (list): List of dicts with `id` and `display_name` for each rule.
- `errors` (list): List of error strings if any.

## Example Output
```
{
  "unknown": {
    "count": 28,
    "rules": [
      {"id": "...", "display_name": "Advanced Multistage Attack Detection"},
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
