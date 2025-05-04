# Tool: sentinel_logs_table_schema_get

## Purpose
Get schema (columns/types) for a Log Analytics table.

## Parameters
| Name      | Type | Required | Description                                   |
|-----------|------|----------|-----------------------------------------------|
| table     | str  | Yes      | Name of the table to retrieve schema for.     |

## Output Fields
| Name   | Type | Description                                        |
|--------|------|----------------------------------------------------|
| table  | str  | Name of the table.                                 |
| schema | list | List of columns with keys: name (str), type (str)  |
| error  | str  | Error message (optional, present if error occurred)|

## Example Request
```json
{
  "table": "SignInLogs"
}
```

## Example Response
```json
{
  "table": "SignInLogs",
  "schema": [
    { "name": "TimeGenerated", "type": "datetime" },
    { "name": "UserPrincipalName", "type": "string" },
    { "name": "AppDisplayName", "type": "string" },
    { "name": "IPAddress", "type": "string" },
    { "name": "ResultType", "type": "int" }
  ]
}
```

## Usage Notes
- Returns all columns and their types for the specified table.
- Uses KQL to fetch schema.

## Error Cases
| Error Message                    | Cause                        |
|----------------------------------|------------------------------|
| Table name is required.          | Missing required parameter   |
| KQL error: ...                   | KQL query failed             |
| REST API client error: ...       | REST API call failed         |

## See Also
- [sentinel_logs_tables_list.md](sentinel_logs_tables_list.md)
- [sentinel_logs_table_details_get.md](sentinel_logs_table_details_get.md)
