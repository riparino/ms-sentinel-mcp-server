# SentinelConnectorsGetTool

## Purpose
Retrieve a specific Azure Sentinel data connector by its ID. Supports both MCP server context and direct invocation (with environment variable fallback).

## Parameters
| Name             | Type   | Required | Description                                    |
|------------------|--------|----------|------------------------------------------------|
| data_connector_id| str    | Yes      | The Azure resource ID of the data connector    |
| kwargs           | dict   | No       | Additional parameters (not used for this tool) |

## Output Fields
| Name        | Type   | Description                                                                 |
|-------------|--------|-----------------------------------------------------------------------------|
| name        | str    | Name of the connector                                                       |
| type        | str    | Azure resource type                                                         |
| kind        | str    | Connector kind/type                                                         |
| id          | str    | Azure resource ID                                                           |
| etag        | str    | ETag                                                                        |
| properties  | dict   | Additional connector properties                                             |
| error       | str    | Error message, if applicable                                                |

## Example Request
```json
{
  "data_connector_id": "/subscriptions/.../dataConnectors/abcd1234"
}
```

## Example Response
```json
{
  "name": "MyConnector",
  "type": "Microsoft.OperationalInsights/workspaces/dataConnectors",
  "kind": "AzureActiveDirectory",
  "id": "/subscriptions/.../dataConnectors/abcd1234",
  "etag": "...",
  "properties": {"tenantId": "...", ...}
}
```

## Usage Notes
- Requires Azure Security Insights API permissions.
- The `data_connector_id` parameter must be a valid Azure resource ID.
- Supports both MCP server context and direct invocation for integration tests.

## Error Cases
| Error Message                                   | Meaning                                    |
|------------------------------------------------|--------------------------------------------|
| "Azure Security Insights SDK is not available."| Required SDK is not installed.             |
| "Missing required parameter: data_connector_id" | The required parameter was not provided.    |
| "Workspace name is not configured..."           | Workspace name missing in context/env.      |
| "Security Insights client is not initialized..."| Client construction failed.                |
| "Error getting data connector: ..."             | Exception occurred during API call.        |

## See Also
- [sentinel_connectors_list.md](sentinel_connectors_list.md)
- [Official Azure Docs](https://learn.microsoft.com/en-us/azure/sentinel/connect-data-sources)
