# sentinel_watchlist_item_get

## Purpose
Retrieves detailed information about a specific item in a Microsoft Sentinel watchlist. This tool allows you to get the complete data for an individual watchlist item identified by both the watchlist alias and the item's unique identifier.

## Parameters
| Name             | Type   | Required | Description                                                      |
|------------------|--------|----------|------------------------------------------------------------------|
| watchlist_alias  | string | Yes      | The alias of the Sentinel watchlist containing the item.         |
| watchlist_item_id| string | Yes      | The unique identifier of the watchlist item to retrieve.         |
| kwargs           | dict   | No       | Additional parameters (for nested invocation compatibility).      |

## Output Fields
The tool returns a dictionary with the following structure:

| Key           | Type    | Description                                          |
|---------------|---------|------------------------------------------------------|
| watchlistItem | dict    | Detailed information about the requested item.       |
| valid         | boolean | Indicates if the operation completed successfully.   |
| error         | string  | Present only if an error occurred.                   |

### Example `watchlistItem` fields:
- id: Full Azure resource ID of the watchlist item
- name: Unique identifier of the watchlist item
- itemsKeyValue: Value of the primary key for this item
- properties: Key-value pairs containing the actual data of the watchlist item
- watchlistAlias: The alias of the watchlist the item belongs to

## Example Request
```
{
  "watchlist_alias": "hva",
  "watchlist_item_id": "d3e30fa7-8909-409e-87f8-d087731da067"
}
```

## Example Response
```
{
  "watchlistItem": {
    "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/Watchlists/hva/WatchlistItems/d3e30fa7-8909-409e-87f8-d087731da067",
    "name": "d3e30fa7-8909-409e-87f8-d087731da067",
    "itemsKeyValue": "server001",
    "properties": {
      "Hostname": "server001",
      "IPAddress": "10.0.0.1",
      "Owner": "IT Department",
      "Classification": "Critical"
    },
    "watchlistAlias": "hva"
  },
  "valid": true
}
```

## Usage Notes
- Returns detailed information about a specific watchlist item identified by its ID.
- Both the watchlist_alias and watchlist_item_id are case-sensitive and must exactly match the values in Sentinel.
- The properties field contains the actual data of the watchlist item as key-value pairs.
- Handles both MCP server and direct invocation (using environment variables for Azure context if needed).
- All errors are returned as a dict with an `error` key.

## Error Cases
- Missing or invalid `watchlist_alias` parameter.
- Missing or invalid `watchlist_item_id` parameter.
- Watchlist not found with the specified alias.
- Watchlist item not found with the specified ID.
- Azure SecurityInsights client initialization failure.
- Azure authentication errors.
- Insufficient permissions to access the watchlist item.
- Network or service connectivity issues.

## See Also
- [sentinel_watchlists_list](sentinel_watchlists_list.md) — for listing all watchlists.
- [sentinel_watchlist_get](sentinel_watchlist_get.md) — for retrieving a specific watchlist.
- [sentinel_watchlist_items_list](sentinel_watchlist_items_list.md) — for listing all items in a watchlist.
