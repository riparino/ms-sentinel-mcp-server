# sentinel_ml_analytics_setting_get

**Description:**
Get a specific Sentinel ML analytics setting by name.

**Parameters:**
- `setting_name` (str, required): The name of the ML analytics setting to retrieve.

**Output:**
```
{
  "setting": {
    "id": "<setting-id>",
    "name": "<setting-name>",
    "kind": "<kind>",
    "etag": "<etag>",
    "type": "<type>",
    "description": "<description>",
    "display_name": "<display-name>",
    "enabled": true|false,
    "last_modified_utc": "<timestamp>",
    "required_data_connectors": [<connector-list>],
    "tactics": [<tactics-list>],
    "techniques": [<techniques-list>],
    "anomaly_version": "<version>",
    "customizable_observations": [<observation-list>],
    "frequency": "<frequency>",
    "settings_status": "<status>",
    "is_default_settings": true|false,
    "anomaly_settings_version": "<version>",
    "settings_definition_id": "<definition-id>",
    "properties": { /* properties object */ },
    "referenced_by_analytic_rules": [
      {
        "rule_name": "<rule-name>",
        "rule_id": "<rule-id>",
        "rule_kind": "<rule-kind>"
      }
    ]
  },
  "valid": true|false,
  "errors": [<error-messages>],
  "error": "<error-message-if-any>"
}
```

**Error Handling:**
If the name is invalid or any error occurs, the output includes an `error` key and a descriptive message. The `errors` list will contain error messages, if any.

**Azure Context Fallback:**
Supports both MCP server and direct invocation. Falls back to environment variables if MCP context is unavailable.

**Example Usage:**
```json
{
  "tool": "sentinel_ml_analytics_setting_get",
  "kwargs": {"setting_name": "<setting-name>"}
}
```

**Example Response (invalid name):**
```json
{
  "setting": {},
  "valid": false,
  "errors": [
    "Error retrieving ML analytics setting: 'in <string>' requires string as left operand, not NoneType"
  ],
  "error": "Error retrieving ML analytics setting: 'in <string>' requires string as left operand, not NoneType"
}
```
{
  "tool": "sentinel_ml_analytics_setting_get",
  "kwargs": {"setting_name": "<setting-name>"}
}
```
