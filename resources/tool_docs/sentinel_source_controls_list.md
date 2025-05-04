# sentinel_source_controls_list

**Description:**
List all Sentinel source controls in the current workspace.

**Parameters:**
_None required. Context is extracted from MCP server or environment variables._

**Output:**
```
{
  "source_controls": [
    {
      "id": "<source-control-id>",
      "name": "<source-control-name>",
      "description": "<description>"
      // ...additional fields depending on Azure API
    }
  ],
  "valid": true,
  "errors": [],
  "error": "<error-message-if-any>"
}
```

**Error Handling:**
If any error occurs, the output includes an `error` key and a descriptive message. The `errors` list will contain error messages, if any.

**Azure Context Fallback:**
Supports both MCP server and direct invocation. Falls back to environment variables if MCP context is unavailable.

**Example Usage:**
```json
{
  "tool": "sentinel_source_controls_list",
  "kwargs": {}
}
```

**Example Response:**
```json
{
  "source_controls": [],
  "valid": true,
  "errors": [],
  "error": null
}
```
{
  "tool": "sentinel_source_controls_list",
  "kwargs": {}
}
```
