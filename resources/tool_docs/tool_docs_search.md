# Tool Docs Search Tool

**Tool Name:** `tool_docs_search`

## Overview
Performs a full-text search across documentation in the `resources/tool_docs` directory and returns matching paths.

## Parameters
- `query` (str, required): Regex or text to search for in docs.
- `k` (int, optional): Max number of results to return (default: 10).

## Output
- `hits` (list[str]): Relative doc paths containing a match.
- If error, returns a dict with `error` (str).

## Example Requests
### Search for docs containing the word "analytics"
```
{
  "query": "analytics"
}
```

### Search for docs containing the word "incident" (limit 2 results)
```
{
  "query": "incident",
  "k": 2
}
```

## Example Output
```
{
  "hits": [
    "sentinel_analytics_rule_get.md",
    "sentinel_analytics_rule_list.md"
  ]
}
```

## Error Handling
- Returns `error` if the search fails or required parameters are missing.

## MCP Compliance
- Inherits from `MCPToolBase`.
- Implements `async def run(self, ctx, **kwargs)`.
- Registered in `register_tools()`.
- Uses robust error handling.
