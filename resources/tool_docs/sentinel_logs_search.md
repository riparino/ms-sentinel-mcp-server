# Sentinel Logs Search Tool Documentation

## Purpose
Runs a KQL query against Azure Monitor Logs (Log Analytics workspace) and returns structured results. Supports both MCP server and direct invocation for integration testing.

---

## Parameters
| Name        | Type   | Required | Description                                                         |
|-------------|--------|----------|---------------------------------------------------------------------|
| query       | string | Yes      | The Kusto Query Language (KQL) query to run.                        |
| timespan    | string | No       | Time window for the query (e.g., '1d', '12h', '30m'). Default: '1d' |

---

## Output Fields
| Name               | Type     | Description                                                                                 |
|--------------------|----------|---------------------------------------------------------------------------------------------|
| valid              | bool     | True if the query ran successfully, False otherwise.                                         |
| errors             | list     | List of error messages (empty if none).                                                      |
| error              | string   | Single error message (empty if none).                                                        |
| query              | string   | The KQL query that was executed.                                                             |
| timespan           | string   | The timespan used for the query.                                                             |
| result_count       | int      | Number of rows returned.                                                                     |
| columns            | list     | List of dicts describing columns: name, type, ordinal.                                       |
| rows               | list     | List of result rows (each is a dict mapping column name to value).                           |
| execution_time_ms  | int      | Query execution time in milliseconds.                                                        |
| warnings           | list     | List of warning messages (e.g., for large result sets).                                      |
| message            | string   | Human-readable status message.                                                                |

---

## Example Request
```
{
  "query": "Heartbeat | take 5"
}
```

---

## Example Response
```
{
  "valid": true,
  "errors": [],
  "query": "Heartbeat | take 5",
  "timespan": "1d",
  "result_count": 0,
  "columns": [
    {"name": "TenantId", "type": "string", "ordinal": 0},
    {"name": "SourceSystem", "type": "string", "ordinal": 1},
    {"name": "TimeGenerated", "type": "string", "ordinal": 2},
    ...
  ],
  "rows": [],
  "execution_time_ms": 1099,
  "warnings": [],
  "message": "Query executed successfully"
}
```

---

## Usage Notes
- The tool supports any valid KQL query against the configured Log Analytics workspace.
- If no results are returned, `rows` will be an empty list but `columns` will describe the expected schema.
- If the query requests a large result set (e.g., `take 10000`), a warning will be included in `warnings`.
- Timespan defaults to '1d' if not specified.

---

## Error Cases
| Error Message                                              | When it Occurs                                                    |
|-----------------------------------------------------------|-------------------------------------------------------------------|
| Missing required parameter: query                         | The `query` parameter was not provided.                           |
| Azure Monitor Logs client or workspace_id is not initialized. Check your credentials and configuration. | Azure credentials or workspace info missing or invalid.           |
| Query timed out after 60 seconds                          | The query did not complete within the timeout window.              |
| Error executing query: <details>                          | Any other unexpected error during query execution.                 |

---

## See Also
- [sentinel_query_validate.md](sentinel_query_validate.md)
- [Azure Monitor KQL documentation](https://docs.microsoft.com/azure/azure-monitor/logs/query-language)

---

*This documentation uses only fictional or placeholder values and never exposes real workspace or credential details.*
