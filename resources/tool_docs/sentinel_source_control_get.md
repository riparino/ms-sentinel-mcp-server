# sentinel_source_control_get

**Description:**
Get details for a specific Sentinel source control by ID.

**Parameters:**
- `source_control_id` (str, required): The ID of the source control to retrieve.

**Output:**
```
{
  "source_control": {
    "id": "<source-control-id>",
    "name": "<source-control-name>",
    "description": "<description>"
    // ...additional fields depending on Azure API
  },
  "valid": true|false,
  "errors": [<error-messages>],
  "error": "<error-message-if-any>"
}
```

**Error Handling:**
If the ID is invalid or any error occurs, the output includes an `error` key and a descriptive message. The `errors` list will contain error messages, if any.

**Azure Context Fallback:**
Supports both MCP server and direct invocation. Falls back to environment variables if MCP context is unavailable.

**Example Usage:**
```json
{
  "tool": "sentinel_source_control_get",
  "kwargs": {"source_control_id": "<source-control-id>"}
}
```

**Example Response (invalid ID):**
```json
{
  "source_control": {},
  "valid": false,
  "errors": [
    "Error retrieving source control: (BadRequest) The value '<source-control-id>' is not valid.\nCode: BadRequest\nMessage: The value '<source-control-id>' is not valid."
  ],
  "error": "Error retrieving source control: (BadRequest) The value '<source-control-id>' is not valid.\nCode: BadRequest\nMessage: The value '<source-control-id>' is not valid."
}
```
{
  "tool": "sentinel_source_control_get",
  "kwargs": {"source_control_id": "<source-control-id>"}
}
```
