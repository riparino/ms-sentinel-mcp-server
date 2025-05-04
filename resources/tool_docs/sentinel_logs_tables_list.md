# Tool: sentinel_logs_tables_list

## Purpose
List available tables in the Log Analytics workspace.

## Parameters
| Name           | Type   | Required | Description                                                    |
|----------------|--------|----------|----------------------------------------------------------------|
| filter_pattern | str    | No       | Pattern to filter table names (case-insensitive substring).    |

## Output Fields
| Name         | Type   | Description                                                      |
|--------------|--------|------------------------------------------------------------------|
| found        | int    | Number of tables found.                                          |
| tables       | list   | List of tables with keys: name (str), lastUpdated (str), rowCount (int) |
| error        | str    | Error message (optional, present if an error occurred).           |

## Example Request
```json
{
  "filter_pattern": "SignIn"
}
```

## Example Response
```json
{
  "found": 2,
  "tables": [
    { "name": "SignInLogs", "lastUpdated": "2025-04-22T14:53:00Z", "rowCount": 485120 },
    { "name": "SignInSummary", "lastUpdated": "2025-04-22T14:50:00Z", "rowCount": 12480 }
  ]
}
```

## Usage Notes
- Returns all tables if `filter_pattern` is not provided.
- Uses KQL and REST API for comprehensive table info.
- Caches results for performance.

## Error Cases
| Error Message                                               | Cause                                      |
|------------------------------------------------------------|--------------------------------------------|
| Azure Logs client is not initialized. Check your credentials and configuration. | Credentials or config missing/invalid       |
| No tables found.                                           | No tables exist or filter excludes all      |
| KQL error: ...                                             | KQL query failed                           |
| REST API client error: ...                                 | REST API call failed                       |

## See Also
- [sentinel_logs_table_schema_get.md](sentinel_logs_table_schema_get.md)
- [sentinel_logs_table_details_get.md](sentinel_logs_table_details_get.md)
