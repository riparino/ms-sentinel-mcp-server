# sentinel_watchlist_get

## Purpose
Retrieves detailed information about a specific Microsoft Sentinel watchlist by its alias. Provides comprehensive metadata about the watchlist including its properties, creation time, and item count.

## Parameters
| Name           | Type   | Required | Description                                                      |
|----------------|--------|----------|------------------------------------------------------------------|
| watchlist_alias| string | Yes      | The alias of the Sentinel watchlist to retrieve.                 |
| kwargs         | dict   | No       | Additional parameters (for nested invocation compatibility).      |

## Output Fields
The tool returns a dictionary with the following structure:

| Key       | Type    | Description                                          |
|-----------|---------|------------------------------------------------------|
| watchlist | dict    | Detailed information about the requested watchlist.  |
| valid     | boolean | Indicates if the operation completed successfully.   |
| error     | string  | Present only if an error occurred.                   |

### Example `watchlist` fields:
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
{
  "watchlist_alias": "hva"
}
```

## Example Response
```
{
  "watchlist": {
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
  },
  "valid": true
}
```

## Usage Notes
- Returns detailed information about a specific watchlist identified by its alias.
- The watchlist_alias is case-sensitive and must exactly match the alias in Sentinel.
- Handles both MCP server and direct invocation (using environment variables for Azure context if needed).
- All errors are returned as a dict with an `error` key.

## Error Cases
- Missing or invalid `watchlist_alias` parameter.
- Watchlist not found with the specified alias.
- Azure SecurityInsights client initialization failure.
- Azure authentication errors.
- Insufficient permissions to access the watchlist.
- Network or service connectivity issues.

## See Also
- [sentinel_watchlists_list](sentinel_watchlists_list.md) — for listing all watchlists.
- [sentinel_watchlist_items_list](sentinel_watchlist_items_list.md) — for listing items in a watchlist.
