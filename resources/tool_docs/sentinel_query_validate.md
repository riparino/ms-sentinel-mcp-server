# Tool: sentinel_query_validate (KQLValidateTool)

## Purpose
Validates the syntax of a provided KQL (Kusto Query Language) query string locally, without executing it against a workspace. This tool is used to check for KQL syntax errors before attempting to run a query in Microsoft Sentinel or Log Analytics.

## Parameters
| Name       | Type   | Required | Description                                                      |
|------------|--------|----------|------------------------------------------------------------------|
| query      | string | Yes      | The KQL query string to validate.                                |

- The parameter can be provided directly as `query` or nested within a `kwargs` dictionary for compatibility with various invocation patterns.

## Output Fields
| Name    | Type    | Description                                                                 |
|---------|---------|-----------------------------------------------------------------------------|
| valid   | bool    | True if the KQL syntax is valid; False otherwise.                            |
| errors  | list    | List of error messages if validation fails; empty if valid.                   |
| result  | string  | Success message if valid, omitted if invalid.                                |
| error   | string  | Error message if validation fails or if a required parameter is missing.      |

## Example Requests and Responses

### 1. Simple Filter Query
**Request:**
```json
{
  "query": "SecurityEvent | where EventID == 4625"
}
```
**Response:**
```json
{
  "result": "Query validation passed. The KQL syntax appears to be correct.",
  "valid": true,
  "errors": []
}
```

### 2. Aggregation by Account and Hour
**Request:**
```json
{
  "query": "SecurityEvent | where EventID = 4625 | summarize Count=count() by Account, bin(TimeGenerated, 1h)"
}
```
**Response:**
```json
{
  "result": "Query validation passed. The KQL syntax appears to be correct.",
  "valid": true,
  "errors": []
}
```

### 3. Multi-step Aggregation and Projection
**Request:**
```json
{
  "query": "SecurityEvent | summarize Count=count() by Account, bin(TimeGenerated, 1h) | where Count > 10 | project Account, Count, TimeGenerated"
}
```
**Response:**
```json
{
  "result": "Query validation passed. The KQL syntax appears to be correct.",
  "valid": true,
  "errors": []
}
```

### 4. Query with Syntax Error (Missing Parenthesis)
**Request:**
```json
{
  "query": "SecurityEvent | where EventID = 4625 | summarize Count=count() by Account, bin(TimeGenerated, 1h | project Account, Count, TimeGenerated"
}
```
**Response:**
```json
{
  "error": "KQL validation failed:\nUnknown position: Expected: )",
  "valid": false,
  "errors": ["Unknown position: Expected: )"]
}
```

## Usage Notes
- This tool does not execute the query or check for schema correctness; it only validates KQL syntax.
- If the required parameter `query` is missing, the tool returns an error and sets `valid` to false.
- Supports both MCP server and direct invocation (integration tests).
- The tool leverages the local `utilities.kql_validator.validate_kql` function for validation logic.

## Error Cases
| Error Condition                | Error Message                                         |
|-------------------------------|------------------------------------------------------|
| Missing query                  | "Missing required parameter: query"                  |
| KQL validation unavailable     | "KQL validation unavailable" (from validator errors) |
| General exception              | "An error occurred while validating the query..."    |

## See Also

- [sentinel_logs_search](sentinel_logs_table_get.md): Executes KQL queries against Log Analytics tables.

---

_This documentation follows the MCP tool documentation template as required by project architecture guidelines._
