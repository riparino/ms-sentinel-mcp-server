# Sentinel Analytics Rule List Tool

**Tool Name:** `sentinel_analytics_rule_list`

## Overview
Lists all Microsoft Sentinel analytics rules in the current workspace, returning key fields for each rule.

## Parameters
- None required. Uses workspace context from MCP server or environment variables.

## Output
- List of dicts, each containing:
    - `id` (str): Rule ID.
    - `name` (str): Rule name.
    - `display_name` (str): Display name of the rule.
    - `enabled` (bool): Whether the rule is enabled.
    - `severity` (str): Severity level.
    - `description` (str): Description of the rule.
    - `last_modified_utc` (str): Last modification date/time (UTC).
    - `kind` (str): Rule kind/type.
    - ... (other available summary fields)
- If error, returns a dict with `error` (str).

## Example Output
```
[
  {
    "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace>/providers/Microsoft.SecurityInsights/alertRules/BuiltInFusion",
    "name": "BuiltInFusion",
    "kind": "Fusion",
    "displayName": "Advanced Multistage Attack Detection",
    "severity": "High",
    "enabled": true
  },
  {
    "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace>/providers/Microsoft.SecurityInsights/alertRules/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "name": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "kind": "Scheduled",
    "displayName": "New CloudShell User",
    "severity": "Low",
    "enabled": true
  },
  ...
]
```

## Error Handling
- Returns `error` field if context is missing or SDK/API errors occur.

## MCP Compliance
- Inherits from `MCPToolBase`.
- Implements `async def run(self, ctx, **kwargs)`.
- Registered in `register_tools()`.
- Uses robust Azure context extraction and error handling.
