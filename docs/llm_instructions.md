# Microsoft Sentinel MCP Server Instructions

This server provides access to Microsoft Sentinel workspaces, data, and functionality through the Model Context Protocol.

## Essential Workflow

1. **Documentation First**: Before using any tool, retrieve and review its documentation using:
   - `tool_docs_list` - See all available documentation
   - `tool_docs_get` - Get specific documentation by path
   - `tool_docs_search` - Search across documentation

2. **Tool Usage**: After understanding the tool, use it with proper parameters

3. **Formatting Results**: Use markdown templates when available:
   - `markdown_templates_list` - Discover available templates
   - `markdown_template_get` - Retrieve specific template content
   - Templates are named after their associated tools (e.g., `sentinel_incident_get.md`)

## Best Practices

- Validate KQL queries with `sentinel_query_validate` before execution
- Summarise large result sets rather than displaying all data
- Use proper KQL syntax highlighting in code blocks
- Never expose sensitive data (connection strings, API keys, tokens)
- Explain security incidents in a structured, clear manner
- Provide context and disclaimers for security recommendations

## Key Capabilities

- Execute and validate KQL queries against Sentinel and Log Analytics data
- Retrieve and investigate security incidents, alerts, and related entities
- Manage and enumerate analytics rules, rule templates, and ML analytics settings
- List, configure, and get details for data connectors
- Access workspace metadata and configuration
- Manage and query watchlists for enrichment and investigation
- Retrieve and use markdown templates for consistent report formatting
- Explore and search comprehensive tool and resource documentation

## Getting Started

1. Check workspace details: `sentinel_workspace_get`
2. List available tables: `sentinel_logs_tables_list` 
3. Get a table's schema: `sentinel_logs_table_schema_get`
4. Get a table's details: `sentinel_logs_table_details_get`
5. Validate a query before running it: `sentinel_query_validate`
6. Run a query against the workspace: `sentinel_logs_search`

## Security Note

Operations are performed using the configured identity's permissions and subject to Azure RBAC controls.