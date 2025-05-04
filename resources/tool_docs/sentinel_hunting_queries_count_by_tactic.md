# Sentinel Hunting Queries Count By Tactic Tool Documentation

## Purpose
Count Sentinel hunting queries (saved searches) by tactic.

## Parameters
| Name   | Type   | Required | Description                     |
|--------|--------|----------|---------------------------------|
| None   |        |          | This tool takes no parameters.  |

## Output Fields
| Name    | Type   | Description                                         |
|---------|--------|-----------------------------------------------------|
| valid   | bool   | True if the operation was successful                |
| error   | str    | Error message if any                                |
| results | dict   | Mapping of tactic name to count                     |
| errors  | list   | List of error messages                              |

## Example Request
```json
{
}
```

## Example Response
```json
{
  "valid": true,
  "error": null,
  "results": {
    "unknown": {
      "count": 76,
      "queries": [
        {"id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/savedSearches/<query-id>", "display_name": "SharePointFileOperation via devices with previously unseen user agents"},
        {"id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/savedSearches/<query-id>", "display_name": "Microsoft Sentinel Connectors Administrative Operations"}
      ]
    }
  },
  "errors": []
}
```

## Usage Notes
- Useful for reporting and dashboarding.

## Error Cases
- Azure API or credential errors

## See Also
- sentinel_hunting_queries_list
- sentinel_hunting_query_get
