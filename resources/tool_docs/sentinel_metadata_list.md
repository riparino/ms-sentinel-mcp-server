# sentinel_metadata_list

**Description:**
List all Sentinel metadata in the current workspace.

**Parameters:**
_None required. Context is extracted from MCP server or environment variables._

**Output:**
```
{
  "metadata": [
    {
      "id": "<metadata-id>",
      "name": "<metadata-name>",
      "kind": "<kind>",
      "content_id": "<content-id>",
      "version": "<version>",
      "parent_id": "<parent-id>",
      "author": { /* author object */ },
      "source": { /* source object */ },
      "support": { /* support object */ },
      "categories": null,
      "dependencies": null,
      "created": "<timestamp>",
      "last_modified": "<timestamp>"
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
  "tool": "sentinel_metadata_list",
  "kwargs": {}
}
```

**Example Response:**
```json
{
  "metadata": [
    {
      "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/metadata/analyticsrule-<guid>",
      "name": "analyticsrule-<guid>",
      "kind": "AnalyticsRule",
      "content_id": "<content-id>",
      "version": "2.0.4",
      "parent_id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/alertRules/<guid>",
      "author": "<author-object>",
      "source": "<source-object>",
      "support": "<support-object>",
      "categories": null,
      "dependencies": null,
      "created": "",
      "last_modified": ""
    },
    {
      "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/metadata/huntingquery-<guid>",
      "name": "huntingquery-<guid>",
      "kind": "HuntingQuery",
      "content_id": "<content-id>",
      "version": "2.0.1",
      "parent_id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/savedSearches/<guid>",
      "author": "<author-object>",
      "source": "<source-object>",
      "support": "<support-object>",
      "categories": null,
      "dependencies": null,
      "created": "",
      "last_modified": ""
    }
    // ...more metadata items
  ],
  "valid": true,
  "errors": [],
  "error": null
}
```
{
  "tool": "sentinel_metadata_list",
  "kwargs": {}
}
```
