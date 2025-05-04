# Markdown Templates List Tool

## Purpose
Lists all available markdown templates in the system with their names, URIs, descriptions, and content. This tool helps users discover available templates that can be used for formatting and presenting data in a consistent way.

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| None | | | This tool does not require any parameters |

## Output Fields
| Field | Type | Description |
|-------|------|-------------|
| templates | array | List of template objects |
| templates[].name | string | Name of the template (without .md extension) |
| templates[].uri | string | URI reference to the template (format: markdown://templates/{name}) |
| templates[].description | string | Short description of the template (first line of the file if it starts with #) |
| templates[].content | string | Full markdown content of the template |
| error | string | Error message if the operation failed (only present on error) |

## Example Request
```json
{
  "kwargs": {}
}
```

## Example Response
```json
{
  "templates": [
    {
      "name": "sentinel_workspace_get",
      "uri": "markdown://templates/sentinel_workspace_get",
      "description": "# Azure Sentinel Workspace Details",
      "content": "# Azure Sentinel Workspace Details\n\n**Workspace Name:** `{{ workspace_name }}`\n**Resource Group:** `{{ resource_group }}`\n**Subscription:** `{{ subscription_id }}`\n**Location:** `{{ direct_info.location }}`\n**SKU:** `{{ direct_info.sku }}`\n{% if direct_info.sku_description %}  _Description:_ {{ direct_info.sku_description }}{% endif %}\n..."
    }
  ]
}
```

## Usage Notes
- Templates are stored in the `resources/markdown_templates` directory with a `.md` extension
- Templates can use Jinja2 syntax for variable substitution and control flow
- The description is automatically extracted from the first line of the template if it starts with a # (markdown heading)

## Error Cases
| Error | Description |
|-------|-------------|
| "Markdown templates directory does not exist: {path}" | The templates directory cannot be found |
| "Failed to list markdown templates: {error}" | An unexpected error occurred while listing templates |

## See Also
- [markdown_template_get](markdown_template_get.md) - Get a specific markdown template by name
