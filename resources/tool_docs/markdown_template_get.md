# Markdown Template Get Tool

## Purpose
Retrieves the raw markdown content for a specific template by name. This tool allows users to access template content for rendering or reference purposes.

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| name | string | Yes | Name of the markdown template (without .md extension) |

## Output Fields
| Field | Type | Description |
|-------|------|-------------|
| content | string | Raw markdown content of the template |
| error | string | Error message if the operation failed (only present on error) |
| available_templates | array[string] | List of available template names (only present when template not found) |

## Example Request
```json
{
  "name": "sentinel_workspace_get"
}
```

## Example Response
```json
{
  "content": "# Azure Sentinel Workspace Details\n\n**Workspace Name:** `{{ workspace_name }}`\n**Resource Group:** `{{ resource_group }}`\n**Subscription:** `{{ subscription_id }}`\n**Location:** `{{ direct_info.location }}`\n**SKU:** `{{ direct_info.sku }}`\n{% if direct_info.sku_description %}  _Description:_ {{ direct_info.sku_description }}{% endif %}\n..."
}
```

## Usage Notes
- Templates are stored in the `resources/markdown_templates` directory with a `.md` extension
- The template name should be provided without the `.md` extension
- Templates can use Jinja2 syntax for variable substitution and control flow
- If the requested template doesn't exist, the tool will return a list of available templates

## Error Cases
| Error | Description |
|-------|-------------|
| "Missing or invalid required parameter: name" | The name parameter is missing or invalid |
| "Markdown templates directory does not exist: {path}" | The templates directory cannot be found |
| "Markdown template not found: {name}" | The requested template doesn't exist |
| "Failed to read markdown template: {error}" | An error occurred while reading the template file |
| "Failed to get markdown template: {error}" | An unexpected error occurred |

## See Also
- [markdown_templates_list](markdown_templates_list.md) - List all available markdown templates
