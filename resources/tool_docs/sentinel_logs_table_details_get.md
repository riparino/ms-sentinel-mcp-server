# Tool: sentinel_logs_table_details_get

## Purpose
Get details (metadata, retention, row count, etc.) for a Log Analytics table.

## Parameters
| Name       | Type | Required | Description                                 |
|------------|------|----------|---------------------------------------------|
| table_name | str  | Yes      | Name of the table to retrieve details for.  |

## Output Fields
| Name                     | Type   | Description                                |
|--------------------------|--------|--------------------------------------------|
| table                    | str    | Name of the table.                         |
| lastUpdated              | str    | ISO timestamp of last data update.         |
| rowCount                 | int    | Number of rows in the table.               |
| retentionInDays          | int    | Hot retention period (days).               |
| archiveRetentionInDays   | int    | Archive retention period (days), if present|
| totalRetentionInDays     | int    | Total retention period (days).             |
| plan                     | str    | Table plan (if available).                 |
| provisioningState        | str    | Provisioning state (if available).         |
| restoredLogs             | any    | Restored logs information (if available).  |
| tableSubType             | str    | Table subtype (if available).              |
| tableType                | str    | Table type (if available).                 |
| systemData               | any    | System data (if available).                |
| description              | str    | Table description (if available).          |
| isInherited              | bool   | If retention is inherited.                 |
| isTotalRetentionInherited| bool   | If total retention is inherited.           |
| errors                   | list   | List of error messages (if any).           |
| error                    | str    | Error message (optional, present if error occurred)|

## Example Request
```json
{
  "table_name": "SignInLogs"
}
```

## Example Response

### Typical Response (with available metadata)
```json
{
  "table": "AzureActivity",
  "lastUpdated": "2025-04-25T03:00:46.511607Z",
  "rowCount": 871,
  "retentionInDays": 90,
  "totalRetentionInDays": null,
  "archiveRetentionInDays": null,
  "plan": null,
  "provisioningState": null,
  "tableType": null,
  "description": null,
  "isInherited": null,
  "isTotalRetentionInherited": null
}
```

### Response with Errors
```json
{
  "table": "NonExistentTable",
  "retentionInDays": null,
  "totalRetentionInDays": null,
  "archiveRetentionInDays": null,
  "plan": null,
  "provisioningState": null,
  "tableType": null,
  "description": null,
  "isInherited": null,
  "isTotalRetentionInherited": null,
  "lastUpdated": null,
  "rowCount": 0,
  "errors": ["REST API: No data returned for table metadata.", "KQL error (lastUpdated): Table not found"]
}
```

## Usage Notes
- Combines KQL and REST API metadata for completeness.
- Returns all fields even if some are None.
- Uses direct REST API calls with API version 2017-04-26-preview for metadata retrieval.
- Retention information (retentionInDays) is typically available for most tables.
- Some metadata fields may be null depending on the table type and Azure environment configuration.

## Error Cases
| Error Message                                        | Cause                                       |
|----------------------------------------------------|---------------------------------------------|
| Missing required parameter: table_name               | Table name parameter is missing             |
| REST API: Missing required parameters...            | Missing Azure resource configuration        |
| REST API: No data returned for table metadata.      | API returned no data for the specified table|
| REST API: No properties found in table metadata...  | API response missing properties field       |
| REST API call error: ...                            | Error during REST API call                  |
| KQL error (lastUpdated): ...                        | Error querying for last updated timestamp   |
| KQL error (rowCount): ...                           | Error querying for row count                |
| KQL timeout: ...                                    | KQL query exceeded time limit               |

## See Also
- [sentinel_logs_tables_list.md](sentinel_logs_tables_list.md)
- [sentinel_logs_table_schema_get.md](sentinel_logs_table_schema_get.md)
