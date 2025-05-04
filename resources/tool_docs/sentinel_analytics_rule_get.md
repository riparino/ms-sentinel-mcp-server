# Sentinel Analytics Rule Get Tool

**Tool Name:** `sentinel_analytics_rule_get`

## Overview
Retrieves details for a specific Microsoft Sentinel analytics rule by its ID or name.

## Parameters
- `id` (str, required): The full resource ID or unique name of the analytics rule.

## Output
- Dict containing all available fields for the rule, e.g.:
    - `id` (str): Rule ID.
    - `name` (str): Rule name.
    - `display_name` (str): Display name.
    - `enabled` (bool): Whether the rule is enabled.
    - `severity` (str): Severity level.
    - `description` (str): Description.
    - `query` (str): KQL query (if applicable).
    - `kind` (str): Rule kind/type.
    - ... (all other rule properties)
- If error, returns a dict with `error` (str).

## Example Output
```
{
  "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace>/providers/Microsoft.SecurityInsights/alertRules/BuiltInFusion",
  "name": "BuiltInFusion",
  "kind": "Fusion",
  "displayName": "Advanced Multistage Attack Detection",
  "severity": "High",
  "enabled": true,
  "description": "Microsoft Sentinel uses Fusion, a correlation engine based on scalable machine learning algorithms, to automatically detect multistage attacks by identifying combinations of anomalous behaviors and suspicious activities that are observed at various stages of the kill chain. ...",
  "last_modified_utc": "2025-04-07T11:33:33.084728Z",
  "tactics": [
    "Collection",
    "CommandAndControl",
    "CredentialAccess",
    "DefenseEvasion",
    "Discovery",
    "Execution",
    "Exfiltration",
    "Impact",
    "InitialAccess",
    "LateralMovement",
    "Persistence",
    "PrivilegeEscalation"
  ]
}
```

## Error Handling
- Returns `error` field if context is missing, rule not found, or SDK/API errors occur.

## MCP Compliance
- Inherits from `MCPToolBase`.
- Implements `async def run(self, ctx, **kwargs)`.
- Registered in `register_tools()`.
- Uses robust Azure context extraction and error handling.
