# sentinel_watchlists_list

## Purpose
Lists all Microsoft Sentinel watchlists in the current workspace. Watchlists are user-created tables that can be used to store data for lookups and enrichment in Sentinel queries, analytics rules, and hunting.

## Parameters
| Name   | Type | Required | Description                                                 |
|--------|------|----------|-------------------------------------------------------------|
| kwargs | dict | No       | Additional parameters (for nested invocation compatibility). |

## Output Fields
The tool returns a dictionary with the following structure:

| Key       | Type    | Description                                          |
|-----------|---------|------------------------------------------------------|
| watchlists| list    | List of watchlist objects with their metadata.       |
| count     | integer | The number of watchlists returned.                   |
| valid     | boolean | Indicates if the operation completed successfully.   |
| error     | string  | Present only if an error occurred.                   |

### Example `watchlists` fields:
- id: Full Azure resource ID of the watchlist
- name: Name of the watchlist
- alias: Alias used to reference the watchlist
- displayName: User-friendly display name of the watchlist
- description: Description of the watchlist's purpose
- provider: Provider of the watchlist (e.g., "Microsoft")
- source: Source of the watchlist data (e.g., "Local file")
- itemsSearchKey: Primary key column for the watchlist items
- created: Creation timestamp
- updated: Last update timestamp
- itemsCount: Number of items in the watchlist

## Example Request
```
{}
```

## Example Response
```
{
  "watchlists": [
    {
      "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/Watchlists/hva",
      "name": "hva",
      "alias": "hva",
      "displayName": "High Value Assets",
      "description": "List of high value assets in the organization",
      "provider": "Microsoft",
      "source": "Local file",
      "itemsSearchKey": "Hostname",
      "created": "2025-04-20T08:15:30.422179Z",
      "updated": "2025-04-20T08:15:30.422179Z",
      "itemsCount": 10
    }
  ],
  "count": 1,
  "valid": true
}
```

## Usage Notes
- Returns all watchlists in the current Microsoft Sentinel workspace.
- The response includes basic metadata about each watchlist.
- If no watchlists exist, returns an empty list with count 0.
- Handles both MCP server and direct invocation (using environment variables for Azure context if needed).
- All errors are returned as a dict with an `error` key.

## Error Cases
- Azure SecurityInsights client initialization failure.
- Azure authentication errors.
- Insufficient permissions to access watchlists.
- Network or service connectivity issues.

## See Also
- [sentinel_watchlist_get](sentinel_watchlist_get.md) — for retrieving a specific watchlist.
- [sentinel_watchlist_items_list](sentinel_watchlist_items_list.md) — for listing items in a watchlist.
