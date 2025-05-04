# sentinel_workspace_get

## Purpose
Get detailed information about the current Sentinel Log Analytics workspace, including workspace name, resource group, subscription ID, and workspace properties. Returns additional guidance for related data connectors and analytics rules.

## Parameters
| Name                | Type   | Required | Description                                                                 |
|---------------------|--------|----------|-----------------------------------------------------------------------------|
| kwargs              | dict   | No       | Additional arguments for future compatibility (MCP/SSE pattern).            |

## Output Fields
| Key                    | Type         | Description                                                                 |
|------------------------|--------------|-----------------------------------------------------------------------------|
| workspace_name         | str          | The name of the Sentinel Log Analytics workspace.                           |
| resource_group         | str          | The Azure resource group for the workspace.                                 |
| subscription_id        | str          | The Azure subscription ID.                                                  |
| properties             | dict         | Detailed properties about the workspace (location, SKU, retention, etc.).   |
| additional_information | list of str  | Guidance on related tools and next steps.                                   |
| error                  | str (opt)    | Error message if an error occurs.                                           |

## Example Request
```python
result = await tool(ctx, kwargs={})
```

## Example Response
```json
{
  "workspace_name": "<workspace-name>",
  "resource_group": "<resource-group>",
  "subscription_id": "<subscription-id>",
  "properties": {
    "location": "eastus",
    "sku": "pergb2018",
    "sku_description": null,
    "last_sku_update": "",
    "retention_period_days": 30,
    "daily_quota_gb": null,
    "quota_reset_time": "",
    "ingestion_status": null,
    "public_network_access_ingestion": "Enabled",
    "public_network_access_query": "Enabled",
    "created": "2025-04-07T11:31:40.1654851Z",
    "last_modified": "2025-04-07T11:34:21.8036702Z",
    "features": "<features-object>"
  },
  "additional_information": [
    "For data connector details, use the `sentinel_connectors_list` tool.",
    "For analytics rules details, use the `list_analytics_rules` tool."
  ]
}
```

## Usage Notes
- Returns minimal information if Azure SDK or workspace context is missing.
- Supports both MCP server and direct invocation. If `ctx.request_context` is not available, falls back to environment variables for Azure context (`AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_SUBSCRIPTION_ID`, `AZURE_RESOURCE_GROUP`, `AZURE_WORKSPACE_NAME`).
- All errors are returned in the `error` field for testability.

## Error Cases
| Error Message                                      | Meaning                                                      |
|----------------------------------------------------|--------------------------------------------------------------|
| Missing Azure SDK or workspace details; returning minimal info. | Required context or SDK is missing, only basic info returned. |
| Error retrieving workspace info: <exception>        | An exception occurred while querying Azure for workspace info |

## See Also
- [sentinel_connectors_list](sentinel_connectors_list.md)
- [list_analytics_rules](sentinel_analytics_rule_list.md)
