# Sentinel Hunting Query Get Tool Documentation

## Purpose
Retrieve the full details of a Sentinel hunting query (saved search) by name or ID.

## Parameters
| Name     | Type   | Required | Description                                                    |
|----------|--------|----------|----------------------------------------------------------------|
| query_id | string | No       | The full resource ID or GUID of the saved search (optional)    |
| name     | string | No       | The display name or name of the saved search (optional)        |

## Output Fields
| Name        | Type   | Description                                         |
|-------------|--------|-----------------------------------------------------|
| valid       | bool   | True if the operation was successful                |
| error       | str    | Error message if any                                |
| results     | dict   | Full hunting query details if found                 |
| errors      | list   | List of error messages                              |

## Example Request
```json
{
  "query_id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/savedSearches/<query-id>"
}
```

## Example Response
```json
{
  "valid": true,
  "error": null,
  "results": {
    "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/savedSearches/<query-id>",
    "name": "0dd4c9dd-5d2c-4c2d-a0e5-eafeca5d9910",
    "display_name": "SharePointFileOperation via devices with previously unseen user agents",
    "category": "Hunt Queries",
    "query": "let starttime = todatetime('{{StartTimeISO}}'); ...",
    "tags": [
      {"name": "description", "value": "Tracking via user agent is one way ..."},
      {"name": "tactics", "value": "Exfiltration"},
      {"name": "techniques", "value": "T1030"}
    ],
    "tactics": ["Exfiltration"],
    "techniques": ["T1030"],
    "description": "Tracking via user agent is one way to differentiate ...",
    "version": 2
  },
  "errors": []
}
```

## Usage Notes
- At least one of `query_id` or `name` must be provided.
- Returns error if no match found.

## Error Cases
- Missing both query_id and name
- No matching query found
- Azure API or credential errors

## See Also
- sentinel_hunting_queries_list
- sentinel_hunting_search
