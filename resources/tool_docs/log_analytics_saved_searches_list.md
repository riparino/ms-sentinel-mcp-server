# Log Analytics Saved Searches List

## Purpose

This tool retrieves a list of all saved searches in the current Log Analytics workspace. Saved searches are stored queries that can be reused and shared, and are often used for common monitoring scenarios or as the basis for alert rules in Microsoft Sentinel.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| None | | | This tool does not require any parameters |

## Output Fields

| Field | Type | Description |
|-------|------|-------------|
| savedSearches | Array | List of saved search objects |
| savedSearches[].id | String | Full resource ID of the saved search |
| savedSearches[].name | String | Name/identifier of the saved search |
| savedSearches[].type | String | Resource type (Microsoft.OperationalInsights/savedSearches) |
| count | Integer | Total number of saved searches returned |
| valid | Boolean | Indicates if the operation was successful |
| error | String | Error message if the operation failed (only present on error) |

## Example Request

```json
{
  "tool": "log_analytics_saved_searches_list"
}
```

## Example Response

```json
{
  "savedSearches": [
    {
      "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/savedSearches/LogManagement(<workspace-name>)_General|StaleComputers",
      "name": "LogManagement(<workspace-name>)_General|StaleComputers",
      "type": "Microsoft.OperationalInsights/savedSearches"
    },
    {
      "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/savedSearches/LogManagement(<workspace-name>)_General|dataTypeDistribution",
      "name": "LogManagement(<workspace-name>)_General|dataTypeDistribution",
      "type": "Microsoft.OperationalInsights/savedSearches"
    }
    // Additional saved searches...
  ],
  "count": 76,
  "valid": true
}
```

## Usage Notes

- This tool requires proper Azure authentication and permissions to access the Log Analytics workspace.
- The tool returns basic information about each saved search. To get detailed information about a specific saved search, use the `log_analytics_saved_search_get` tool with the saved search ID.
- The response may be large if there are many saved searches in the workspace.
- The saved searches are returned in the order provided by the Azure API.

## Error Cases

| Error | Description |
|-------|-------------|
| "Missing Azure SDK or workspace details." | The required Azure SDK modules are not available or workspace configuration is missing |
| "Azure LogAnalytics client initialization failed: {error}" | Failed to initialize the Azure LogAnalytics client |
| "Azure LogAnalytics client is not initialized" | The Azure LogAnalytics client could not be initialized |
| "Error retrieving saved searches: {error}" | An error occurred while retrieving saved searches from the Azure API |

## See Also

- [log_analytics_saved_search_get](log_analytics_saved_search_get.md) - Get details for a specific saved search
- [Azure Log Analytics Documentation](https://docs.microsoft.com/azure/azure-monitor/logs/log-analytics-overview)
