# Microsoft Sentinel MCP Server Naming Convention

This document defines the naming convention for the Microsoft Sentinel MCP Server components, including tools, resources, and prompts.

## Core Principles

1. **Domain-Based Hierarchy**: Names follow the pattern `<domain>_<product>_<category>_<action>` for tools and prompts, and `<domain>_<product>://<category>/<subcategory>` for resources.
2. **Service Ownership Alignment**: Naming reflects actual Azure service ownership and relationships. Azure Monitor owns logs and workspaces; Sentinel is built on top of these.
3. **Consistency**: Similar operations use consistent verbs and categories across different components.
4. **Scalability**: The naming scheme allows for future expansion to other security products and features.
5. **Singular vs Plural**: Use singular nouns for operations on individual items (e.g., `incident_get`) and plural for collections (e.g., `incident_list`).

## Tool Naming Convention

Tools follow the pattern: `azure_<product>_<category>_<action>`

- **Domain**: Always `azure` for Microsoft Azure services
- **Product**: Specific product (sentinel, monitor, defender, etc.)
- **Category**: Feature area within the product
- **Action**: Operation (get, list, search, validate, etc.)

### Verb Usage Guidelines

- **list**: Retrieves multiple items (e.g., `sentinel_incidents_list`)
- **get**: Retrieves a single item by identifier (e.g., `sentinel_incident_get`)
- **search**: Performs a query operation (e.g., `sentinel_logs_search`)
- **create**: Generates a new item (e.g., `sentinel_analytics_create_detection`)
- **validate**: Verifies syntax or correctness (e.g., `sentinel_query_validate`)
- **update**: Modifies an existing item
- **delete**: Removes an item

## Resource Naming Convention

Resources follow the URI pattern: `azure_<product>://<category>/<subcategory>`

- **Domain**: Always `azure` for Microsoft Azure services
- **Product**: The specific product (sentinel, monitor, defender, etc.)
- **Category**: Primary categorisation (reference, examples, data)
- **Subcategory**: Further classification (kql, logs, incidents)

## Prompt Naming Convention

Prompts follow the same pattern as tools: `sentinel_<category>_<action>`

- The naming should emphasise the workflow or scenario the prompt supports
- Verbs can be more descriptive of the guided process (investigate, respond, create)

## Tool Implementation Status

| Category | Purpose | Standardised Name | Implemented |
|----------|---------|-------------------|-------------|
| KQL Tools | Validates KQL syntax | `sentinel_query_validate` | Yes (as `sentinel_query_validate`) |
| Hunting Tools | Runs hunting queries | `sentinel_hunting_search` | Yes (as `sentinel_hunting_search`) |
| Table Tools | Lists available tables | `sentinel_logs_tables_list` | Yes (as `sentinel_logs_tables_list`) |
| Table Tools | Retrieves table schema | `sentinel_logs_table_schema` | Yes (as `sentinel_logs_tables_schema`) |
| Log Tools | Executes queries against logs | `sentinel_logs_search` | Yes (as `sentinel_logs_search`) |
| Connector Tools | Lists data connectors | `sentinel_connectors_list` | Yes (as `sentinel_connectors_list`) |
| Incident Tools | Retrieves recent incidents | `sentinel_incident_list` | Yes (as `sentinel_incident_list`) |
| Incident Tools | Gets incident details | `sentinel_incident_get` | Yes (as `sentinel_incident_get`) |
| Workspace Tools | Gets workspace details | `sentinel_workspace_get` | Yes (as `sentinel_workspace_get`) |
| Workspace Tools | Lists workspace metadata | `sentinel_workspace_list` | No |
| Workbook Tools | Lists available workbooks | `sentinel_workbook_list` | No |
| Workbook Tools | Gets workbook details | `sentinel_workbook_get` | No |
| Analytics Tools | Lists analytics rules | `sentinel_analytics_rule_list` | No |
| Analytics Tools | Gets analytics rule details | `sentinel_analytics_rule_get` | No |
| Data Collection Tools | Lists data collection endpoints | `sentinel_dce_list` | No |
| Data Collection Tools | Gets data collection endpoint | `sentinel_dce_get` | No |
| Notebook Tools | Lists available notebooks | `sentinel_notebook_list` | No |
| Notebook Tools | Gets notebook details | `sentinel_notebook_get` | No |
| Repository Tools | Lists content repositories | `sentinel_repository_list` | No |
| Repository Tools | Gets repository details | `sentinel_repository_get` | No |
| Summary Tools | Lists summary rules | `sentinel_summary_rule_list` | No |
| Summary Tools | Gets summary rule details | `sentinel_summary_rule_get` | No |
| Watchlist Tools | Lists available watchlists | `sentinel_watchlist_list` | No |
| Watchlist Tools | Gets watchlist details | `sentinel_watchlist_get` | No |
| Azure Monitor DCR | Lists Data Collection Rules | `azure_monitor_dcr_list` | No |
| Azure Monitor DCR | Gets Data Collection Rule | `azure_monitor_dcr_get` | No |
| Azure Monitor Workspace | Lists Log Analytics Workspaces | `azure_monitor_workspace_list` | No |
| Azure Monitor Metrics | Queries Azure Monitor metrics | `azure_monitor_metrics_query` | No |
| Azure Monitor Alerts | Creates monitoring alert rule | `azure_monitor_alerts_create` | No |
| Entra ID Users | Lists Entra ID users | `entra_users_list` | No |
| Entra ID Users | Gets user details | `entra_user_get` | No |
| Entra ID Applications | Lists registered applications | `entra_applications_list` | No |
| Entra ID Access | Verifies access permissions | `entra_access_check` | No |
| Entra ID Sign-ins | Lists authentication logs | `entra_signin_logs_list` | No |
| Defender Recommendations | Lists security recommendations | `defender_recommendations_list` | No |
| Defender Score | Retrieves security score | `defender_score_get` | No |
| Defender Alerts | Lists security alerts | `defender_alerts_list` | No |
| Defender Alerts | Gets specific alert details | `defender_alert_get` | No |
| Defender Scan | On-demand security scan | `defender_resource_scan` | No |

## Resource Implementation Status

| Category | Content/Purpose | Standardised Name | Implemented |
|----------|-----------------|-------------------|-------------|
| KQL Basics | Basic KQL syntax | `sentinel://reference/kql/basics` | Yes |
| KQL Operators | KQL operators docs | `sentinel://reference/kql/operators` | Yes |
| KQL Operators | KQL aggregation funcs | `sentinel://reference/kql/operators/aggregations` | Yes |
| KQL Examples | General KQL examples | `sentinel://reference/kql/examples` | Yes |
| KQL Examples | Security KQL examples | `sentinel://reference/kql/examples/security` | Yes |
| KQL Cheatsheet | KQL quick reference | `sentinel://reference/kql/cheatsheet` | Yes |
| Sentinel Examples | Sentinel query examples | `sentinel://examples/hunting` | Yes |
| Sentinel Tables | Common Sentinel tables | `sentinel://reference/logs/tables` | Yes |

## Prompt Implementation Status

| Category | Purpose | Standardised Name | Implemented |
|----------|---------|-------------------|-------------|
| Investigation | IP investigation | `sentinel_hunting_investigate_ip` | Yes (as `sentinel_hunting_investigate_ip`) |
| Incident Response | Incident workflow | `sentinel_incident_respond` | Yes (as `sentinel_incident_respond`) |
| Query Building | Creates detection query | `sentinel_analytics_create_detection` | Yes (as `sentinel_analytics_create_detection`) |
| Query Building | Creates advanced query | `sentinel_hunting_create_query` | Yes (as `sentinel_hunting_create_query`) |

## Adjacent Services

The naming convention extends to other Microsoft security and monitoring services, as shown in the tools table above. These follow the same patterns and principles as the Sentinel-specific tools.

## Future Extension Guidelines

When adding new components:

1. **New Features**: Use the product's actual feature name as the category (e.g., `sentinel_workbooks_list`)
2. **New Products**: Add new domain prefixes for different products (e.g., `defender`, `entra`)
3. **New Actions**: Maintain verb consistency across similar operations
4. **New Resources**: Follow the established URI pattern and categorisation hierarchy

## Implementation Notes

- Tools and prompts should be registered with these standardised names
- Resources should be exposed with the new URI scheme
- For backward compatibility during transition, consider supporting both old and new naming schemes temporarily
