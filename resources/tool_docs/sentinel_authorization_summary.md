# sentinel_authorization_summary

## Purpose
Summarize Azure RBAC role assignments for Microsoft Sentinel and Log Analytics, reporting effective read permissions and key role assignments for the current identity.

## Parameters
| Name               | Type   | Required | Description                                                        |
|--------------------|--------|----------|--------------------------------------------------------------------|
| kwargs             | dict   | No       | Additional parameters (not used, for future extensibility)         |

## Output Fields
| Key                   | Type    | Description                                                                 |
|-----------------------|---------|-----------------------------------------------------------------------------|
| workspace             | dict    | Workspace and scope context (IDs, names, tried scopes)                      |
| role_assignments      | list    | List of role assignments (see below for fields)                             |
| permissions_assessment| dict    | Assessment of Sentinel/Log Analytics read access and covered scopes          |
| summary               | dict    | Summary counts and error list                                               |
| error                 | string  | Error message if any error occurred                                         |

### role_assignments fields
| Field                 | Type    | Description                                                                 |
|-----------------------|---------|-----------------------------------------------------------------------------|
| role_assignment_id    | string  | Azure role assignment resource ID                                            |
| principal_id          | string  | Azure AD object ID of the principal                                         |
| scope                 | string  | Azure scope of the assignment                                               |
| role_definition_id    | string  | Role definition ID                                                          |
| role_name             | string  | Role name                                                                   |
| description           | string  | Role description                                                            |
| category              | string  | Role category (e.g. BuiltInRole)                                            |
| is_read               | bool    | True if role is considered a 'read' role                                    |
| is_sentinel_read      | bool    | True if role is a recognized Sentinel read role                             |
| is_log_analytics_read | bool    | True if role is a recognized Log Analytics read role                        |

## Example Request
```
{
  "kwargs": {}
}
```

## Example Response
```
{
  "workspace": {
    "subscription_id": "...",
    "resource_group": "...",
    "workspace_name": "...",
    "workspace_id": "...",
    "scope_used": "...",
    "scopes_tried": ["...", "...", "..."]
  },
  "role_assignments": [
    {
      "role_assignment_id": "...",
      "principal_id": "...",
      "scope": "...",
      "role_definition_id": "...",
      "role_name": "Log Analytics Contributor",
      "description": "...",
      "category": "BuiltInRole",
      "is_read": true,
      "is_sentinel_read": false,
      "is_log_analytics_read": false
    }
  ],
  "permissions_assessment": {
    "has_sentinel_read": true,
    "has_log_analytics_read": true,
    "read_scopes": ["...", "..."]
  },
  "summary": {
    "sentinel_read_roles": 1,
    "log_analytics_read_roles": 1,
    "total_roles": 14,
    "scopes_with_read_access": 4,
    "errors": []
  }
}
```

## Usage Notes
- Requires Azure credentials and workspace context, provided via MCP or environment variables.
- Returns all output keys even on error for robust testability.
- Uses both direct and nested kwargs for parameter extraction.

## Error Cases
- Missing Azure context or credentials: returns 'error' with details and empty lists for other fields.
- Azure SDK errors: returns 'error' with exception type and message, plus partial output if available.

## See Also
- [sentinel_incident_details_get.md](sentinel_incident_details_get.md)
- [tool-architecture-and-implementation-requirements.md](../docs/architecture/tool-architecture-and-implementation-requirements.md)
