# Tool Docs Get Tool

**Tool Name:** `tool_docs_get`

## Overview
Returns the raw markdown content for a given documentation path in the `resources/tool_docs` directory.

## Parameters
- `path` (str, required): Relative path to the markdown doc (as returned by `tool_docs_list`).

## Output
- `content` (str): Raw markdown content of the file.
- If error, returns a dict with `error` (str) and may include `available_docs` (list[str]).

## Example Requests
### Get a specific documentation file
```
{
  "path": "sentinel_analytics_rule_get.md"
}
```

## Example Output
```
{
  "content": "# Sentinel Analytics Rule Get Tool\n\n**Tool Name:** `sentinel_analytics_rule_get`\n..."
}
```

## Error Handling
- Returns `error` if the file does not exist or is outside the docs directory.
- Returns `available_docs` if the requested file is missing, listing all available docs.

## MCP Compliance
- Inherits from `MCPToolBase`.
- Implements `async def run(self, ctx, **kwargs)`.
- Registered in `register_tools()`.
- Uses robust error handling.
