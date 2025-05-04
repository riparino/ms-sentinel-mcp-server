# sentinel_watchlist_items_list

## Purpose
Lists all items in a specific Microsoft Sentinel watchlist identified by its alias. Watchlist items are individual records stored in a watchlist that can be used for lookups and enrichment in Sentinel queries, analytics rules, and hunting.

## Parameters
| Name           | Type   | Required | Description                                                      |
|----------------|--------|----------|------------------------------------------------------------------|
| watchlist_alias| string | Yes      | The alias of the Sentinel watchlist to retrieve items from.      |
| kwargs         | dict   | No       | Additional parameters (for nested invocation compatibility).      |

## Output Fields
The tool returns a dictionary with the following structure:

| Key           | Type    | Description                                          |
|---------------|---------|------------------------------------------------------|
| watchlistItems| list    | List of watchlist item objects with their data.      |
| count         | integer | The number of watchlist items returned.              |
| watchlistAlias| string  | The alias of the watchlist the items belong to.      |
| valid         | boolean | Indicates if the operation completed successfully.   |
| error         | string  | Present only if an error occurred.                   |

### Example `watchlistItems` fields:
- id: Full Azure resource ID of the watchlist item
- name: Unique identifier of the watchlist item
- itemsKeyValue: Value of the primary key for this item
- properties: Key-value pairs containing the actual data of the watchlist item

## Example Request
```
{
  "watchlist_alias": "hva"
}
```

## Example Response
```
{
  "watchlistItems": [
    {
      "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/Watchlists/hva/WatchlistItems/<item-id>",
      "name": "<item-id>",
      "itemsKeyValue": "server001",
      "properties": {
        "Hostname": "server001",
        "IPAddress": "10.0.0.1",
        "Owner": "IT Department",
        "Classification": "Critical"
      }
    },
    {
      "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/Watchlists/hva/WatchlistItems/<item-id>",
      "name": "<item-id>",
      "itemsKeyValue": "server002",
      "properties": {
        "Hostname": "server002",
        "IPAddress": "10.0.0.2",
        "Owner": "Finance Department",
        "Classification": "High"
      }
    }
  ],
  "count": 2,
  "watchlistAlias": "hva",
  "valid": true
}
```

## Usage Notes
- Returns all items in a specific watchlist identified by its alias.
- The watchlist_alias is case-sensitive and must exactly match the alias in Sentinel.
- The properties field contains the actual data of the watchlist item as key-value pairs.
- If no items exist in the watchlist, returns an empty list with count 0.
- Handles both MCP server and direct invocation (using environment variables for Azure context if needed).
- All errors are returned as a dict with an `error` key.

## Error Cases
- Missing or invalid `watchlist_alias` parameter.
- Watchlist not found with the specified alias.
- Azure SecurityInsights client initialization failure.
- Azure authentication errors.
- Insufficient permissions to access the watchlist items.
- Network or service connectivity issues.

## See Also
- [sentinel_watchlists_list](sentinel_watchlists_list.md) — for listing all watchlists.
- [sentinel_watchlist_get](sentinel_watchlist_get.md) — for retrieving a specific watchlist.
- [sentinel_watchlist_item_get](sentinel_watchlist_item_get.md) — for retrieving a specific watchlist item.
