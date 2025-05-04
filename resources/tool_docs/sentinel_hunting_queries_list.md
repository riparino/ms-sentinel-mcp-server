# Sentinel Hunting Queries List Tool Documentation

## Purpose
List all Sentinel hunting queries (saved searches) with optional tactic/technique filtering.

## Parameters
| Name         | Type   | Required | Description                                              |
|--------------|--------|----------|----------------------------------------------------------|
| tactic       | string | No       | Filter queries by tactic (case-insensitive, optional)    |
| technique    | string | No       | Filter queries by technique (case-insensitive, optional) |

## Output Fields
| Name    | Type   | Description                                         |
|---------|--------|-----------------------------------------------------|
| valid   | bool   | True if the operation was successful                |
| error   | str    | Error message if any                                |
| results | list   | List of hunting queries (dicts)                     |
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
  "results": [
    {
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
    {"id": "...", "name": "...", "display_name": "...", "category": "...", "query": "...", "tags": [], "tactics": [], "techniques": [], "description": null, "version": 2}
  ],
  "errors": []
}
```

## Usage Notes
- Filters are optional. Returns all queries if not specified.

## Error Cases
- Azure API or credential errors

## See Also
- sentinel_hunting_search
- sentinel_hunting_query_get
