# Tool Docs List Tool

**Tool Name:** `tool_docs_list`

## Overview
Enumerates available Sentinel server documentation markdown paths in the `resources/tool_docs` directory.

## Parameters
- `prefix` (str, optional): Only include docs whose relative path starts with this prefix.

## Output
- `paths` (list[str]): List of relative markdown doc paths.
- If error, returns a dict with `error` (str).

## Example Requests
### List all documentation files
```
{
  "prefix": ""
}
```

### List documentation files starting with a specific prefix
```
{
  "prefix": "sentinel_analytics"
}
```

## Example Output
```
{
  "paths": [
    "sentinel_analytics_rule_get.md",
    "sentinel_analytics_rule_list.md",
    "sentinel_analytics_rules_count_by_tactic.md"
  ]
}
```

## Error Handling
- Returns `error` field if the docs directory cannot be read or other errors occur.

## MCP Compliance
- Inherits from `MCPToolBase`.
- Implements `async def run(self, ctx, **kwargs)`.
- Registered in `register_tools()`.
- Uses robust error handling.
