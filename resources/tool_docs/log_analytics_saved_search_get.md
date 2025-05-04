# Log Analytics Saved Search Get

## Purpose

This tool retrieves detailed information about a specific saved search in the Log Analytics workspace by its ID. Saved searches are stored queries that can be reused and shared, and are often used for common monitoring scenarios or as the basis for alert rules in Microsoft Sentinel.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| saved_search_id | String | Yes | The ID of the saved search to retrieve. This is the name portion of the saved search resource ID, such as "LogManagement(workspace-name)_General\|StaleComputers" |

## Output Fields

| Field | Type | Description |
|-------|------|-------------|
| savedSearch | Object | The saved search details |
| savedSearch.id | String | Full resource ID of the saved search |
| savedSearch.name | String | Name/identifier of the saved search |
| savedSearch.type | String | Resource type (Microsoft.OperationalInsights/savedSearches) |
| savedSearch.category | String | Category of the saved search (e.g., "General Exploration") |
| savedSearch.displayName | String | Human-readable name of the saved search |
| savedSearch.query | String | The KQL query text of the saved search |
| savedSearch.version | Integer | Version number of the saved search |
| savedSearch.functionAlias | String | Function alias if the saved search is published as a function (may be null) |
| valid | Boolean | Indicates if the operation was successful |
| error | String | Error message if the operation failed (only present on error) |

## Example Request

```json
{
  "tool": "log_analytics_saved_search_get",
  "saved_search_id": "LogManagement(workspace-name)_General|StaleComputers"
}
```

## Example Response

```json
{
  "savedSearch": {
    "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/savedSearches/LogManagement(<workspace-name>)_General|StaleComputers",
    "name": "LogManagement(<workspace-name>)_General|StaleComputers",
    "type": "Microsoft.OperationalInsights/savedSearches",
    "category": "General Exploration",
    "displayName": "Stale Computers (data older than 24 hours)",
    "query": "search not(ObjectName == \"Advisor Metrics\" or ObjectName == \"ManagedSpace\") | summarize lastdata = max(TimeGenerated) by Computer | limit 500000 | where lastdata < ago(24h)\r\n// Oql: NOT(ObjectName=\"Advisor Metrics\" OR ObjectName=ManagedSpace) | measure max(TimeGenerated) as lastdata by Computer | top 500000 | where lastdata < NOW-24HOURS",
    "version": 2
  },
  "valid": true
}
```

## Usage Notes

- This tool requires proper Azure authentication and permissions to access the Log Analytics workspace.
- The saved search ID is the name portion of the resource ID, not the full resource ID.
- To find available saved search IDs, use the `log_analytics_saved_searches_list` tool first.
- The response includes the full KQL query text, which can be used to understand or modify the saved search.
- Some fields may be null or missing depending on the saved search configuration.

## Error Cases

| Error | Description |
|-------|-------------|
| "saved_search_id parameter is required" | The required saved_search_id parameter was not provided |
| "Missing Azure SDK or workspace details." | The required Azure SDK modules are not available or workspace configuration is missing |
| "Azure LogAnalytics client initialization failed: {error}" | Failed to initialize the Azure LogAnalytics client |
| "Azure LogAnalytics client is not initialized" | The Azure LogAnalytics client could not be initialized |
| "Error retrieving saved search ID {saved_search_id}: {error}" | An error occurred while retrieving the saved search from the Azure API |

## See Also

- [log_analytics_saved_searches_list](log_analytics_saved_searches_list.md) - List all saved searches in a workspace
- [Azure Log Analytics Documentation](https://docs.microsoft.com/azure/azure-monitor/logs/log-analytics-overview)
