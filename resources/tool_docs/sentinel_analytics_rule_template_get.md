# Sentinel Analytics Rule Template Get Tool

**Tool Name:** `sentinel_analytics_rule_template_get`

## Overview
Retrieves details for a specific Microsoft Sentinel analytics rule template by its ID or name.

## Parameters
- `id` (str, required): The full resource ID or unique name of the analytics rule template.

## Output
- Dict containing all available fields for the template, e.g.:
    - `id` (str): Template ID.
    - `name` (str): Template name.
    - `display_name` (str): Display name.
    - `description` (str): Description.
    - `tactics` (list): List of MITRE tactics (if available).
    - `techniques` (list): List of MITRE techniques (if available).
    - ... (all other template properties)
- If error, returns a dict with `error` (str).

## Example Output
```
{
  "id": "/subscriptions/.../AlertRuleTemplates/abcde",
  "name": "TemplateName",
  "display_name": "Template Display Name",
  "description": "Detects ...",
  "tactics": ["collection", "exfiltration"],
  "techniques": ["T1005", "T1020"]
  ...
}
```

## Error Handling
- Returns `error` field if context is missing, template not found, or SDK/API errors occur.

## MCP Compliance
- Inherits from `MCPToolBase`.
- Implements `async def run(self, ctx, **kwargs)`.
- Registered in `register_tools()`.
- Uses robust Azure context extraction and error handling.
