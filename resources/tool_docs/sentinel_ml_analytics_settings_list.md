# sentinel_ml_analytics_settings_list

**Description:**
List all Sentinel ML analytics settings in the current workspace.

**Parameters:**
_None required. Context is extracted from MCP server or environment variables._

**Output:**
```
{
  "settings": [
    {
      "id": "<setting-id>",
      "name": "<setting-name>",
      "description": "<description>",
      "enabled": true|false
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
  "tool": "sentinel_ml_analytics_settings_list",
  "kwargs": {}
}
```

**Example Response:**
```json
{
  "settings": [
    {
      "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/securityMLAnalyticsSettings/<setting-guid>",
      "name": "b40a7a5b-5d39-46fe-a79e-2acdb38e1ce7",
      "description": "This algorithm detects an unusually high volume of AWS cloud trail log console failed login events per group user account within the last day. The model is trained on the previous 21 days of AWS cloud trail log events on group user account basis. This activity may indicate that the account is compromised.",
      "enabled": true
    },
    {
      "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/securityMLAnalyticsSettings/<setting-guid>",
      "name": "29094df8-e0c7-4475-a74c-bda74a07affb",
      "description": "This algorithm detects an unusually high volume of successful logins per user account by different logon types. The model is trained on the previous 21 days of security event ID 4624 on an account. It indicates anomalous high volume of successful logins in the last day.",
      "enabled": true
    }
    // ...more settings
  ],
  "valid": true,
  "errors": [],
  "error": null
}
```
{
  "tool": "sentinel_ml_analytics_settings_list",
  "kwargs": {}
}
```
