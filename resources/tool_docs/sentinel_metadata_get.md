# sentinel_metadata_get

**Description:**
Get details for specific Sentinel metadata by ID.

**Parameters:**
- `metadata_id` (str, required): The ID or short name of the metadata object to retrieve (can be either the full ARM resource ID or just the short name, e.g., `analyticsrule-<guid>`).

**Output:**
```json
{
  "metadata": {
    "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/metadata/analyticsrule-<guid>",
    "name": "analyticsrule-<guid>",
    "kind": "AnalyticsRule",
    "content_id": "<content-id>",
    "version": "2.0.4",
    "parent_id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/alertRules/<guid>",
    "author": {
      "name": "Microsoft",
      "email": "support@microsoft.com"
    },
    "source": {
      "kind": "Solution",
      "name": "Microsoft 365",
      "source_id": "azuresentinel.azure-sentinel-solution-office365"
    },
    "support": {
      "tier": "Microsoft",
      "name": "Microsoft Corporation",
      "email": "support@microsoft.com",
      "link": "https://support.microsoft.com/"
    },
    "categories": null,
    "dependencies": null,
    "created": "",
    "last_modified": ""
  },
  "valid": true,
  "errors": []
}
```

**Error Handling:**
If the metadata ID is invalid or not found, the output will look like:
```json
{
  "metadata": {},
  "valid": false,
  "errors": ["Error retrieving metadata: Operation returned an invalid status 'Not Found'"],
  "error": "Error retrieving metadata: Operation returned an invalid status 'Not Found'"
}
```


**Error Handling:**
If the ID is invalid or any error occurs, the output includes an `error` key and a descriptive message. The `errors` list will contain error messages, if any.

**Azure Context Fallback:**
Supports both MCP server and direct invocation. Falls back to environment variables if MCP context is unavailable.

**Example Usage:**
Request with short name:
```json
{
  "tool": "sentinel_metadata_get",
  "kwargs": {"metadata_id": "analyticsrule-<guid>"}
}
```
Request with full ARM resource ID:
```json
{
  "tool": "sentinel_metadata_get",
  "kwargs": {"metadata_id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/metadata/analyticsrule-<guid>"}
}
```

**Example Response:**
```json
{
  "metadata": {
    "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/metadata/analyticsrule-<guid>",
    "name": "analyticsrule-<guid>",
    "kind": "AnalyticsRule",
    "content_id": "<content-id>",
    "version": "2.0.4",
    "parent_id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/alertRules/<guid>",
    "author": {
      "name": "Microsoft",
      "email": "support@microsoft.com"
    },
    "source": {
      "kind": "Solution",
      "name": "Microsoft 365",
      "source_id": "azuresentinel.azure-sentinel-solution-office365"
    },
    "support": {
      "tier": "Microsoft",
      "name": "Microsoft Corporation",
      "email": "support@microsoft.com",
      "link": "https://support.microsoft.com/"
    },
    "categories": null,
    "dependencies": null,
    "created": "",
    "last_modified": ""
  },
  "valid": true,
  "errors": []
}
```

**Example Error Response:**
```json
{
  "metadata": {},
  "valid": false,
  "errors": ["Error retrieving metadata: Operation returned an invalid status 'Not Found'"],
  "error": "Error retrieving metadata: Operation returned an invalid status 'Not Found'"
}
```
