# Sentinel Analytics Rule Templates List Tool

**Tool Name:** `sentinel_analytics_rule_templates_list`

## Overview
Lists all Microsoft Sentinel analytics rule templates in the current workspace, returning key fields for each template.

## Parameters
- None required. Uses workspace context from MCP server or environment variables.

## Output
- List of dicts, each containing:
    - `id` (str): Template ID.
    - `name` (str): Template name.
    - `display_name` (str): Display name of the template.
    - `description` (str): Description of the template.
    - `tactics` (list): List of MITRE tactics (if available).
    - `techniques` (list): List of MITRE techniques (if available).
    - ... (other available summary fields)
- If error, returns a dict with `error` (str).

## Example Output
```
[
  {
    "id": "/subscriptions/.../AlertRuleTemplates/abcde",
    "name": "TemplateName",
    "display_name": "Template Display Name",
    "description": "Detects ...",
    "tactics": ["collection", "exfiltration"],
    "techniques": ["T1005", "T1020"]
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
