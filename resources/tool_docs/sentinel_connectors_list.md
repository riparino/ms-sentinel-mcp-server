# SentinelConnectorsListTool

## Purpose
List all data connectors in an Azure Sentinel workspace using the Azure Security Insights API. Supports both MCP server context and direct invocation (with environment variable fallback).

## Parameters
| Name            | Type   | Required | Description                                             |
|-----------------|--------|----------|---------------------------------------------------------|
| kwargs          | dict   | Yes      | Additional parameters (not used for this tool)          |

## Output Fields
| Name        | Type   | Description                                                                 |
|-------------|--------|-----------------------------------------------------------------------------|
| count       | int    | The number of data connectors returned.                                      |
| connectors  | list   | List of connector objects (see below).                                       |
| note        | str    | Warning about Azure API limitations.                                         |
| error       | str    | Error message, if applicable.                                               |

### Connector Object
| Name   | Type   | Description                 |
|--------|--------|-----------------------------|
| name   | str    | Name of the connector       |
| kind   | str    | Connector kind/type         |
| id     | str    | Azure resource ID           |
| etag   | str    | ETag                        |
| type   | str    | Azure resource type         |

## Example Request
```json
{
  "kwargs": {}
}
```

## Example Response
```json
{
  "count": 2,
  "connectors": [
    {"name": "MyConnector", "kind": "AzureActiveDirectory", "id": "/subscriptions/...", "etag": "...", "type": "Microsoft.OperationalInsights/workspaces/dataConnectors"},
    {"name": "OtherConnector", "kind": "ThreatIntelligence", "id": "/subscriptions/...", "etag": "...", "type": "Microsoft.OperationalInsights/workspaces/dataConnectors"}
  ],
  "note": "⚠️ Connector list may be incomplete. Built-in and gallery-deployed connectors are not included due to Azure API limitations. Manual verification recommended."
}
```

## Usage Notes
- Requires Azure Security Insights API permissions.
- Built-in and gallery connectors may not be listed due to API limitations.
- Supports both MCP server context and direct invocation for integration tests.

## Error Cases
| Error Message                                             | Meaning                                    |
|----------------------------------------------------------|--------------------------------------------|
| "Azure Security Insights SDK is not available."          | Required SDK is not installed.             |
| "Workspace name is not configured..."                    | Workspace name missing in context/env.      |
| "Security Insights client is not initialized..."         | Client construction failed.                |
| "Error listing data connectors: ..."                     | Exception occurred during API call.        |

## See Also
- [sentinel_connectors_get.md](sentinel_connectors_get.md)
- [Official Azure Docs](https://learn.microsoft.com/en-us/azure/sentinel/connect-data-sources)
