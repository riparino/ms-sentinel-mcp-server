<!--
This file contains a complete list of KQL queries from git://github.com/dstreefkerk/ms-sentinel-mcp-server.git.
Generated automatically using Repomix.
-->

This file is a merged representation of a subset of the codebase, containing specifically included files, combined into a single document by Repomix.
The content has been processed where content has been compressed (code blocks are separated by ⋮---- delimiter).

# Directory Structure
```
docs/
  architecture/
    libraries/
      azure-mgmt-loganalytics-api-reference.md
      azure-mgmt-securityinsight-api-reference.md
      data-connector-visibility-summary.md
      MCP Python SDK Readme.md
    backend-structure.md
    implementation-plan.md
    naming_convention.md
    project-requirements-document.md
    prompt-architecture-doc.md
    security-guideline-document.md
    system-flow-document.md
    tech-stack-document.md
    tool-architecture-and-implementation-requirements.md
  llm_instructions.md
resources/
  markdown_templates/
    sentinel_workspace_get.md
  tool_docs/
    entra_id_get_group.md
    entra_id_get_user.md
    entra_id_list_groups.md
    entra_id_list_users.md
    llm_instructions_get.md
    log_analytics_saved_search_get.md
    log_analytics_saved_searches_list.md
    markdown_template_get.md
    markdown_templates_list.md
    sentinel_analytics_rule_get.md
    sentinel_analytics_rule_list.md
    sentinel_analytics_rule_template_get.md
    sentinel_analytics_rule_templates_count_by_tactic.md
    sentinel_analytics_rule_templates_count_by_technique.md
    sentinel_analytics_rule_templates_list.md
    sentinel_analytics_rules_count_by_tactic.md
    sentinel_analytics_rules_count_by_technique.md
    sentinel_authorization_summary.md
    sentinel_connectors_get.md
    sentinel_connectors_list.md
    sentinel_domain_whois_get.md
    sentinel_hunting_queries_count_by_tactic.md
    sentinel_hunting_queries_list.md
    sentinel_hunting_query_get.md
    sentinel_incident_details_get.md
    sentinel_ip_geodata_get.md
    sentinel_logs_search_with_dummy_data.md
    sentinel_logs_search.md
    sentinel_logs_table_details_get.md
    sentinel_logs_table_schema_get.md
    sentinel_logs_tables_list.md
    sentinel_metadata_get.md
    sentinel_metadata_list.md
    sentinel_ml_analytics_setting_get.md
    sentinel_ml_analytics_settings_list.md
    sentinel_query_validate.md
    sentinel_source_control_get.md
    sentinel_source_controls_list.md
    sentinel_watchlist_get.md
    sentinel_watchlist_item_get.md
    sentinel_watchlist_items_list.md
    sentinel_watchlists_list.md
    sentinel_workspace_get.md
    tool_docs_get.md
    tool_docs_list.md
    tool_docs_search.md
README.md
```

# Files

## File: docs/architecture/libraries/azure-mgmt-loganalytics-api-reference.md
````markdown
# Azure Log Analytics Management Client SDK API Reference Guide

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Client Initialization](#client-initialization)
- [Workspaces Management](#workspaces-management)
- [Clusters Management](#clusters-management)
- [Tables Management](#tables-management)
- [Data Sources Management](#data-sources-management)
- [Data Exports Management](#data-exports-management)
- [Saved Searches Management](#saved-searches-management)
- [Query Management](#query-management)
- [Storage Insights Management](#storage-insights-management)
- [Linked Services Management](#linked-services-management)
- [Shared Keys Management](#shared-keys-management)
- [Data Models](#data-models)
- [Enumerations](#enumerations)
- [Error Handling](#error-handling)
- [Authentication](#authentication)
- [Asynchronous Operations](#asynchronous-operations)

## Overview

The Azure Log Analytics Management Client SDK provides access to manage Azure Log Analytics resources programmatically. This SDK is part of the Azure Management Libraries for Python.

Current version: 13.0.0b7

## Installation

```bash
pip install azure-mgmt-loganalytics
```

## Client Initialization

The main entry point for using the Log Analytics Management SDK is the `LogAnalyticsManagementClient` class.

### LogAnalyticsManagementClient

The primary client for interacting with Azure Log Analytics service.

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.loganalytics import LogAnalyticsManagementClient

# Initialize client
client = LogAnalyticsManagementClient(
    credential=DefaultAzureCredential(),
    subscription_id="your-subscription-id"
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| credential | TokenCredential | Azure credential for authentication |
| subscription_id | str | The Azure subscription ID |
| base_url | str | Optional. Default: "https://management.azure.com" |

## Workspaces Management

Workspaces are the primary resources in Log Analytics. They serve as containers for your data and provide a unique environment for data collection, analysis, and storage.

### Methods

| Method | Description | Return Type |
|--------|-------------|-------------|
| list() | Gets all workspaces in a subscription | ItemPaged[Workspace] |
| list_by_resource_group(resource_group_name) | Gets workspaces in a resource group | ItemPaged[Workspace] |
| begin_create_or_update(resource_group_name, workspace_name, parameters) | Create or update a workspace | LROPoller[Workspace] |
| begin_delete(resource_group_name, workspace_name, force=None) | Delete a workspace | LROPoller[None] |
| get(resource_group_name, workspace_name) | Get a workspace | Workspace |
| update(resource_group_name, workspace_name, parameters) | Update a workspace | Workspace |

#### Example: Create a Workspace

```python
response = client.workspaces.begin_create_or_update(
    resource_group_name="my-resource-group",
    workspace_name="my-workspace",
    parameters={
        "location": "eastus",
        "properties": {
            "retentionInDays": 30,
            "sku": {"name": "PerGB2018"}
        },
        "tags": {"environment": "production"}
    }
).result()
```

#### Example: List Workspaces

```python
workspaces = client.workspaces.list_by_resource_group(
    resource_group_name="my-resource-group"
)

for workspace in workspaces:
    print(f"Workspace: {workspace.name}, ID: {workspace.id}")
```

## Clusters Management

Log Analytics clusters allow you to use dedicated capacity for your Log Analytics workspaces.

### Methods

| Method | Description | Return Type |
|--------|-------------|-------------|
| list_by_resource_group(resource_group_name) | Gets clusters in a resource group | ItemPaged[Cluster] |
| list() | Gets all clusters in a subscription | ItemPaged[Cluster] |
| begin_create_or_update(resource_group_name, cluster_name, parameters) | Create/update a cluster | LROPoller[Cluster] |
| begin_delete(resource_group_name, cluster_name) | Delete a cluster | LROPoller[None] |
| get(resource_group_name, cluster_name) | Get a cluster | Cluster |
| begin_update(resource_group_name, cluster_name, parameters) | Update a cluster | LROPoller[Cluster] |

#### Example: Create a Cluster

```python
response = client.clusters.begin_create_or_update(
    resource_group_name="my-resource-group",
    cluster_name="my-cluster",
    parameters={
        "location": "westus2",
        "identity": {
            "type": "SystemAssigned"
        },
        "sku": {
            "name": "CapacityReservation",
            "capacity": 1000
        },
        "properties": {
            "isDoubleEncryptionEnabled": True
        }
    }
).result()
```

## Tables Management

Tables are used to store Log Analytics data in a structured format.

### Methods

| Method | Description | Return Type |
|--------|-------------|-------------|
| list_by_workspace(resource_group_name, workspace_name) | Get all tables in a workspace | ItemPaged[Table] |
| begin_create_or_update(resource_group_name, workspace_name, table_name, parameters) | Create/update a table | LROPoller[Table] |
| begin_update(resource_group_name, workspace_name, table_name, parameters) | Update a table | LROPoller[Table] |
| get(resource_group_name, workspace_name, table_name) | Get a table | Table |
| begin_delete(resource_group_name, workspace_name, table_name) | Delete a table | LROPoller[None] |
| migrate(resource_group_name, workspace_name, table_name) | Migrate a table | None |
| cancel_search(resource_group_name, workspace_name, table_name) | Cancel search | None |

#### Example: Create a Table

```python
response = client.tables.begin_create_or_update(
    resource_group_name="my-resource-group",
    workspace_name="my-workspace",
    table_name="MyCustomTable",
    parameters={
        "properties": {
            "schema": {
                "name": "MyCustomTable",
                "columns": [
                    {
                        "name": "TimeGenerated",
                        "type": "datetime"
                    },
                    {
                        "name": "Computer",
                        "type": "string"
                    },
                    {
                        "name": "EventID",
                        "type": "int"
                    }
                ]
            },
            "retentionInDays": 30,
            "plan": "Analytics"
        }
    }
).result()
```

## Data Sources Management

Data sources define how Log Analytics collects data.

### Methods

| Method | Description | Return Type |
|--------|-------------|-------------|
| create_or_update(resource_group_name, workspace_name, data_source_name, parameters) | Create/update a data source | DataSource |
| delete(resource_group_name, workspace_name, data_source_name) | Delete a data source | None |
| get(resource_group_name, workspace_name, data_source_name) | Get a data source | DataSource |
| list_by_workspace(resource_group_name, workspace_name) | Get all data sources in a workspace | DataSourceListResult |

#### Example: Create a Data Source

```python
response = client.data_sources.create_or_update(
    resource_group_name="my-resource-group",
    workspace_name="my-workspace",
    data_source_name="my-windows-event-source",
    parameters={
        "kind": "WindowsEvent",
        "properties": {
            "eventLogName": "Application",
            "eventTypes": [
                {"eventType": "Error"},
                {"eventType": "Warning"}
            ]
        }
    }
)
```

## Data Exports Management

Data exports allow you to continuously export data from a Log Analytics workspace.

### Methods

| Method | Description | Return Type |
|--------|-------------|-------------|
| create_or_update(resource_group_name, workspace_name, data_export_name, parameters) | Create/update a data export | DataExport |
| delete(resource_group_name, workspace_name, data_export_name) | Delete a data export | None |
| get(resource_group_name, workspace_name, data_export_name) | Get a data export | DataExport |
| list_by_workspace(resource_group_name, workspace_name) | List data exports in a workspace | DataExportListResult |

#### Example: Create a Data Export

```python
response = client.data_exports.create_or_update(
    resource_group_name="my-resource-group",
    workspace_name="my-workspace",
    data_export_name="my-data-export",
    parameters={
        "properties": {
            "destination": {
                "resourceId": "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.Storage/storageAccounts/{storage-account}",
                "type": "StorageAccount"
            },
            "tableNames": ["SecurityEvent", "Heartbeat"],
            "enable": True
        }
    }
)
```

## Saved Searches Management

Saved searches allow you to save and reuse queries in Log Analytics.

### Methods

| Method | Description | Return Type |
|--------|-------------|-------------|
| delete(resource_group_name, workspace_name, saved_search_id) | Delete a saved search | None |
| create_or_update(resource_group_name, workspace_name, saved_search_id, parameters) | Create/update saved search | SavedSearch |
| get(resource_group_name, workspace_name, saved_search_id) | Get a saved search | SavedSearch |
| list_by_workspace(resource_group_name, workspace_name) | Get all saved searches in a workspace | SavedSearchesListResult |

#### Example: Create a Saved Search

```python
response = client.saved_searches.create_or_update(
    resource_group_name="my-resource-group",
    workspace_name="my-workspace",
    saved_search_id="my-saved-search",
    parameters={
        "etag": "*",
        "properties": {
            "category": "Monitoring",
            "displayName": "All Events with level Error",
            "query": "Event | where EventLevel == 1",
            "version": 1
        }
    }
)
```

## Query Management

Query operations for Log Analytics.

### Methods

| Method | Description | Return Type |
|--------|-------------|-------------|
| list(resource_group_name, query_pack_name) | List all queries | LogAnalyticsQueryPackQueryListResult |
| get(resource_group_name, query_pack_name, query_id) | Get a query | LogAnalyticsQueryPackQuery |
| delete(resource_group_name, query_pack_name, query_id) | Delete a query | None |

#### Example: List Queries

```python
response = client.queries.list(
    resource_group_name="my-resource-group",
    query_pack_name="my-query-pack"
)

for query in response.value:
    print(f"Query: {query.display_name}, ID: {query.id}")
```

## Storage Insights Management

Storage insights connect Azure Storage accounts to Log Analytics.

### Methods

| Method | Description | Return Type |
|--------|-------------|-------------|
| create_or_update(resource_group_name, workspace_name, storage_insight_name, parameters) | Create/update storage insight | StorageInsightConfig |
| delete(resource_group_name, workspace_name, storage_insight_name) | Delete a storage insight | None |
| get(resource_group_name, workspace_name, storage_insight_name) | Get a storage insight | StorageInsightConfig |
| list_by_workspace(resource_group_name, workspace_name) | List storage insights in a workspace | StorageInsightListResult |

#### Example: Create a Storage Insight

```python
response = client.storage_insight_configs.create_or_update(
    resource_group_name="my-resource-group",
    workspace_name="my-workspace",
    storage_insight_name="my-storage-insight",
    parameters={
        "properties": {
            "storageAccount": {
                "id": "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.Storage/storageAccounts/{storage-account}"
            },
            "tables": ["WADWindowsEventLogsTable"],
            "containers": ["wad-iis-logfiles"]
        }
    }
)
```

## Linked Services Management

Linked services connect other Azure services to Log Analytics.

### Methods

| Method | Description | Return Type |
|--------|-------------|-------------|
| create_or_update(resource_group_name, workspace_name, linked_service_name, parameters) | Create/update linked service | LinkedService |
| delete(resource_group_name, workspace_name, linked_service_name) | Delete a linked service | None |
| get(resource_group_name, workspace_name, linked_service_name) | Get a linked service | LinkedService |
| list_by_workspace(resource_group_name, workspace_name) | List linked services in a workspace | LinkedServiceListResult |

#### Example: Create a Linked Service

```python
response = client.linked_services.create_or_update(
    resource_group_name="my-resource-group",
    workspace_name="my-workspace",
    linked_service_name="Automation",
    parameters={
        "properties": {
            "resourceId": "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.Automation/automationAccounts/{automation-account}"
        }
    }
)
```

## Shared Keys Management

Management of shared keys for Log Analytics workspaces.

### Methods

| Method | Description | Return Type |
|--------|-------------|-------------|
| get_shared_keys(resource_group_name, workspace_name) | Get shared keys for a workspace | SharedKeys |
| regenerate_shared_keys(resource_group_name, workspace_name, key_name) | Regenerate shared keys | SharedKeys |

#### Example: Get Shared Keys

```python
response = client.shared_keys.get_shared_keys(
    resource_group_name="my-resource-group",
    workspace_name="my-workspace"
)

primary_key = response.primary_shared_key
secondary_key = response.secondary_shared_key
```

## Data Models

### Workspace

Primary Log Analytics workspace resource

| Property | Type | Description |
|----------|------|-------------|
| id | str | Resource ID |
| name | str | Resource name |
| type | str | Resource type |
| location | str | Azure region |
| tags | dict | Resource tags |
| etag | str | Resource ETag |
| sku | dict | SKU information |
| retention_in_days | int | Data retention period |
| customer_id | str | Workspace customer ID |
| provisioning_state | str | Provisioning state |
| created_date | str | Creation date |
| modified_date | str | Last modification date |
| features | dict | Workspace features |
| workspace_capping | dict | Workspace data capping settings |
| public_network_access_for_ingestion | str | Public network access for data ingestion |
| public_network_access_for_query | str | Public network access for queries |
| private_link_scoped_resources | list | Private link resources |

### Cluster

Log Analytics cluster resource

| Property | Type | Description |
|----------|------|-------------|
| id | str | Resource ID |
| name | str | Resource name |
| type | str | Resource type |
| location | str | Azure region |
| tags | dict | Resource tags |
| identity | dict | Managed identity information |
| sku | dict | SKU information |
| cluster_id | str | Unique cluster identifier |
| provisioning_state | str | Provisioning state |
| is_double_encryption_enabled | bool | Whether double encryption is enabled |
| is_availability_zones_enabled | bool | Whether availability zones are enabled |
| billing_type | str | Billing type (Cluster or Workspaces) |
| key_vault_properties | dict | Key vault settings for CMK |
| created_date | str | Creation date |
| last_modified_date | str | Last modification date |
| associated_workspaces | list | Workspaces using this cluster |

### DataSource

Log Analytics data source

| Property | Type | Description |
|----------|------|-------------|
| id | str | Resource ID |
| name | str | Resource name |
| type | str | Resource type |
| kind | str | Data source kind |
| properties | dict | Data source-specific properties |

### DataExport

Configuration for exporting data

| Property | Type | Description |
|----------|------|-------------|
| id | str | Resource ID |
| name | str | Resource name |
| type | str | Resource type |
| data_export_id | str | Unique export identifier |
| created_date | str | Creation date |
| last_modified_date | str | Last modification date |
| data_export_type | str | Export type |
| destination | dict | Export destination details |
| enable | bool | Whether export is enabled |
| stream_names | list | Streams to export |
| table_names | list | Tables to export |

### Table

Log Analytics table

| Property | Type | Description |
|----------|------|-------------|
| id | str | Resource ID |
| name | str | Resource name |
| type | str | Resource type |
| schema | dict | Table schema |
| retention_in_days | int | Data retention period |
| total_retention_in_days | int | Total retention period |
| plan | str | Table plan (Basic or Analytics) |
| search_results | dict | Search result information |
| table_type | str | Table type |
| sub_type | str | Table subtype |
| source | str | Table source |
| columns | list | Column definitions |
| provisioning_state | str | Provisioning state |

### SavedSearch

Saved search in a workspace

| Property | Type | Description |
|----------|------|-------------|
| id | str | Resource ID |
| etag | str | Resource ETag |
| category | str | Search category |
| display_name | str | Display name |
| query | str | KQL query text |
| function_alias | str | Function alias |
| function_parameters | list | Function parameters |
| version | int | Version number |

## Enumerations

### BillingType

| Value | Description |
|-------|-------------|
| CLUSTER | Billing at cluster level |
| WORKSPACES | Billing at workspace level |

### ClusterEntityStatus

| Value | Description |
|-------|-------------|
| CREATING | Cluster is being created |
| SUCCEEDED | Operation succeeded |
| FAILED | Operation failed |
| CANCELED | Operation was canceled |
| DELETING | Cluster is being deleted |
| PROVISIONING_ACCOUNT | Account is being provisioned |
| UPDATING | Cluster is being updated |

### DataSourceKind

| Value | Description |
|-------|-------------|
| WINDOWS_EVENT | Windows Event logs |
| WINDOWS_PERFORMANCE_COUNTER | Windows performance counters |
| IIS_LOGS | IIS logs |
| LINUX_SYSLOG | Linux syslog |
| LINUX_PERFORMANCE_OBJECT | Linux performance objects |
| CUSTOM_LOG | Custom logs |
| AZURE_ACTIVITY_LOG | Azure Activity logs |
| OFFICE365 | Office 365 logs |
| WINDOWS_TELEMETRY | Windows telemetry |
| SQL_DATA_CLASSIFICATION | SQL data classification |
| APPLICATION_INSIGHTS | Application Insights data |

### SkuNameEnum

| Value | Description |
|-------|-------------|
| FREE | Free tier |
| STANDARD | Standard tier |
| PREMIUM | Premium tier |
| PER_NODE | Per node pricing |
| PER_GB2018 | Per GB pricing (2018) |
| STANDALONE | Standalone pricing |
| CAPACITY_RESERVATION | Capacity reservation pricing |

### TablePlanEnum

| Value | Description |
|-------|-------------|
| BASIC | Basic plan |
| ANALYTICS | Analytics plan |

### TableTypeEnum

| Value | Description |
|-------|-------------|
| MICROSOFT | Microsoft-defined tables |
| CUSTOM_LOG | Custom log tables |
| RESTORED_LOGS | Restored log tables |
| SEARCH_RESULTS | Search results tables |

## Error Handling

The SDK uses standard Azure error handling patterns. Error responses follow the ErrorResponse model:

```python
try:
    response = client.workspaces.get(
        resource_group_name="my-resource-group",
        workspace_name="non-existent-workspace"
    )
except HttpResponseError as e:
    print(f"Error code: {e.error.code}")
    print(f"Message: {e.error.message}")
    # Handle specific error codes
    if e.error.code == "ResourceNotFound":
        print("The workspace does not exist")
```

## Authentication

The SDK supports multiple authentication methods:

```python
# Default Azure authentication (environment, managed identity, etc.)
from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()

# Service principal authentication
from azure.identity import ClientSecretCredential
credential = ClientSecretCredential(
    tenant_id="tenant-id",
    client_id="client-id",
    client_secret="client-secret"
)

# Initialize client
client = LogAnalyticsManagementClient(
    credential=credential,
    subscription_id="subscription-id"
)
```

## Asynchronous Operations

The SDK provides async versions of all operations in the `aio` namespace.

```python
from azure.identity.aio import DefaultAzureCredential
from azure.mgmt.loganalytics.aio import LogAnalyticsManagementClient
import asyncio

async def main():
    async with DefaultAzureCredential() as credential:
        client = LogAnalyticsManagementClient(
            credential=credential,
            subscription_id="subscription-id"
        )
        
        workspaces = [
            workspace async for workspace in client.workspaces.list()
        ]
        
        for workspace in workspaces:
            print(f"Workspace: {workspace.name}")
            
        # Long-running operations
        workspace = await (
            client.workspaces.begin_create_or_update(
                resource_group_name="my-resource-group",
                workspace_name="my-workspace",
                parameters={
                    "location": "eastus",
                    "properties": {"retentionInDays": 30}
                }
            )
        ).result()
        
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```
````

## File: docs/architecture/libraries/azure-mgmt-securityinsight-api-reference.md
````markdown
# Azure Management SecurityInsight SDK for Python

## Overview

The Azure Management SecurityInsight SDK for Python provides tools for managing Azure Sentinel resources. It allows you to automate the management of incidents, alert rules, data connectors, bookmarks, watchlists, and other security-related resources in Azure Sentinel.

## Installation

```bash
pip install azure-mgmt-securityinsight
```

## Authentication

This SDK uses the Azure Identity library for authentication. You can authenticate using various methods such as environment variables, managed identity, or interactive login.

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.securityinsight import SecurityInsights

# Authenticate using default credentials
credential = DefaultAzureCredential()
subscription_id = "<your-subscription-id>"

# Initialize the client
client = SecurityInsights(
    credential=credential,
    subscription_id=subscription_id
)
```

## Primary Client Class

### SecurityInsights

The main client class for interacting with Azure Security Insights (Azure Sentinel).

```python
class SecurityInsights(object):
    def __init__(self, credential, subscription_id, base_url="https://management.azure.com", **kwargs)
```

**Parameters**:
- `credential`: Required. An instance of `TokenCredential` from the `azure.core.credentials` package.
- `subscription_id`: Required. The ID of the Azure subscription.
- `base_url`: Optional. The service URL. Default is "https://management.azure.com".

**Public Methods**:
- `close()`: Closes the client connection.

**Available Operations**:
The client class exposes various operation groups as properties:

```python
# Example of accessing operations
client.incidents.list(resource_group_name, workspace_name)
client.alert_rules.get(resource_group_name, workspace_name, rule_id)
```

## Operations Groups

### IncidentsOperations

Operations related to security incidents in Sentinel.

**Key Methods**:
- `list(resource_group_name, workspace_name, filter=None, orderby=None, top=None, skip_token=None)`: Lists all incidents
- `get(resource_group_name, workspace_name, incident_id)`: Gets a specific incident
- `create_or_update(resource_group_name, workspace_name, incident_id, incident)`: Creates or updates an incident
- `delete(resource_group_name, workspace_name, incident_id)`: Deletes an incident
- `run_playbook(resource_group_name, workspace_name, incident_identifier, request_body=None)`: Triggers a playbook on an incident
- `create_team(resource_group_name, workspace_name, incident_id, team_properties)`: Creates a Microsoft Team for incident collaboration
- `list_alerts(resource_group_name, workspace_name, incident_id)`: Gets all alerts related to an incident
- `list_bookmarks(resource_group_name, workspace_name, incident_id)`: Gets all bookmarks related to an incident
- `list_entities(resource_group_name, workspace_name, incident_id)`: Gets all entities related to an incident

### IncidentCommentsOperations

Operations related to comments on security incidents.

**Key Methods**:
- `list(resource_group_name, workspace_name, incident_id)`: Lists all comments for an incident
- `get(resource_group_name, workspace_name, incident_id, incident_comment_id)`: Gets a specific comment
- `create_or_update(resource_group_name, workspace_name, incident_id, incident_comment_id, incident_comment)`: Creates or updates a comment
- `delete(resource_group_name, workspace_name, incident_id, incident_comment_id)`: Deletes a comment

### IncidentTasksOperations

Operations related to tasks created for incidents.

**Key Methods**:
- `list(resource_group_name, workspace_name, incident_id)`: Lists all tasks for an incident
- `get(resource_group_name, workspace_name, incident_id, incident_task_id)`: Gets a specific task
- `create_or_update(resource_group_name, workspace_name, incident_id, incident_task_id, incident_task)`: Creates or updates a task
- `delete(resource_group_name, workspace_name, incident_id, incident_task_id)`: Deletes a task

### IncidentRelationsOperations

Operations related to relations between incidents and other entities.

**Key Methods**:
- `list(resource_group_name, workspace_name, incident_id)`: Lists all relations for an incident
- `get(resource_group_name, workspace_name, incident_id, relation_name)`: Gets a specific relation
- `create_or_update(resource_group_name, workspace_name, incident_id, relation_name, relation)`: Creates or updates a relation
- `delete(resource_group_name, workspace_name, incident_id, relation_name)`: Deletes a relation

### AlertRulesOperations

Operations related to alert rules that generate incidents.

**Key Methods**:
- `list(resource_group_name, workspace_name)`: Lists all alert rules
- `get(resource_group_name, workspace_name, rule_id)`: Gets a specific alert rule
- `create_or_update(resource_group_name, workspace_name, rule_id, alert_rule)`: Creates or updates an alert rule
- `delete(resource_group_name, workspace_name, rule_id)`: Deletes an alert rule

### AlertRuleTemplatesOperations

Operations related to templates for alert rules.

**Key Methods**:
- `list(resource_group_name, workspace_name)`: Lists all alert rule templates
- `get(resource_group_name, workspace_name, template_id)`: Gets a specific alert rule template

### ActionsOperations

Operations related to actions that can be performed in response to an alert.

**Key Methods**:
- `list(resource_group_name, workspace_name, rule_id)`: Lists all actions for an alert rule
- `get(resource_group_name, workspace_name, rule_id, action_id)`: Gets a specific action
- `create_or_update(resource_group_name, workspace_name, rule_id, action_id, action)`: Creates or updates an action
- `delete(resource_group_name, workspace_name, rule_id, action_id)`: Deletes an action

### AutomationRulesOperations

Operations related to automation rules in Sentinel.

**Key Methods**:
- `list(resource_group_name, workspace_name)`: Lists all automation rules
- `get(resource_group_name, workspace_name, rule_id)`: Gets a specific automation rule
- `create_or_update(resource_group_name, workspace_name, rule_id, automation_rule)`: Creates or updates an automation rule
- `delete(resource_group_name, workspace_name, rule_id)`: Deletes an automation rule

### DataConnectorsOperations

Operations related to data sources connected to Sentinel.

**Key Methods**:
- `list(resource_group_name, workspace_name)`: Lists all data connectors
- `get(resource_group_name, workspace_name, data_connector_id)`: Gets a specific data connector
- `create_or_update(resource_group_name, workspace_name, data_connector_id, connector)`: Creates or updates a data connector
- `delete(resource_group_name, workspace_name, data_connector_id)`: Deletes a data connector

### DataConnectorsCheckRequirementsOperations

Operations to check requirements for data connectors.

**Key Methods**:
- `check(resource_group_name, workspace_name, connector_kind)`: Checks if the requirements for a specific connector kind are met

### EntitiesOperations

Operations related to security entities (e.g., hosts, accounts, IP addresses).

**Key Methods**:
- `get(resource_group_name, workspace_name, entity_id, entity_types=None)`: Gets a specific entity
- `expand(resource_group_name, workspace_name, entities=None)`: Expands entity information

### EntitiesGetTimelineOperations

Operations related to timelines for entities.

**Key Methods**:
- `post(resource_group_name, workspace_name, entity_id, parameters)`: Gets a timeline for an entity

### EntitiesRelationsOperations

Operations related to relations between entities.

**Key Methods**:
- `list(resource_group_name, workspace_name, entity_id)`: Lists all relations for an entity
- `get(resource_group_name, workspace_name, entity_id, relation_name)`: Gets a specific entity relation

### BookmarksOperations

Operations related to investigation bookmarks.

**Key Methods**:
- `list(resource_group_name, workspace_name)`: Lists all bookmarks
- `get(resource_group_name, workspace_name, bookmark_id)`: Gets a specific bookmark
- `create_or_update(resource_group_name, workspace_name, bookmark_id, bookmark)`: Creates or updates a bookmark
- `delete(resource_group_name, workspace_name, bookmark_id)`: Deletes a bookmark

### BookmarkRelationsOperations

Operations related to relations between bookmarks and other entities.

**Key Methods**:
- `list(resource_group_name, workspace_name, bookmark_id)`: Lists all relations for a bookmark
- `get(resource_group_name, workspace_name, bookmark_id, relation_name)`: Gets a specific bookmark relation
- `create_or_update(resource_group_name, workspace_name, bookmark_id, relation_name, relation)`: Creates or updates a relation
- `delete(resource_group_name, workspace_name, bookmark_id, relation_name)`: Deletes a relation

### WatchlistsOperations

Operations related to watchlists in Sentinel.

**Key Methods**:
- `list(resource_group_name, workspace_name)`: Lists all watchlists
- `get(resource_group_name, workspace_name, watchlist_alias)`: Gets a specific watchlist
- `create_or_update(resource_group_name, workspace_name, watchlist_alias, watchlist)`: Creates or updates a watchlist
- `delete(resource_group_name, workspace_name, watchlist_alias)`: Deletes a watchlist

### WatchlistItemsOperations

Operations related to items in watchlists.

**Key Methods**:
- `list(resource_group_name, workspace_name, watchlist_alias)`: Lists all items in a watchlist
- `get(resource_group_name, workspace_name, watchlist_alias, watchlist_item_id)`: Gets a specific watchlist item
- `create_or_update(resource_group_name, workspace_name, watchlist_alias, watchlist_item_id, watchlist_item)`: Creates or updates a watchlist item
- `delete(resource_group_name, workspace_name, watchlist_alias, watchlist_item_id)`: Deletes a watchlist item

### ThreatIntelligenceIndicatorsOperations

Operations related to threat intelligence indicators.

**Key Methods**:
- `list(resource_group_name, workspace_name)`: Lists all threat intelligence indicators
- `get(resource_group_name, workspace_name, indicator_name)`: Gets a specific indicator
- `create_or_update(resource_group_name, workspace_name, indicator_name, indicator)`: Creates or updates an indicator
- `delete(resource_group_name, workspace_name, indicator_name)`: Deletes an indicator

### ThreatIntelligenceIndicatorMetricsOperations

Operations related to threat intelligence indicator metrics.

**Key Methods**:
- `collect(resource_group_name, workspace_name, filtering_criteria=None)`: Collects metrics for threat intelligence indicators

### IPGeodataOperations

Operations related to geolocation data for IP addresses.

**Key Methods**:
- `get(resource_group_name, workspace_name, ip)`: Gets geolocation data for an IP address

### DomainWhoisOperations

Operations related to WHOIS information for domains.

**Key Methods**:
- `get(resource_group_name, workspace_name, domain)`: Gets WHOIS data for a domain

### FileImportsOperations

Operations related to importing files into Sentinel.

**Key Methods**:
- `list(resource_group_name, workspace_name)`: Lists all file imports
- `get(resource_group_name, workspace_name, file_import_id)`: Gets a specific file import
- `create_or_update(resource_group_name, workspace_name, file_import_id, file_import)`: Creates or updates a file import
- `delete(resource_group_name, workspace_name, file_import_id)`: Deletes a file import

### MetadataOperations

Operations related to metadata in Sentinel.

**Key Methods**:
- `list(resource_group_name, workspace_name)`: Lists all metadata
- `get(resource_group_name, workspace_name, metadata_id)`: Gets specific metadata
- `put(resource_group_name, workspace_name, metadata_id, metadata)`: Creates or updates metadata
- `patch(resource_group_name, workspace_name, metadata_id, metadata_patch)`: Updates metadata
- `delete(resource_group_name, workspace_name, metadata_id)`: Deletes metadata

### OfficeConsentsOperations

Operations related to Office 365 consent grants for Sentinel.

**Key Methods**:
- `list(resource_group_name, workspace_name)`: Lists all office consents
- `get(resource_group_name, workspace_name, consent_id)`: Gets a specific office consent
- `create_or_update(resource_group_name, workspace_name, consent_id, office_consent)`: Creates or updates an office consent
- `delete(resource_group_name, workspace_name, consent_id)`: Deletes an office consent

### SentinelOnboardingStatesOperations

Operations related to onboarding state of Sentinel.

**Key Methods**:
- `list(resource_group_name, workspace_name)`: Lists all onboarding states
- `get(resource_group_name, workspace_name, sentinel_onboarding_state_id)`: Gets a specific onboarding state
- `create_or_update(resource_group_name, workspace_name, sentinel_onboarding_state_id, onboarding_state)`: Creates or updates an onboarding state
- `delete(resource_group_name, workspace_name, sentinel_onboarding_state_id)`: Deletes an onboarding state

### SecurityMLAnalyticsSettingsOperations

Operations related to machine learning analytics settings in Sentinel.

**Key Methods**:
- `list(resource_group_name, workspace_name)`: Lists all ML analytics settings
- `get(resource_group_name, workspace_name, setting_name)`: Gets a specific ML analytics setting
- `create_or_update(resource_group_name, workspace_name, setting_name, setting)`: Creates or updates an ML analytics setting
- `delete(resource_group_name, workspace_name, setting_name)`: Deletes an ML analytics setting

### SourceControlsOperations

Operations related to source control for Sentinel content.

**Key Methods**:
- `list(resource_group_name, workspace_name)`: Lists all source controls
- `get(resource_group_name, workspace_name, source_control_id)`: Gets a specific source control
- `create_or_update(resource_group_name, workspace_name, source_control_id, source_control)`: Creates or updates a source control
- `delete(resource_group_name, workspace_name, source_control_id)`: Deletes a source control

## Key Model Classes

### Incident

Represents a security incident in Sentinel.

**Key Properties**:
- `title`: The title of the incident
- `description`: The description of the incident
- `severity`: Incident severity (High, Medium, Low, Informational)
- `status`: Incident status (New, Active, Closed)
- `classification`: Incident classification (Undetermined, TruePositive, BenignPositive, FalsePositive)
- `owner`: Information about the incident assignee
- `labels`: List of labels relevant to the incident
- `first_activity_time_utc`: Time of the first activity in the incident
- `last_activity_time_utc`: Time of the last activity in the incident

### AlertRule

Base class for different types of alert rules.

**Derived Classes**:
- `ScheduledAlertRule`: Rules that run on a schedule
- `FusionAlertRule`: Rules that use Fusion technology to detect advanced threats
- `MicrosoftSecurityIncidentCreationAlertRule`: Rules that create incidents from Microsoft security alerts
- `NrtAlertRule`: Near-real-time alert rules
- `ThreatIntelligenceAlertRule`: Rules based on threat intelligence
- `MLBehaviorAnalyticsAlertRule`: Rules based on ML behavior analytics

### Entity

Base class for security entities in Sentinel.

**Derived Classes**:
- `AccountEntity`: User account entities
- `HostEntity`: Computer/device entities
- `IPEntity`: IP address entities
- `FileEntity`: File entities
- `ProcessEntity`: Process entities
- `UrlEntity`: URL entities
- `MailboxEntity`: Email mailbox entities
- `MailMessageEntity`: Email message entities
- `MailClusterEntity`: Email cluster entities
- `MalwareEntity`: Malware entities
- `FileHashEntity`: File hash entities
- `RegistryKeyEntity`: Registry key entities
- `RegistryValueEntity`: Registry value entities
- `AzureResourceEntity`: Azure resource entities
- `SecurityGroupEntity`: Security group entities
- `IoTDeviceEntity`: IoT device entities

### DataConnector

Base class for data sources that connect to Sentinel.

**Derived Classes**:
- `AADDataConnector`: Azure Active Directory data connector
- `ASCDataConnector`: Azure Security Center data connector
- `OfficeDataConnector`: Office 365 data connector
- `TIDataConnector`: Threat Intelligence data connector
- `TiTaxiiDataConnector`: TAXII Threat Intelligence data connector
- `MCASDataConnector`: Microsoft Cloud App Security data connector
- `MDATPDataConnector`: Microsoft Defender ATP data connector
- `Dynamics365DataConnector`: Dynamics 365 data connector
- `CodelessApiPollingDataConnector`: Codeless API polling data connector
- `CodelessUiDataConnector`: Codeless UI data connector
- `AwsCloudTrailDataConnector`: AWS CloudTrail data connector
- `AwsS3DataConnector`: AWS S3 data connector

### AutomationRule

Represents an automation rule in Sentinel.

**Key Properties**:
- `display_name`: The display name of the automation rule
- `order`: The order of the automation rule
- `triggering_logic`: The conditions that trigger the automation rule
- `actions`: The actions to perform when the rule is triggered
- `enabled`: Whether the rule is enabled

### Watchlist

Represents a watchlist in Sentinel.

**Key Properties**:
- `display_name`: The display name of the watchlist
- `source`: The source of the watchlist data
- `provider`: The provider of the watchlist
- `items_search_key`: The key to search for items in the watchlist
- `description`: The description of the watchlist

### Bookmark

Represents an investigation bookmark in Sentinel.

**Key Properties**:
- `display_name`: The display name of the bookmark
- `query`: The query that defines the bookmark
- `query_result`: The result of the query
- `notes`: Notes about the bookmark
- `labels`: Labels associated with the bookmark
- `created_by`: Information about who created the bookmark

## Important Enums

### IncidentSeverity
Severity levels for incidents:
- `High`: High severity
- `Medium`: Medium severity
- `Low`: Low severity
- `Informational`: Informational severity

### IncidentStatus
Status values for incidents:
- `New`: New incident
- `Active`: Incident being investigated
- `Closed`: Resolved incident

### IncidentClassification
Classification reasons for closed incidents:
- `Undetermined`: Undetermined classification
- `TruePositive`: Confirmed malicious activity
- `BenignPositive`: Suspicious but not malicious
- `FalsePositive`: False positive

### AlertRuleKind
Types of alert rules:
- `Scheduled`: Scheduled query rules
- `MicrosoftSecurityIncidentCreation`: Microsoft security alerts
- `Fusion`: Fusion alerts (advanced correlation)
- `NRT`: Near-real-time alerts
- `ThreatIntelligence`: Threat intelligence alerts
- `MLBehaviorAnalytics`: Machine learning behavior analytics alerts

### EntityKind
Types of security entities:
- `Account`: User accounts
- `Host`: Computers and devices
- `IP`: IP addresses
- `File`: Files
- `Process`: Processes
- `URL`: Web URLs
- `Mailbox`: Email mailboxes
- `MailMessage`: Email messages
- `MailCluster`: Email clusters
- And many other entity types

### DataConnectorKind
Types of data connectors:
- `AzureActiveDirectory`: Azure AD connector
- `AzureSecurityCenter`: Azure Security Center connector
- `Office365`: Office 365 connector
- `ThreatIntelligence`: Threat intelligence connector
- `ThreatIntelligenceTaxii`: TAXII threat intelligence connector
- `APIPolling`: API polling connector
- `GenericUI`: Generic UI connector
- And many other connector types

## Common Usage Examples

### Initialize the Client

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.securityinsight import SecurityInsights

# Authenticate using default credentials
credential = DefaultAzureCredential()
subscription_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

# Initialize the client
client = SecurityInsights(
    credential=credential,
    subscription_id=subscription_id
)
```

### List All Incidents

```python
# List all incidents in a workspace
incidents = client.incidents.list(
    resource_group_name="myResourceGroup",
    workspace_name="myWorkspace"
)

for incident in incidents:
    print(f"Incident: {incident.name}, Status: {incident.properties.status}, Severity: {incident.properties.severity}")
```

### Create or Update an Incident

```python
# Create or update an incident
response = client.incidents.create_or_update(
    resource_group_name="myResourceGroup",
    workspace_name="myWorkspace",
    incident_id="00000000-0000-0000-0000-000000000000",
    incident={
        "etag": '"0300bf09-0000-0000-0000-5c37296e0000"',
        "properties": {
            "title": "Security Incident",
            "description": "This is a security incident",
            "severity": "High",
            "status": "New",
            "owner": {
                "objectId": "2046feea-040d-4a46-9e2b-91c2941bfa70",
            },
            "firstActivityTimeUtc": "2023-01-01T00:00:00Z",
            "lastActivityTimeUtc": "2023-01-02T00:00:00Z",
        },
    },
)
```

### Create an Alert Rule

```python
# Create a scheduled alert rule
response = client.alert_rules.create_or_update(
    resource_group_name="myResourceGroup",
    workspace_name="myWorkspace",
    rule_id="00000000-0000-0000-0000-000000000000",
    alert_rule={
        "kind": "Scheduled",
        "etag": '"0300bf09-0000-0000-0000-5c37296e0000"',
        "properties": {
            "displayName": "Suspicious Activity Rule",
            "description": "Rule to detect suspicious activity",
            "severity": "Medium",
            "enabled": True,
            "query": "SecurityEvent | where EventID == 4624",
            "queryFrequency": "PT1H",
            "queryPeriod": "PT1H",
            "triggerOperator": "GreaterThan",
            "triggerThreshold": 0,
            "suppressionDuration": "PT1H",
            "suppressionEnabled": False,
            "tactics": ["InitialAccess", "Execution"],
            "alertDetailsOverride": {
                "alertDisplayNameFormat": "Suspicious login from {{Computer}}",
                "alertDescriptionFormat": "Suspicious login detected",
            },
            "incidentConfiguration": {
                "createIncident": True,
                "groupingConfiguration": {
                    "enabled": True,
                    "reopenClosedIncident": False,
                    "lookbackDuration": "PT5H",
                    "matchingMethod": "AllEntities",
                    "groupByEntities": ["Account", "IP"],
                },
            },
        },
    },
)
```

### Work with Data Connectors

```python
# List all data connectors
connectors = client.data_connectors.list(
    resource_group_name="myResourceGroup",
    workspace_name="myWorkspace"
)

for connector in connectors:
    print(f"Connector: {connector.name}, Kind: {connector.kind}")

# Create an Office 365 data connector
response = client.data_connectors.create_or_update(
    resource_group_name="myResourceGroup",
    workspace_name="myWorkspace",
    data_connector_id="00000000-0000-0000-0000-000000000000",
    connector={
        "kind": "Office365",
        "properties": {
            "tenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "dataTypes": {
                "exchange": {
                    "state": "Enabled"
                },
                "sharePoint": {
                    "state": "Enabled"
                },
                "teams": {
                    "state": "Enabled"
                }
            }
        }
    }
)
```

### Work with Entities

```python
# Get a specific entity
entity = client.entities.get(
    resource_group_name="myResourceGroup",
    workspace_name="myWorkspace",
    entity_id="00000000-0000-0000-0000-000000000000",
    entity_types=["Account", "Host"]
)

print(f"Entity: {entity.name}, Kind: {entity.kind}")

# Expand entity information
expanded_entity = client.entities.expand(
    resource_group_name="myResourceGroup",
    workspace_name="myWorkspace",
    entities={
        "entities": [
            {
                "id": "00000000-0000-0000-0000-000000000000",
                "kind": "Account"
            }
        ]
    }
)
```

### Working with Watchlists

```python
# Create a watchlist
response = client.watchlists.create_or_update(
    resource_group_name="myResourceGroup",
    workspace_name="myWorkspace",
    watchlist_alias="HighValueAssets",
    watchlist={
        "properties": {
            "displayName": "High Value Assets",
            "source": "Local file",
            "provider": "Microsoft",
            "itemsSearchKey": "Hostname",
            "description": "List of high value assets"
        }
    }
)

# Add an item to the watchlist
response = client.watchlist_items.create_or_update(
    resource_group_name="myResourceGroup",
    workspace_name="myWorkspace",
    watchlist_alias="HighValueAssets",
    watchlist_item_id="00000000-0000-0000-0000-000000000000",
    watchlist_item={
        "properties": {
            "itemsKeyValue": "server001",
            "properties": {
                "Hostname": "server001",
                "IPAddress": "10.0.0.1",
                "Owner": "IT Department",
                "Classification": "Critical"
            }
        }
    }
)
```

## Dependencies

The package depends on the following key components:

1. `azure-core`: For HTTP pipeline and core functionality
2. `azure-mgmt-core`: For ARM client functionality
3. `azure-identity`: For authentication (not a direct dependency but recommended for use)

## Additional Resources

- [Azure Sentinel Documentation](https://docs.microsoft.com/azure/sentinel/)
- [Azure Sentinel REST API Reference](https://docs.microsoft.com/rest/api/securityinsights/)
- [Azure SDK for Python Documentation](https://docs.microsoft.com/python/api/overview/azure/)
````

## File: docs/architecture/libraries/data-connector-visibility-summary.md
````markdown
# Data Connector Visibility and API Limitations in Azure Sentinel

## Overview
Azure Sentinel's data connector retrieval process is constrained by significant API limitations that impact the comprehensiveness of connector discovery and management.

## Connector Visibility Hierarchy

### Visible Connectors (Programmatically Retrievable)
1. **User-Deployed Connectors**
   - Created via ARM (Azure Resource Manager) templates
   - Deployed through Azure Functions
   - Configured using Logic Apps
   - Manually configured by security administrators

### Hidden/Invisible Connectors
1. **Built-in Connectors**
   - Examples:
     - Azure Activity
     - Microsoft Threat Protection
     - Azure Active Directory
   - Fundamental to core security monitoring
   - Cannot be retrieved via standard API calls

2. **Gallery-Deployed Connectors**
   - Pre-configured connectors from Microsoft's security ecosystem
   - Examples:
     - Cisco Umbrella
     - ZScaler
     - Various third-party security solutions
   - Typically added through content hub

## API Limitations
- Current Azure Sentinel APIs only expose user-deployed connectors
- No direct method to list all available connectors, including built-in and gallery connectors
- Limited metadata retrieval for existing connectors

## Workaround Strategies
1. **Ingestion Volume Analysis**
   - Use KQL queries to identify active data sources
   - Examine `Usage` and `CommonSecurityLog` tables
   - Track data ingestion patterns

2. **Manual Discovery**
   - Azure Portal > Sentinel > Data Connectors
   - Provides comprehensive view of all connectors
   - Includes built-in and gallery connectors not visible via API

## Technical Implications
- Security automation scripts must account for incomplete connector listings
- Manual verification recommended for comprehensive security configuration
- Potential gaps in automated connector management

## Best Practices
- Do not rely solely on API-retrieved connector lists
- Cross-reference API results with portal configurations
- Implement additional validation steps in security tooling
- Maintain manual oversight of data connector configurations

## Future Outlook
- Ongoing improvements expected in Azure Sentinel's API capabilities
- Potential future enhancements to connector discovery mechanisms

## Warning for Developers
⚠️ **Important**: Any programmatic connector discovery should include explicit warnings about the limitations of the retrieved data.

## Recommended Disclaimer
"Connector list may be incomplete. Built-in and gallery-deployed connectors are not included due to Azure API limitations. Manual verification recommended."
````

## File: docs/architecture/libraries/MCP Python SDK Readme.md
````markdown
# MCP Python SDK

<div align="center">

<strong>Python implementation of the Model Context Protocol (MCP)</strong>

[![PyPI][pypi-badge]][pypi-url]
[![MIT licensed][mit-badge]][mit-url]
[![Python Version][python-badge]][python-url]
[![Documentation][docs-badge]][docs-url]
[![Specification][spec-badge]][spec-url]
[![GitHub Discussions][discussions-badge]][discussions-url]

</div>

<!-- omit in toc -->
## Table of Contents

- [MCP Python SDK](#mcp-python-sdk)
  - [Overview](#overview)
  - [Installation](#installation)
    - [Adding MCP to your python project](#adding-mcp-to-your-python-project)
    - [Running the standalone MCP development tools](#running-the-standalone-mcp-development-tools)
  - [Quickstart](#quickstart)
  - [What is MCP?](#what-is-mcp)
  - [Core Concepts](#core-concepts)
    - [Server](#server)
    - [Resources](#resources)
    - [Tools](#tools)
    - [Prompts](#prompts)
    - [Images](#images)
    - [Context](#context)
  - [Running Your Server](#running-your-server)
    - [Development Mode](#development-mode)
    - [Claude Desktop Integration](#claude-desktop-integration)
    - [Direct Execution](#direct-execution)
    - [Mounting to an Existing ASGI Server](#mounting-to-an-existing-asgi-server)
  - [Examples](#examples)
    - [Echo Server](#echo-server)
    - [SQLite Explorer](#sqlite-explorer)
  - [Advanced Usage](#advanced-usage)
    - [Low-Level Server](#low-level-server)
    - [Writing MCP Clients](#writing-mcp-clients)
    - [MCP Primitives](#mcp-primitives)
    - [Server Capabilities](#server-capabilities)
  - [Documentation](#documentation)
  - [Contributing](#contributing)
  - [License](#license)

[pypi-badge]: https://img.shields.io/pypi/v/mcp.svg
[pypi-url]: https://pypi.org/project/mcp/
[mit-badge]: https://img.shields.io/pypi/l/mcp.svg
[mit-url]: https://github.com/modelcontextprotocol/python-sdk/blob/main/LICENSE
[python-badge]: https://img.shields.io/pypi/pyversions/mcp.svg
[python-url]: https://www.python.org/downloads/
[docs-badge]: https://img.shields.io/badge/docs-modelcontextprotocol.io-blue.svg
[docs-url]: https://modelcontextprotocol.io
[spec-badge]: https://img.shields.io/badge/spec-spec.modelcontextprotocol.io-blue.svg
[spec-url]: https://spec.modelcontextprotocol.io
[discussions-badge]: https://img.shields.io/github/discussions/modelcontextprotocol/python-sdk
[discussions-url]: https://github.com/modelcontextprotocol/python-sdk/discussions

## Overview

The Model Context Protocol allows applications to provide context for LLMs in a standardized way, separating the concerns of providing context from the actual LLM interaction. This Python SDK implements the full MCP specification, making it easy to:

- Build MCP clients that can connect to any MCP server
- Create MCP servers that expose resources, prompts and tools
- Use standard transports like stdio and SSE
- Handle all MCP protocol messages and lifecycle events

## Installation

### Adding MCP to your python project

We recommend using [uv](https://docs.astral.sh/uv/) to manage your Python projects. 

If you haven't created a uv-managed project yet, create one:

   ```bash
   uv init mcp-server-demo
   cd mcp-server-demo
   ```

   Then add MCP to your project dependencies:

   ```bash
   uv add "mcp[cli]"
   ```

Alternatively, for projects using pip for dependencies:
```bash
pip install "mcp[cli]"
```

### Running the standalone MCP development tools

To run the mcp command with uv:

```bash
uv run mcp
```

## Quickstart

Let's create a simple MCP server that exposes a calculator tool and some data:

```python
# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"
```

You can install this server in [Claude Desktop](https://claude.ai/download) and interact with it right away by running:
```bash
mcp install server.py
```

Alternatively, you can test it with the MCP Inspector:
```bash
mcp dev server.py
```

## What is MCP?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io) lets you build servers that expose data and functionality to LLM applications in a secure, standardized way. Think of it like a web API, but specifically designed for LLM interactions. MCP servers can:

- Expose data through **Resources** (think of these sort of like GET endpoints; they are used to load information into the LLM's context)
- Provide functionality through **Tools** (sort of like POST endpoints; they are used to execute code or otherwise produce a side effect)
- Define interaction patterns through **Prompts** (reusable templates for LLM interactions)
- And more!

## Core Concepts

### Server

The FastMCP server is your core interface to the MCP protocol. It handles connection management, protocol compliance, and message routing:

```python
# Add lifespan support for startup/shutdown with strong typing
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass

from fake_database import Database  # Replace with your actual DB type

from mcp.server.fastmcp import Context, FastMCP

# Create a named server
mcp = FastMCP("My App")

# Specify dependencies for deployment and development
mcp = FastMCP("My App", dependencies=["pandas", "numpy"])


@dataclass
class AppContext:
    db: Database


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""
    # Initialize on startup
    db = await Database.connect()
    try:
        yield AppContext(db=db)
    finally:
        # Cleanup on shutdown
        await db.disconnect()


# Pass lifespan to server
mcp = FastMCP("My App", lifespan=app_lifespan)


# Access type-safe lifespan context in tools
@mcp.tool()
def query_db(ctx: Context) -> str:
    """Tool that uses initialized resources"""
    db = ctx.request_context.lifespan_context["db"]
    return db.query()
```

### Resources

Resources are how you expose data to LLMs. They're similar to GET endpoints in a REST API - they provide data but shouldn't perform significant computation or have side effects:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My App")


@mcp.resource("config://app")
def get_config() -> str:
    """Static configuration data"""
    return "App configuration here"


@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: str) -> str:
    """Dynamic user data"""
    return f"Profile data for user {user_id}"
```

### Tools

Tools let LLMs take actions through your server. Unlike resources, tools are expected to perform computation and have side effects:

```python
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My App")


@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    return weight_kg / (height_m**2)


@mcp.tool()
async def fetch_weather(city: str) -> str:
    """Fetch current weather for a city"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.weather.com/{city}")
        return response.text
```

### Prompts

Prompts are reusable templates that help LLMs interact with your server effectively:

```python
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("My App")


@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:

{code}"


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]
```

### Images

FastMCP provides an `Image` class that automatically handles image data:

```python
from mcp.server.fastmcp import FastMCP, Image
from PIL import Image as PILImage

mcp = FastMCP("My App")


@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")
```

### Context

The Context object gives your tools and resources access to MCP capabilities:

```python
from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP("My App")


@mcp.tool()
async def long_task(files: list[str], ctx: Context) -> str:
    """Process multiple files with progress tracking"""
    for i, file in enumerate(files):
        ctx.info(f"Processing {file}")
        await ctx.report_progress(i, len(files))
        data, mime_type = await ctx.read_resource(f"file://{file}")
    return "Processing complete"
```

## Running Your Server

### Development Mode

The fastest way to test and debug your server is with the MCP Inspector:

```bash
mcp dev server.py

# Add dependencies
mcp dev server.py --with pandas --with numpy

# Mount local code
mcp dev server.py --with-editable .
```

### Claude Desktop Integration

Once your server is ready, install it in Claude Desktop:

```bash
mcp install server.py

# Custom name
mcp install server.py --name "My Analytics Server"

# Environment variables
mcp install server.py -v API_KEY=abc123 -v DB_URL=postgres://...
mcp install server.py -f .env
```

### Direct Execution

For advanced scenarios like custom deployments:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My App")

if __name__ == "__main__":
    mcp.run()
```

Run it with:
```bash
python server.py
# or
mcp run server.py
```

### Mounting to an Existing ASGI Server

You can mount the SSE server to an existing ASGI server using the `sse_app` method. This allows you to integrate the SSE server with other ASGI applications.

```python
from starlette.applications import Starlette
from starlette.routing import Mount, Host
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("My App")

# Mount the SSE server to the existing ASGI server
app = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),
    ]
)

# or dynamically mount as host
app.router.routes.append(Host('mcp.acme.corp', app=mcp.sse_app()))
```

For more information on mounting applications in Starlette, see the [Starlette documentation](https://www.starlette.io/routing/#submounting-routes).

## Examples

### Echo Server

A simple server demonstrating resources, tools, and prompts:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Echo")


@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"


@mcp.tool()
def echo_tool(message: str) -> str:
    """Echo a message as a tool"""
    return f"Tool echo: {message}"


@mcp.prompt()
def echo_prompt(message: str) -> str:
    """Create an echo prompt"""
    return f"Please process this message: {message}"
```

### SQLite Explorer

A more complex example showing database integration:

```python
import sqlite3

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("SQLite Explorer")


@mcp.resource("schema://main")
def get_schema() -> str:
    """Provide the database schema as a resource"""
    conn = sqlite3.connect("database.db")
    schema = conn.execute("SELECT sql FROM sqlite_master WHERE type='table'").fetchall()
    return "
".join(sql[0] for sql in schema if sql[0])


@mcp.tool()
def query_data(sql: str) -> str:
    """Execute SQL queries safely"""
    conn = sqlite3.connect("database.db")
    try:
        result = conn.execute(sql).fetchall()
        return "
".join(str(row) for row in result)
    except Exception as e:
        return f"Error: {str(e)}"
```

## Advanced Usage

### Low-Level Server

For more control, you can use the low-level server implementation directly. This gives you full access to the protocol and allows you to customize every aspect of your server, including lifecycle management through the lifespan API:

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fake_database import Database  # Replace with your actual DB type

from mcp.server import Server


@asynccontextmanager
async def server_lifespan(server: Server) -> AsyncIterator[dict]:
    """Manage server startup and shutdown lifecycle."""
    # Initialize resources on startup
    db = await Database.connect()
    try:
        yield {"db": db}
    finally:
        # Clean up on shutdown
        await db.disconnect()


# Pass lifespan to server
server = Server("example-server", lifespan=server_lifespan)


# Access lifespan context in handlers
@server.call_tool()
async def query_db(name: str, arguments: dict) -> list:
    ctx = server.request_context
    db = ctx.lifespan_context["db"]
    return await db.query(arguments["query"])
```

The lifespan API provides:
- A way to initialize resources when the server starts and clean them up when it stops
- Access to initialized resources through the request context in handlers
- Type-safe context passing between lifespan and request handlers

```python
import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# Create a server instance
server = Server("example-server")


@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    return [
        types.Prompt(
            name="example-prompt",
            description="An example prompt template",
            arguments=[
                types.PromptArgument(
                    name="arg1", description="Example argument", required=True
                )
            ],
        )
    ]


@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    if name != "example-prompt":
        raise ValueError(f"Unknown prompt: {name}")

    return types.GetPromptResult(
        description="Example prompt",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text="Example prompt text"),
            )
        ],
    )


async def run():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="example",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
```

### Writing MCP Clients

The SDK provides a high-level client interface for connecting to MCP servers:

```python
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["example_server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)


# Optional: create a sampling callback
async def handle_sampling_message(
    message: types.CreateMessageRequestParams,
) -> types.CreateMessageResult:
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text="Hello, world! from model",
        ),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
    )


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write, sampling_callback=handle_sampling_message
        ) as session:
            # Initialize the connection
            await session.initialize()

            # List available prompts
            prompts = await session.list_prompts()

            # Get a prompt
            prompt = await session.get_prompt(
                "example-prompt", arguments={"arg1": "value"}
            )

            # List available resources
            resources = await session.list_resources()

            # List available tools
            tools = await session.list_tools()

            # Read a resource
            content, mime_type = await session.read_resource("file://some/path")

            # Call a tool
            result = await session.call_tool("tool-name", arguments={"arg1": "value"})


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
```

### MCP Primitives

The MCP protocol defines three core primitives that servers can implement:

| Primitive | Control               | Description                                         | Example Use                  |
|-----------|-----------------------|-----------------------------------------------------|------------------------------|
| Prompts   | User-controlled       | Interactive templates invoked by user choice        | Slash commands, menu options |
| Resources | Application-controlled| Contextual data managed by the client application   | File contents, API responses |
| Tools     | Model-controlled      | Functions exposed to the LLM to take actions        | API calls, data updates      |

### Server Capabilities

MCP servers declare capabilities during initialization:

| Capability  | Feature Flag                 | Description                        |
|-------------|------------------------------|------------------------------------|
| `prompts`   | `listChanged`                | Prompt template management         |
| `resources` | `subscribe`<br/>`listChanged`| Resource exposure and updates      |
| `tools`     | `listChanged`                | Tool discovery and execution       |
| `logging`   | -                            | Server logging configuration       |
| `completion`| -                            | Argument completion suggestions    |

## Documentation

- [Model Context Protocol documentation](https://modelcontextprotocol.io)
- [Model Context Protocol specification](https://spec.modelcontextprotocol.io)
- [Officially supported servers](https://github.com/modelcontextprotocol/servers)

## Contributing

We are passionate about supporting contributors of all levels of experience and would love to see you get involved in the project. See the [contributing guide](CONTRIBUTING.md) to get started.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
````

## File: docs/architecture/backend-structure.md
````markdown
# Backend Structure
## Microsoft Sentinel MCP Server

### 1. Data Models

#### Server Context Model

```python
@dataclass
class AzureServicesContext:
    """Container for Azure service clients and credentials"""
    
    credential: Optional[DefaultAzureCredential]  # Azure authentication credentials
    logs_client: Optional[LogsQueryClient]        # Client for querying logs
    metrics_client: Optional[MetricsQueryClient]  # Client for querying metrics
    security_insights_client: Optional[SecurityInsights]  # Client for security insights
    loganalytics_client: Optional[LogAnalyticsManagementClient]  # Client for workspace management
    workspace_id: str                             # Azure Log Analytics workspace ID
    subscription_id: str                          # Azure subscription ID
    resource_group: str                           # Azure resource group name
    config: Dict[str, Any]                        # Additional configuration values
```

#### Query Models

```python
@dataclass
class QueryRequest:
    """Model for KQL query requests"""
    
    query: str                      # The KQL query text
    timespan: Union[str, timedelta] # Time period for query (e.g., "1d", "PT1H")
    workspace_id: str               # Target workspace ID
    include_statistics: bool = False # Whether to include query statistics
    include_visualization: bool = False # Whether to include visualization data
    server_timeout: Optional[int] = None # Server-side timeout in seconds
```

```python
@dataclass
class QueryResponse:
    """Model for KQL query results"""
    
    tables: List[Dict[str, Any]]    # Result tables with columns and rows
    statistics: Optional[Dict[str, Any]] = None # Query performance statistics
    visualization: Optional[Dict[str, Any]] = None # Visualization data if requested
    error: Optional[str] = None     # Error message if query failed
    partial: bool = False           # Whether results are partial
```

#### Incident Models

```python
@dataclass
class SecurityIncidentListing:
    """Model for security incident list results"""
    
    incidents: List[Dict[str, Any]] # List of incidents with metadata
    total_count: int                # Total number of incidents (for pagination)
    skip_token: Optional[str] = None # Token for retrieving next page
```

#### Task Management Models

```python
@dataclass
class TaskInfo:
    """Information about a running task"""
    
    id: str                     # Unique identifier for the task
    name: str                   # Human-readable name of the task
    start_time: datetime        # When the task was started
    is_complete: bool = False   # Whether the task has completed
    result: Any = None          # The result of the task (if complete)
    error: Optional[str] = None # Error message if task failed
```

### 2. API Contracts

#### Resources API

- **List Resources**
  - URL: (MCP protocol - resources/list)
  - Method: MCP request
  - Parameters: None
  - Response: List of available resources with URIs, names, and descriptions
  - Authentication: None (MCP protocol handles authentication)

- **Read Resource**
  - URL: (MCP protocol - resources/read)
  - Method: MCP request
  - Parameters: 
    - uri: String (resource URI to read)
  - Response: Resource content with mime type
  - Authentication: None (MCP protocol handles authentication)
  - Error responses:
    - Resource not found
    - Invalid URI format
    - Access denied

#### Tools API

- **List Tools**
  - URL: (MCP protocol - tools/list)
  - Method: MCP request
  - Parameters: None
  - Response: List of available tools with names, descriptions, and input schemas
  - Authentication: None (MCP protocol handles authentication)

- **Call Tool**
  - URL: (MCP protocol - tools/call)
  - Method: MCP request
  - Parameters:
    - name: String (tool name to call)
    - arguments: Object (tool-specific parameters)
  - Response: Tool execution results or error
  - Authentication: None (MCP protocol handles authentication)
  - Error responses:
    - Tool not found
    - Invalid parameters
    - Execution error
    - Azure authentication error
    - Access denied

#### Prompts API

- **List Prompts**
  - URL: (MCP protocol - prompts/list)
  - Method: MCP request
  - Parameters: None
  - Response: List of available prompts with names, descriptions, and argument schemas
  - Authentication: None (MCP protocol handles authentication)

- **Get Prompt**
  - URL: (MCP protocol - prompts/get)
  - Method: MCP request
  - Parameters:
    - name: String (prompt name to get)
    - arguments: Object (prompt-specific parameters)
  - Response: Prompt messages
  - Authentication: None (MCP protocol handles authentication)
  - Error responses:
    - Prompt not found
    - Invalid parameters

### 3. Service Architecture

#### Core Server Component
- **FastMCP Server**: Main server instance that handles MCP protocol communication
  - Manages the server lifecycle and component registration
  - Dispatches MCP requests to the appropriate handlers
  - Provides the context for all operations

#### Resource Components
- **KQL Reference Resources**: Provides documentation on KQL syntax and operators
- **Examples Resources**: Provides example KQL queries for common scenarios
- **Tables Resources**: Provides information about Sentinel data tables

#### Tool Components
- **Query Tools**: Executes and validates KQL queries
  - KQL validation using Kusto.Language library
  - Query execution through Azure Monitor API
- **Incident Tools**: Manages security incidents
  - Lists incidents with filtering and pagination
  - Gets detailed incident information
- **Workspace Tools**: Manages workspace information
  - Gets workspace details and configuration
- **Data Connector Tools**: Manages data connectors
  - Lists available data connectors
  - Gets connector details

#### Prompt Components
- **Investigation Prompts**: Templates for security investigations
- **Query Building Prompts**: Templates for building KQL queries
- **Workspace Visualization Prompts**: Templates for visualizing workspace information

#### Utility Components
- **Task Manager**: Manages asynchronous tasks
  - Tracks running tasks
  - Handles timeouts and cancellation
  - Provides progress reporting
- **KQL Validator**: Validates KQL query syntax
  - Uses Kusto.Language library
  - Provides detailed error messages
- **Connection Tester**: Tests Azure connectivity
  - Validates credentials
  - Checks workspace access

### 4. Storage Strategy

The server is primarily stateless and doesn't maintain persistent storage. Data is retrieved from Azure services as needed.

- **In-Memory Storage**:
  - Running tasks are tracked in memory
  - Cached validation results (short-term)
  - Connection state during server lifetime

- **Azure Storage**:
  - All permanent data is stored in Microsoft Sentinel/Log Analytics
  - Query results are retrieved directly from Azure
  - Incidents and other security data remain in Azure

### 5. Access Control Policies

- **Azure Authentication**:
  - All Azure interactions use DefaultAzureCredential
  - Service principals require Reader role for Log Analytics workspace
  - Incident management requires Security Reader role for Sentinel
  - Writing to incidents requires Security Responder role

- **Local Access Control**:
  - Server assumes the local user should have full access to functionality
  - No additional authentication layer in the server itself
  - Relies on MCP client for user authentication

### 6. Integration Patterns

- **Azure Integration**:
  - Uses official Azure SDKs for all Azure service communication
  - Follows Azure authentication best practices
  - Handles Azure API errors and retries

- **MCP Protocol Integration**:
  - Implements MCP protocol specification for client-server communication
  - Supports multiple transports (stdio, SSE)
  - Provides standardized resource, tool, and prompt interfaces

- **Python.NET Integration**:
  - Uses Python.NET bridge to access .NET libraries
  - Loads Kusto.Language DLL for KQL validation
  - Fallback mechanisms when .NET components are unavailable

### 7. Caching Strategy

- **KQL Validation Cache**:
  - Caches validation results for identical queries briefly
  - Invalidates cache when server detects schema changes

- **Schema Information Cache**:
  - Caches table schemas during server lifetime
  - Refreshes periodically to catch schema changes

- **No Result Caching**:
  - Query results are not cached to ensure freshness
  - Each query executes against Azure for current data

### 8. Scaling Considerations

- **Concurrent Operations**:
  - Uses Python async to handle multiple operations concurrently
  - Task manager limits maximum concurrent Azure operations
  - Implements backoff for rate-limited Azure APIs

- **Resource Consumption**:
  - Monitors memory usage for large query results
  - Implements timeouts for long-running operations
  - Cancels abandoned tasks to free resources

### 9. Transaction Management

- **Azure Transaction Guarantees**:
  - Relies on Azure services for transactional guarantees
  - Query operations are inherently read-only
  - Incident updates use Azure API's transaction handling

- **Error Handling**:
  - Catches exceptions during operations
  - Provides clear error messages in responses
  - Avoids partial updates where possible
  - Implements cleanup for failed operations

- **State Management**:
  - Maintains minimal mutable state
  - Uses immutable data structures where possible
  - Isolates side effects to specific components
````

## File: docs/architecture/implementation-plan.md
````markdown
# Implementation Plan
## Microsoft Sentinel MCP Server

This implementation plan provides a step-by-step guide for developing the Microsoft Sentinel MCP Server. Each step builds on previous ones, creating a functional server incrementally.

### Step 1: Project Initialization [Done]
Create the basic project structure and setup files.
- Create project directory: `mkdir microsoft-sentinel-mcp-server`
- Navigate to project directory: `cd microsoft-sentinel-mcp-server`
- Initialize Python virtual environment: `uv venv`
- Create basic project structure with empty directories:
  - `mkdir resources tools prompts utilities`
  - `touch __init__.py server.py main.py`

### Step 2: Setup Basic Configuration [Done]
Create configuration and project definition files.
- Create `pyproject.toml` with project metadata and dependencies
- Create `.gitignore` for Python projects
- Create `README.md` with project overview
- Create `.env.example` file for environment variables template

### Step 3: Initialize MCP Server Framework [Done]
Create the basic server skeleton with MCP.
- Edit `server.py` to create basic FastMCP instance
- Add server lifespan function with context manager
- Add dummy data to test server initialization

### Step 4: Add Utility Components [Done]
Create utility modules for common functionality.
- Create `utilities/logging.py` for centralised logging configuration
- Create `utilities/task_manager.py` for async task management
- Add basic error handling and standard logging formats

### Step 5: Create Azure Authentication [Done]
Implement Azure authentication components.
- Create Azure service context data class in `server.py`
- Implement DefaultAzureCredential initialisation
- Add environment variable loading for Azure credentials
- Add error handling for authentication failures

### Step 6: Add Connection Testing [Done]
Create connection testing functionality.
- Create `utilities/connection_test.py` module
- Implement tests for Azure credentials
- Add tests for Log Analytics workspace access
- Add tests for Security Insights access

### Step 7: Create Component Loader [Done]
Create dynamic component loading system.
- Create `register_components.py` file
- Implement resource and tool discovery functions
- Add error handling for component loading
- Add logging for loaded components

### Step 8: Basic KQL Validation [Done]
Implement KQL validation utilities.
- Create `utilities/kql_validator.py` module
- Implement Kusto.Language library integration
- Add fallback for environments without .NET
- Create validation helper functions

### Step 9: DLL Download Utility [Done]
Create utilities for loading external dependencies.
- Create `download_dll.py` for fetching Kusto.Language DLL
- Add version checking and download functions
- Implement post-installation hooks
- Add error handling for download failures

### Step 10: Role and Permissions Check [In Progress]
Implement a robust role and permissions check utility using the Azure SDK (not direct REST API calls). The utility should:
- Retrieve role assignments for the current authenticated identity using the SDK.
- For each assignment, fetch role definition details and extract role name, description, and scope.
- Detect 'read' roles using improved logic (patterns: 'reader', 'read', 'monitor.*read') and check for special Sentinel/Log Analytics read roles.
- Track and summarize Sentinel read roles, Log Analytics read roles, total roles, and read-access scopes.
- Return workspace details, all role assignments, and a permissions assessment (including whether required read access is present).
- Log key actions and handle errors robustly.
- Reference: see prior implementation using direct REST calls for logic requirements; this step must use the official Azure SDK for all resource and role queries.


### Step 11: Basic KQL Resources [Done]
Create fundamental KQL reference resources.
- Create `resources/kql_basics.py` with KQL syntax guide
- Create `resources/kql_operators.py` with operator documentation
- Create `resources/kql_examples.py` with example queries
- Add resource registration functions

### Step 12: Table Reference Resources [Done]
Create resources for table information.
- Create resource with table listings and schemas
- Add documentation for common fields
- Include data type information
- Add registration for these resources

### Step 13: Basic KQL Validation Tool [Done]
Create the KQL validation tool.
- Create `tools/kql_tools.py` module
- Implement query validation tool
- Add detailed error reporting
- Register the validation tool with the server

### Step 14: Query Execution Tool [Done]
Create the KQL query execution tool.
- Create `tools/query_tools.py` module
- Implement query execution using Azure Monitor
- Add parameter validation and transformation
- Register the query tools with the server

### Step 15: Table Management Tools [Done]
Create tools for working with tables.
- Create `tools/table_tools.py` module
- Implement table listing functionality
- Add schema retrieval tool
- Register table tools with the server

### Step 16: Incident Management Tools [Done]
Create security incident management tools.
- Create `tools/incident_tools.py` module
- Implement incident listing with filtering
- Add incident detail retrieval
- Register incident tools with the server

### Step 17: Data Connector Tools [Done]
Create data connector management tools.
- Create `tools/data_connector_tools.py` module
- Implement connector listing functionality
- Add connector detail retrieval
- Register connector tools with the server

### Step 20: Workbook Tools
Create workbook management tools.
- Create `tools/workbook_tools.py` module
- Implement `sentinel_workbook_list` tool for listing available workbooks
- Implement `sentinel_workbook_get` tool for getting workbook details
- Register workbook tools with the server

### Step 21: Analytics Tools [Done]
Create analytics rule management tools.
- Create `tools/analytics_tools.py` module
- Implement `sentinel_analytics_rule_list` tool for listing analytics rules
- Implement `sentinel_analytics_rule_get` tool for getting rule details
- Register analytics tools with the server

### Step 25: Repository Tools
Create repository management tools.
- Create `tools/repository_tools.py` module
- Implement `sentinel_repository_list` tool for listing content repositories
- Implement `sentinel_repository_get` tool for getting repository details
- Register repository tools with the server

### Step 26: Summary Tools [Done]
Create summary rules tools.
- Create `tools/summary_tools.py` module
- Implement summary rule listing tool
- Add summary rule detail retrieval
- Register summary tools with the server

### Step 30: KQL Query Building Prompts [Done]
Create KQL query building prompts.
- Create `prompts/kql_builder.py` module
- Implement detection query builder prompt
- Add advanced query builder prompt
- Register query building prompts with the server

### Step 31: Workspace Visualization Prompts [Done]
Create workspace visualisation prompts.
- Create `prompts/workspace_visualisation.py` module
- Implement workspace visualisation logic
- Register workspace visualisation prompts with the server

### Step 32: Error Handling Improvements
Enhance error handling throughout the codebase.
- Add detailed error messages for common failures
- Implement graceful degradation for services
- Add retry logic for transient errors
- Ensure user-friendly error messages

### Step 33: Documentation Improvements
Add comprehensive documentation.
- Update README.md with detailed usage information
- Add docstrings to all functions and classes
- Create CONTRIBUTING.md for development guidelines
- Add usage examples

### Step 34: Type Hint Improvements
Enhance type hints for better IDE support and validation.
- Add detailed type annotations to all functions
- Create custom type definitions where needed
- Validate type correctness with mypy
- Fix any type-related issues

### Step 35: Testing Infrastructure
Create basic testing infrastructure.
- Create `tests` directory
- Add unit test framework for utilities
- Create mock Azure services for testing
- Add test helper functions

### Step 36: Unit Tests for Utilities
Add unit tests for utility functions.
- Create tests for task manager
- Add tests for KQL validator
- Create tests for logging utilities
- Add tests for Azure SDK utilities

### Step 37: Testing Resources
Add tests for MCP resources.
- Create tests for resource loading
- Add tests for resource content
- Verify resource registration
- Test dynamic resource loading

### Step 38: Testing Tools
Add tests for MCP tools.
- Create tests for KQL tools
- Add tests for incident tools
- Create tests for connection testing
- Verify tool parameters and error handling

### Step 39: Testing Prompts
Add tests for MCP prompts.
- Create tests for prompt registration
- Add tests for prompt arguments
- Verify prompt message generation
- Test prompt error conditions

### Step 40: Integration Testing
Create integration tests for connected components.
- Add tests for server initialisation
- Create tests for Azure connectivity
- Add end-to-end tool execution tests
- Verify resource and tool interaction

### Step 41: Performance Optimization
Optimize performance-critical components.
- Add caching for frequent operations
- Optimize query execution
- Improve parallel task handling
- Monitor and reduce memory usage

### Step 42: Security Review
Review and enhance security measures.
- Audit credential handling
- Review input validation
- Check for sensitive data exposure
- Verify secure Azure connections

### Step 43: Code Quality Improvements
Enhance overall code quality.
- Run linters (flake8, pylint) and fix issues
- Apply code formatting with Black
- Sort imports with isort
- Address any code smells or complexity issues

### Step 44: Implement Logging Enhancements
Improve logging for operations monitoring.
- Add structured logging
- Implement log levels for different scenarios
- Add request tracing
- Ensure sensitive data isn't logged

### Step 45: Add Progress Reporting
Implement progress reporting for long-running operations.
- Add progress callbacks for query execution
- Implement operation status tracking
- Add estimated time remaining calculations
- Ensure consistent progress update format

### Step 46: Claude Desktop Integration
Ensure smooth integration with Claude Desktop.
- Test installation via mcp CLI
- Add custom naming options
- Verify environment variable passing
- Ensure proper shutdown handling

### Step 47: SSE Transport Support
Add Server-Sent Events transport support.
- Implement SSE transport handler
- Add transport auto-detection
- Verify message routing
- Test with SSE clients

### Step 48: Advanced Error Recovery
Enhance error recovery mechanisms.
- Add automatic reconnection for Azure services
- Implement graceful service degradation
- Add background recovery attempts
- Improve error diagnostics

### Step 49: Query Result Formatting
Improve query result presentation.
- Add pretty formatting for results
- Implement result truncation for large datasets
- Add statistics formatting
- Create human-readable error formatting

### Step 50: Authentication Improvements
Enhance authentication flexibility.
- Add credential caching
- Implement token refresh handling
- Add interactive login fallback
- Improve authentication error messages

## Caching Layer (Workspace, Table, Schema)

To optimize performance and reduce redundant Azure API calls, the Sentinel MCP Server implements a caching layer for key data retrieval endpoints:

- **Workspace Metadata**: Caches workspace info API responses per workspace.
- **Table Listings**: Caches the list of tables per workspace and filter pattern.
- **Table Schemas**: Caches the schema for each table per workspace.

### Implementation Details
- The cache is implemented using a thread-safe singleton in `utilities/cache.py`, based on `cachetools.TTLCache`.
- Default TTL (time-to-live) is 10 minutes. Entries are evicted automatically after this period.
- Cache keys are namespaced for clarity and safety:  
  - `workspace:{workspace_id}`  
  - `tables:{workspace_id}:{filter_pattern}`  
  - `schema:{workspace_id}:{table_name}`
- The cache is integrated directly into the relevant tool functions (`get_workspace_info`, `list_tables`, `get_table_schema`).

### Invalidation Strategy
- **Automatic:** Entries expire after the TTL (10 minutes).
- **Manual:** The cache can be fully cleared at runtime by calling `cache.clear()` on the singleton instance in `utilities/cache.py` (e.g., via a debug endpoint or Python shell).
- **Mutation-aware:** If you implement tools that mutate workspace or table state, you MUST clear the cache or invalidate affected keys after mutation to avoid serving stale data.

### Extensibility
- TTL and cache size are configurable in `utilities/cache.py`.
- For advanced scenarios, pattern-based invalidation or event-driven cache clearing can be added.

### Example Usage

```python
from utilities.cache import cache

# Get from cache
result = cache.get("tables:workspace123:")

# Set in cache
cache.set("tables:workspace123:", my_table_list)

# Clear cache (manual invalidation)
cache.clear()
```

### File Structure Specifications

```
microsoft-sentinel-mcp-server/
├── .env.example                 # Environment variable template
├── .gitignore                   # Git ignore patterns
├── __init__.py                  # Package initialisation
├── download_dll.py              # Kusto.Language DLL downloader
├── main.py                      # Entry point script
├── post_install.py              # Post-installation script
├── pyproject.toml               # Project metadata and dependencies
├── README.md                    # Project documentation
├── register_components.py       # Component registration utilities
├── server.py                    # Main server implementation
├── setup.py                     # Setup script (minimal, defers to pyproject.toml)
├── prompts/                     # Prompt templates
│   ├── __init__.py              # Package initialisation
│   ├── kql_builder.py           # KQL query building prompts
│   ├── security_investigation.py # Security investigation prompts
│   └── workspace_visualization.py # Workspace visualisation prompts
├── resources/                   # Static resources
│   ├── __init__.py              # Package initialisation
│   ├── kql_basics.py            # KQL syntax basics
│   ├── kql_cheatsheet.py        # KQL quick reference
│   ├── kql_examples.py          # Example KQL queries
│   └── kql_operators.py         # KQL operator reference
├── tools/                       # Operational tools
│   ├── __init__.py              # Package initialisation
│   ├── analytics_tools.py       # Analytics rule tools
│   ├── data_collection_tools.py # Data collection endpoint tools
│   ├── data_connector_tools.py  # Data connector management
│   ├── dcr_tools.py             # Data Collection Rules tools
│   ├── enrichment_tools.py      # IP/Domain enrichment tools
│   ├── entra_tools.py           # Entra ID user tools
│   ├── hunting_tools.py         # Security hunting tools
│   ├── incident_tools.py        # Incident management
│   ├── kql_tools.py             # KQL validation
│   ├── notebook_tools.py        # Notebook tools
│   ├── query_tools.py           # Query execution
│   ├── repository_tools.py      # Repository tools
│   ├── summary_tools.py         # Summary rules tools
│   ├── table_tools.py           # Table management
│   ├── watchlist_tools.py       # Watchlist tools
│   ├── workbook_tools.py        # Workbook tools
│   └── workspace_tools.py       # Workspace information
├── utilities/                   # Helper utilities
│   ├── __init__.py              # Package initialisation
│   ├── azure_sdk_utils.py       # Azure SDK utilities
│   ├── cache.py                 # Caching layer
│   ├── connection_test.py       # Connection testing
│   ├── kql_validator.py         # KQL validation logic
│   ├── logging.py               # Logging configuration
│   └── task_manager.py          # Async task management
└── tests/                       # Test suite
    ├── __init__.py              # Package initialisation
    ├── test_resources.py        # Resource tests
    ├── test_server.py           # Server tests
    ├── test_tools.py            # Tool tests
    └── test_utilities.py        # Utility tests
```

### Error Prevention Guidelines

- **Always check for existing files**: Before creating a new file, check if it already exists and ensure you're not overwriting important content.
- **Use consistent naming patterns**: Follow the established naming conventions for resources, tools, and prompts.
- **Validate Azure credentials early**: Test Azure connectivity before attempting to use Azure services.
- **Handle missing dependencies gracefully**: Implement fallbacks when external dependencies like the Kusto.Language DLL are not available.
- **Check error responses from Azure**: Validate that Azure API calls succeeded and handle error cases explicitly.
- **Validate input parameters**: Check parameter types, values, and requirements before using them.
- **Use type hints**: Add proper type annotations to help catch type-related errors early.
- **Control exception propagation**: Catch exceptions at appropriate levels and provide meaningful error messages.
- **Test in isolation**: Test each component independently before integration.
- **Version control properly**: Make small, focused commits with clear descriptions.

### Checkpoints

- **Environment Setup (Step 5)**: Verify that Azure authentication works correctly before proceeding.
- **Component Loading (Step 8)**: Ensure that the dynamic component loading system works before adding specific components.
- **Basic KQL Validation (Step 13)**: Verify that the KQL validation system works correctly before implementing query execution.
- **Basic Tools Working (Step 18)**: Confirm that all basic tools are registered and functional before adding advanced features.
- **Enrichment Tools Working (Step 19)**: Verify that IP geolocation and WHOIS lookups work correctly.
- **Prompt System Working (Step 31)**: Verify that prompts are properly registered and can be retrieved.
- **Integration Test Passing (Step 40)**: Ensure that all components work together correctly.
- **Security Review Completed (Step 42)**: Confirm that all security measures are properly implemented.
- **Claude Desktop Integration (Step 46)**: Verify that the server works correctly with Claude Desktop.

### Testing Instructions

- **Unit Tests**: Run `python -m unittest discover tests` to execute all unit tests.
- **Component Tests**:
  - Test each resource by listing and reading it.
  - Test each tool with valid and invalid inputs.
  - Test each prompt with various arguments.
- **Integration Tests**: Verify that the server can start, initialise, and handle requests.
- **Connection Tests**: Run `python utilities/connection_test.py` to verify Azure connectivity.
- **KQL Validation Test**: Run `python test_dll.py` to verify the Kusto.Language DLL works.
- **Manual Testing with Claude**: Install the server in Claude Desktop and test interactions.

### Dependency Management

- **Use uv**: Manage dependencies with `uv add` and `uv remove`.
- **Lock versions**: Use specific version constraints in `pyproject.toml`.
- **Optional dependencies**: Use dependency groups for development tools.
- **Virtual environments**: Always use a virtual environment for development and testing.
- **Dependency checking**: Verify compatibility of Azure SDK versions.
- **DLL management**: Use the download utility to manage the Kusto.Language DLL.

### Version Control Practices

- **Branching model**:
  - `main`: Stable releases
  - `develop`: Integration branch
  - Feature branches: Named `feature/feature-name`
  - Fix branches: Named `fix/issue-description`
- **Commit messages**: Use clear, descriptive commit messages with prefixes:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation changes
  - `test:` for test additions or changes
  - `refactor:` for code refactoring
- **Pull requests**: Create pull requests for all changes to main branches.
- **Code review**: Require code review for all pull requests.
- **Version tagging**: Tag releases with semantic version numbers (vX.Y.Z).
````

## File: docs/architecture/naming_convention.md
````markdown
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
````

## File: docs/architecture/project-requirements-document.md
````markdown
# Project Requirements Document (PRD)
## Microsoft Sentinel MCP Server

### 1. Project Overview
The Microsoft Sentinel MCP Server is a specialized implementation of the Model Context Protocol (MCP) that provides AI assistants (like Claude) access to Microsoft Sentinel security data and capabilities. The server acts as a bridge between large language models and Azure security infrastructure, allowing AI assistants to query security data, analyze incidents, retrieve threat information, and assist security analysts in their day-to-day operations. This server will enable security teams to leverage AI capabilities within their existing security operations workflows while maintaining security and control over sensitive data.

The primary goal is to create a robust, secure, and efficient MCP server that exposes Microsoft Sentinel's capabilities through standardized MCP resources, tools, and prompts, making complex security tasks more accessible through AI assistance. The server should handle authentication to Azure services, provide error handling for common failure scenarios, and offer a consistent way to access security information.

### 2. Target Users/Systems
- **Primary Users**: 
  - Security Operations Centre (SOC) analysts using AI assistants to accelerate investigations
  - Security engineers who need assistance with creating complex KQL (Kusto Query Language) queries
  - Incident responders who need quick access to incident details and context
  - Security administrators who need to understand their Sentinel workspace configuration

- **Secondary Users**:
  - Security managers seeking summarized security posture information
  - Developers building security tools that integrate with Sentinel
  - AI researchers exploring security analytics use cases

- **Systems**:
  - Microsoft Sentinel instances within Azure
  - Azure Monitor Log Analytics workspaces
  - Claude or other AI assistants that support the MCP protocol
  - Security orchestration platforms that might integrate with the server

### 3. Interaction Flow
Users interact with the server indirectly through an AI assistant. The assistant communicates with the MCP server to fetch data, execute queries, and format results. The AI then presents this information to the user in a natural, conversational manner. When users need security information, they ask the AI assistant questions or request specific analysis. The assistant determines which MCP resources or tools to invoke, sends requests to the MCP server, processes the responses, and presents insights back to the user.

For example, when a security analyst asks, "Show me recent failed login attempts," the AI assistant calls the appropriate query tool on the MCP server, which authenticates to Azure, executes the query against the Sentinel workspace, and returns the results. The AI then formats and explains these results conversationally to the user.

### 4. Technology Stack Overview
The Microsoft Sentinel MCP Server is built on Python 3.13+ using the MCP Python SDK for the protocol implementation. It leverages Azure SDK components for interacting with Microsoft Sentinel and Azure Monitor services. For KQL validation, it uses the Kusto Language library through Python.NET bindings. The server runs as a standalone process that can be connected to an AI assistant directly or through Claude Desktop.

Full details are provided in the Tech Stack Document.

### 5. Core Features/Capabilities

#### Resources
- **KQL Reference Resources**: Provides comprehensive documentation on KQL syntax, operators, and examples
- **Table Reference Resources**: Offers details about common Sentinel data tables and their schemas
- **Security Example Resources**: Includes example KQL queries for common security scenarios
- **Workspace Information Resources**: Delivers information about the Sentinel workspace configuration

#### Tools
- **KQL Query Validation**: Validates KQL syntax without executing queries
- **KQL Query Execution**: Runs KQL queries against the Sentinel workspace
- **Table Schema Explorer**: Retrieves table schemas and available tables
- **Security Incident Management**: Lists, retrieves, and updates security incidents
- **Data Connector Management**: Lists and provides information about data connectors
- **Workspace Information**: Gets detailed information about the Sentinel workspace

#### Prompts
- **Security Investigation Prompts**: Guides through investigating security scenarios
- **KQL Query Building Prompts**: Helps construct complex KQL queries
- **Incident Response Prompts**: Offers structured incident response workflows
- **Workspace Visualization Prompts**: Creates visualizations of workspace configuration

### 6. Scope Limitations
The following items are explicitly excluded from the initial version:

- **No Direct Data Modification**: The server will not allow direct modification of security data or configurations beyond updating incidents
- **No Custom Rule Creation**: The server will not create or modify analytics rules
- **No User Management**: The server will not handle Azure AD user management or permissions
- **Limited Visualizations**: The server will not generate complex visualizations or dashboards
- **No Alerting Functionality**: The server will not create or manage alert notifications
- **No Data Ingestion**: The server will not ingest data into Sentinel
- **No Multi-workspace Support**: The initial version will connect to a single workspace at a time

Future versions may address these limitations as the project evolves.

### 7. Success Criteria
- **Functionality**: Server successfully connects to Azure Sentinel and retrieves data
- **Performance**: Query execution time under 10 seconds for typical KQL queries
- **Reliability**: Server maintains stable connections with proper error handling
- **Security**: All communication with Azure services follows security best practices
- **Usability**: AI assistants can effectively use the server with minimal friction
- **Extensibility**: New tools and resources can be added without major refactoring
- **Validation**: KQL validation provides accurate and helpful feedback
- **Documentation**: Complete documentation of all server capabilities and usage

### 8. Dependencies
- **Azure Subscription**: Active Azure subscription with appropriate permissions
- **Microsoft Sentinel**: Configured Sentinel workspace with data
- **Service Principal**: Azure service principal with appropriate permissions
- **MCP Protocol Support**: AI assistant with MCP protocol support
- **Python Environment**: Python 3.13+ environment for running the server
- **Network Access**: Network connectivity to Azure endpoints
- **Microsoft.NET DLLs**: Kusto.Language DLL for KQL validation
- **Azure SDK Versions**: Compatible versions of Azure SDKs
````

## File: docs/architecture/prompt-architecture-doc.md
````markdown
# Microsoft Sentinel MCP Server Prompt Architecture

## Overview

This document describes the prompt architecture in the Microsoft Sentinel MCP Server as currently implemented. It serves as a reference for LLMs or developers who wish to add new prompts to the system.

## Current Implementation

The Microsoft Sentinel MCP Server implements prompts through a modular plugin architecture in a dedicated `prompts` directory:

```text
project_root/
├── server.py
├── resources/
│   ├── kql_basics.py
│   ├── kql_examples.py
│   └── ...
├── tools/
│   ├── kql_tools.py
│   ├── hunting_tools.py
│   └── ...
└── prompts/
    ├── __init__.py
    ├── security_investigation.py
    ├── kql_builder.py
    └── ...
```

Prompts are registered using the same component loader mechanism used for resources and tools:

```python
if os.path.exists(prompts_dir):
    prompts = load_components(mcp, prompts_dir, "register_prompts")
    logger.info(f"Auto-registered {len(prompts)} prompt modules")
```

This ensures all prompts are automatically discovered and registered with the MCP server during initialisation.

## Prompt Structure

Prompts are implemented as Python functions that return a list of `base.Message` objects, creating a multi-turn conversation template. Each prompt file must define a `register_prompts(mcp)` function that registers one or more prompts with the MCP server.

### Example: Basic Prompt Structure

```python
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

def register_prompts(mcp: FastMCP):
    """Register prompts with the MCP server."""

    @mcp.prompt()
    def sample_prompt(parameter1: str, parameter2: int = 10) -> list[base.Message]:
        """
        Description of what this prompt does.

        Args:
            parameter1: Description of first parameter
            parameter2: Description of second parameter with default value
        """
        return [
            base.UserMessage(f"User question about {parameter1}?"),
            base.AssistantMessage(f"First response about {parameter1} with {parameter2} items."),
            base.UserMessage("Follow-up question?"),
            base.AssistantMessage("Detailed answer to follow-up.")
        ]
```

## Existing Prompts

### Security Investigation Prompts

The `security_investigation.py` module provides prompts for security incident investigation:

```python
@mcp.prompt()
def investigate_ip_address(ip_address: str) -> list[base.Message]:
    """
    Investigate a potentially suspicious IP address in Microsoft Sentinel.

    Args:
        ip_address: The IP address to investigate
    """
    return [
        base.UserMessage(f"I need to investigate the IP address {ip_address} that appeared in our logs. What should I check?"),
        base.AssistantMessage("""
I'll guide you through a structured investigation of this IP address. Here's what we should check:

First, let's determine where this IP appears in our environment:
1. Check for connections to/from this IP across your network
2. Identify which systems have communicated with this IP
3. Determine the volume and frequency of these communications
...
"""),
        # Additional messages in the conversation
    ]
```

### KQL Query Building Prompts

The `kql_builder.py` module provides prompts for building KQL queries:

```python
@mcp.prompt()
def build_detection_query(
    threat_type: str, 
    data_source: str = "SecurityEvent", 
    time_window: str = "1d"
) -> list[base.Message]:
    """
    Create a KQL detection query for a specific threat type.
    
    Args:
        threat_type: Type of threat to detect (e.g., "brute force", "lateral movement")
        data_source: Primary data source table (default: SecurityEvent)
        time_window: Time window for detection (default: 1d)
    """
    return [
        base.UserMessage(f"I need to create a KQL detection query for {threat_type} attacks using {data_source} data over a {time_window} time window."),
        base.AssistantMessage("I'll help you build an effective detection query. First, let me show you some relevant KQL examples:"),
        base.AssistantMessage("Please reference the KQL examples at sentinel://examples/hunting"),
        # Additional messages in the conversation
    ]
```

## Adding New Prompts

To add a new prompt to the Microsoft Sentinel MCP Server, follow these steps:

1. **Create or select a prompt file**: Either create a new `.py` file in the `prompts` directory or add to an existing file based on the prompt category.

2. **Define the registration function**: Ensure your file has a `register_prompts(mcp: FastMCP)` function.

3. **Implement your prompt**: Define your prompt function with appropriate parameters and docstrings.

4. **Create the message sequence**: Build a realistic conversation flow using `base.UserMessage` and `base.AssistantMessage` objects.

5. **Test your prompt**: Restart the server to auto-register your prompt and test it with the MCP Inspector or Claude Desktop.

### Example: Adding a New Alert Analysis Prompt

```python
# In prompts/alert_analysis.py
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

def register_prompts(mcp: FastMCP):
    """Register alert analysis prompts."""

    @mcp.prompt()
    def analyse_security_alert(alert_name: str, severity: str = "any") -> list[base.Message]:
        """
        Analyse a specific type of security alert in Microsoft Sentinel.
        
        Args:
            alert_name: The name of the alert type to analyse
            severity: Optional filter for alert severity (any, high, medium, low)
        """
        return [
            base.UserMessage(f"I need to analyse {alert_name} alerts{' with ' + severity + ' severity' if severity != 'any' else ''}. What should I look for?"),
            base.AssistantMessage(f"""
I'll guide you through analysing {alert_name} alerts{' with ' + severity + ' severity' if severity != 'any' else ''}.

First, let's retrieve recent instances of this alert type:

```kusto
SecurityAlert
| where TimeGenerated > ago(7d)
| where AlertName contains "{alert_name}"
{f'| where AlertSeverity == "{severity}"' if severity != 'any' else ''}
| summarize count() by AlertName, AlertSeverity
```

Next, let's examine what these alerts tell us:
...
"""),
            base.UserMessage("Can you help me understand what entities are typically involved in these alerts?"),
            base.AssistantMessage(f"""
Great question. Let's extract the entities involved in {alert_name} alerts:

```kusto
SecurityAlert
| where TimeGenerated > ago(7d)
| where AlertName contains "{alert_name}"
{f'| where AlertSeverity == "{severity}"' if severity != 'any' else ''}
| extend Entities = parse_json(Entities)
| mv-expand Entity = Entities
| extend EntityType = tostring(Entity.Type), EntityName = tostring(Entity.Name)
| summarize count() by EntityType, EntityName
| sort by count_ desc
```

This will show you the most common entities involved in these alerts, which typically include:
...
""")
            # Additional messages as needed
        ]
```

## Best Practices for Creating Prompts

1. **Clear Documentation**
   - Provide detailed docstrings for each prompt
   - Document all parameters thoroughly
   - Include usage examples in comments when helpful

2. **Effective Structure**
   - Create realistic multi-turn conversations
   - Start with context and general information
   - Build toward specific, actionable recommendations
   - Include follow-up questions that users might ask

3. **Resource Integration**
   - Reference relevant resources like "sentinel://examples/hunting"
   - Consider embedding resource references directly in messages
   - Connect prompts to existing documentation when appropriate

4. **Dynamic Content**
   - Use parameters to customise the conversation
   - Include template variables in query examples
   - Adjust content based on parameter values

5. **Code Formatting**
   - Format KQL queries in proper ```kusto code blocks
   - Structure output with clear markdown formatting
   - Use headings, lists, and other formatting to improve readability

## Resource References in Prompts

While the current implementation uses text references to resources (e.g., "Please reference the KQL examples at sentinel://examples/hunting"), you can also use direct resource references in the future:

```python
# Example of direct resource reference (not currently implemented)
@mcp.prompt()
def prompt_with_resource(topic: str) -> list[base.Message]:
    """Prompt that directly references a resource."""
    
    # Create a resource reference
    kql_resource = {
        "type": "resource",
        "resource": {
            "uri": "sentinel://examples/hunting",
            "mimeType": "text/markdown"
        }
    }
    
    return [
        base.UserMessage(f"I need help with {topic}."),
        base.AssistantMessage("Here's some helpful information:", content=kql_resource)
    ]
```

## Conclusion

The prompt architecture in the Microsoft Sentinel MCP Server provides a flexible, extensible system for creating guided conversations. By following the patterns established in the existing code, you can easily add new prompts that help users navigate complex security tasks, build KQL queries, and analyse security data effectively.
````

## File: docs/architecture/security-guideline-document.md
````markdown
# Security Guideline Document
## Microsoft Sentinel MCP Server

### 1. Core Security Principles

The Microsoft Sentinel MCP Server adheres to these core security principles:

- **Defense in Depth**: Multiple layers of security controls mitigate different types of attacks
- **Principle of Least Privilege**: Components operate with the minimum permissions needed
- **Secure by Default**: Security measures are enabled by default with secure configuration
- **Data Protection**: Sensitive information is protected at rest and in transit
- **Zero Trust**: No inherent trust in any component or service
- **Transparency**: Clear documentation of security behaviors and limitations
- **Shift Left Security**: Security considerations built into the design from the beginning

### 2. Authentication Security

#### Azure Authentication Mechanisms

- **DefaultAzureCredential**
  - Primary authentication method for Azure services
  - Tries multiple authentication methods in sequence:
    1. Environment variables (AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID)
    2. Managed identity (when running in Azure)
    3. Azure CLI credentials
    4. Interactive browser authentication
  - Credentials must be provided before server startup

- **Service Principal Authentication**
  - Recommended for production deployments
  - Requires Client ID, Client Secret, and Tenant ID
  - Service principal must have the following roles assigned:
    - `Log Analytics Reader` for the workspace
    - `Microsoft Sentinel Reader` for read operations
    - `Microsoft Sentinel Responder` for incident management

- **Credential Lifecycle Management**
  - Credentials are loaded once during server initialization
  - Token refresh is handled automatically by Azure Identity library
  - No credentials are persisted to disk by the server
  - Environment variables should be configured in .env file (not committed to version control)

#### Credential Storage

- **Environment Variables**
  - Preferred method for supplying credentials
  - Set via `.env` file or directly in the environment
  - Example format:
    ```
    AZURE_TENANT_ID=00000000-0000-0000-0000-000000000000
    AZURE_CLIENT_ID=00000000-0000-0000-0000-000000000000
    AZURE_CLIENT_SECRET=client-secret-value
    AZURE_SUBSCRIPTION_ID=00000000-0000-0000-0000-000000000000
    ```

- **Credential Handling**
  - Credentials are never logged
  - Secrets are never included in error messages
  - In-memory credential objects are properly disposed after use
  - No caching of raw credentials

#### Authentication Error Handling

- Detailed authentication error messages without exposing secrets
- Graceful degradation when authentication fails
- Clear guidance for resolving authentication issues
- Authentication errors logged with appropriate severity

### 3. Authorization Framework

#### Azure RBAC Integration

- **Role Requirements**
  - Minimal required roles for full functionality:
    - `Log Analytics Reader`
    - `Microsoft Sentinel Reader`
    - `Microsoft Sentinel Responder`
  - Read-only functionality requires only:
    - `Log Analytics Reader`
    - `Microsoft Sentinel Reader`

- **Permission Verification**
  - Server verifies permissions on startup
  - Missing permissions result in specific warnings
  - Features requiring missing permissions are disabled

#### Server-Side Authorization

- **No Additional Authorization Layer**
  - Server assumes the authenticated Azure identity should have full access
  - No additional user authentication is implemented in the server
  - The MCP client (Claude Desktop) handles user authentication

- **Feature Degradation**
  - Features automatically disable when permissions are insufficient
  - Clear error messages indicate permission requirements
  - Read-only operations remain available when write permissions are missing

### 4. Data Protection

#### Data at Rest

- **No Persistent Storage**
  - The server doesn't store any data persistently
  - All security data remains in Azure Sentinel
  - No caching of query results or incident data to disk
  - Temporary files (if created) are properly cleaned up

- **Environment Variable Protection**
  - Environment variables should be protected by OS-level access controls
  - .env files should never be committed to version control
  - .env.example provides a template without actual values

#### Data in Transit

- **Azure SDK Encryption**
  - All communication with Azure services uses HTTPS/TLS 1.2+
  - Azure SDK handles certificate validation and secure connections
  - Default secure connection settings used for all Azure operations

- **MCP Protocol Security**
  - Local communication via stdio or SSE is not encrypted
  - Server assumes the local environment is trusted
  - For remote operation, an external TLS layer should be added

#### Sensitive Data Handling

- **No Logging of Sensitive Data**
  - Query contents are logged without parameters
  - Error messages exclude sensitive details
  - Authentication details are never logged
  - Log levels control verbosity of information

- **Memory Protection**
  - Sensitive objects cleared from memory when no longer needed
  - No serialization of credential objects
  - Proper handling of exceptions to prevent memory leaks

### 5. Input Validation

#### KQL Query Validation

- **Syntax Validation**
  - All KQL queries validated before execution
  - Kusto.Language library used for accurate validation
  - Detailed error messages for invalid syntax
  - Defense against KQL injection via proper query parameterization

- **Query Size Limits**
  - Maximum query length: 1MB
  - Maximum execution time: 10 minutes
  - Maximum result size: 50MB
  - Limits enforced before query execution

#### Parameter Validation

- **Type Checking**
  - All parameters validated for correct types
  - Conversion errors handled gracefully
  - Strong typing used throughout the codebase

- **Value Validation**
  - Numeric ranges validated (e.g., timeout values, limits)
  - String patterns validated (e.g., UUIDs, resource IDs)
  - Enum values validated against allowed values
  - Default values provided for optional parameters

#### Resource URI Validation

- **URI Format**
  - Resource URIs validated against allowed patterns
  - Protocol-specific validation for different URI types
  - Path traversal prevention for file URIs
  - Sanitization of URI components

- **Safe Resource Loading**
  - Resource contents validated before returning
  - MIME type verification
  - Size limits enforced
  - Content sanity checks

### 6. Vulnerability Mitigation

#### Code Injection Prevention

- **KQL Injection Prevention**
  - All user-provided query components properly validated
  - Parameter values properly escaped when interpolated
  - No dynamic KQL generation without validation
  - Query isolation from control mechanisms

- **Command Injection Prevention**
  - No shell command execution in the codebase
  - Subprocess calls (if needed) use list arguments, not shell=True
  - Proper argument validation before execution
  - Limited subprocess capabilities

#### Denial of Service Protection

- **Query Limiting**
  - Timeout enforcement for all queries
  - Maximum concurrent operations limit
  - Task cancellation for abandoned operations
  - Rate limiting for repetitive operations

- **Resource Consumption Controls**
  - Memory usage monitoring
  - Large result pagination
  - Task priority system
  - Graceful degradation under load

#### Supply Chain Security

- **Dependency Review**
  - All dependencies reviewed for security issues
  - Specific versions pinned in requirements
  - Regular updates for security patches
  - Limited dependency tree depth

- **Secure Dependency Installation**
  - Integrity verification of packages
  - Dependency lockfiles used
  - Installation from trusted sources
  - Vulnerability scanning in CI/CD

### 7. Security Testing

#### Required Security Tests

- **Static Analysis**
  - Run Bandit for Python security analysis
  - mypy for type checking
  - Custom linting rules for security patterns
  - Run on every code change

- **Authentication Testing**
  - Verify credential handling
  - Test authentication failure scenarios
  - Check token refresh behavior
  - Validate permission checks

- **Input Validation Testing**
  - Test with malformed inputs
  - Verify syntax validation
  - Check boundary conditions
  - Ensure proper error messages

- **Dependency Analysis**
  - Regular dependency vulnerability scanning
  - Check for outdated packages
  - Verify license compliance
  - Test compatibility with security patches

### 8. Monitoring and Incident Response

#### Security Logging

- **Log Levels**
  - ERROR: Security-related failures
  - WARNING: Potential security concerns
  - INFO: Normal security operations
  - DEBUG: Detailed security diagnostics

- **Log Content**
  - Authentication attempts (success/failure)
  - Authorization decisions
  - Operation execution
  - Resource access
  - Error conditions

- **Log Protection**
  - Logs directed to stderr by default
  - Sensitive data filtered from logs
  - Structured logging format
  - Log rotation if file logging enabled

#### Alert Thresholds

- **Authentication Failures**
  - Alert on multiple failed authentication attempts
  - Track unusual authentication patterns
  - Monitor for credential misuse

- **Authorization Failures**
  - Alert on repeated permission denied errors
  - Track attempts to access unauthorized resources
  - Monitor for privilege escalation attempts

- **Operational Anomalies**
  - Alert on abnormal query patterns
  - Monitor resource consumption spikes
  - Track unusual error rates

#### Incident Response Procedures

- **Authentication Issues**
  1. Identify the source of authentication failures
  2. Verify credential validity and permissions
  3. Rotate credentials if compromise is suspected
  4. Review logs for unauthorized access attempts

- **Azure Service Disruptions**
  1. Verify Azure service status
  2. Check network connectivity
  3. Validate credential permissions
  4. Implement appropriate fallback behaviors

- **Security Vulnerabilities**
  1. Assess vulnerability impact
  2. Apply temporary mitigations
  3. Update affected dependencies
  4. Implement permanent fixes

### 9. Dependency Security

#### Secure Dependencies

- **Azure SDK Security**
  - Use latest secure versions of Azure SDK components
  - Follow Microsoft security advisories
  - Implement recommended security practices
  - Test compatibility before upgrading

- **Python Package Security**
  - Pin dependency versions for predictability
  - Use trusted package sources
  - Verify package integrity
  - Regularly update for security patches

- **Third-Party Library Security**
  - Review security practices of third-party libraries
  - Limit scope of third-party code
  - Isolate potentially risky dependencies
  - Have fallbacks for critical dependencies

#### Secure Updates

- **Update Verification**
  - Test updates in isolation before deployment
  - Verify security fixes are included
  - Check for breaking changes in security patches
  - Validate compatibility with existing code

- **Update Frequency**
  - Security patches applied immediately
  - Regular updates for all dependencies
  - Version migration planning
  - Update documentation

#### Vulnerability Management

- **Vulnerability Tracking**
  - Monitor security advisories for dependencies
  - Track CVEs affecting the codebase
  - Assess impact of vulnerabilities
  - Prioritize based on severity and exploitability

- **Remediation Processes**
  - Document vulnerability remediation procedures
  - Test patches before deployment
  - Provide workarounds when patches aren't available
  - Communicate security updates to users

### Implementation Specifics

#### Secure Authentication Implementation

```python
def initialize_azure_credentials():
    """Initialize Azure credentials securely."""
    try:
        # DefaultAzureCredential tries multiple authentication methods
        credential = DefaultAzureCredential(
            exclude_shared_token_cache_credential=True,  # More predictable authentication
            logging_enable=False  # Prevent logging sensitive details
        )
        
        # Test credential by requesting a token
        # This validates credentials before proceeding
        token = credential.get_token("https://management.azure.com/.default")
        if not token:
            raise ValueError("Could not acquire token with provided credentials")
        
        return credential
    except Exception as e:
        # Log without revealing secrets
        logger.error(f"Authentication error: {type(e).__name__}")
        # Re-raise with generic message
        raise ValueError("Failed to authenticate with Azure. Check credentials and permissions.") from e
```

#### Secure Input Validation Implementation

```python
def validate_kql_query(query: str, max_length: int = 1024 * 1024) -> Tuple[bool, List[str]]:
    """
    Validate KQL query syntax securely.
    
    Args:
        query: The query to validate
        max_length: Maximum allowed query length
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    # Check size limits
    if not query:
        return False, ["Query is empty"]
    
    if len(query) > max_length:
        return False, [f"Query exceeds maximum length of {max_length} characters"]
    
    try:
        # Use KustoLanguage library for validation
        kql_code = self.KustoCode.Parse(query)
        diagnostics = list(kql_code.GetDiagnostics())
        
        if diagnostics:
            # Format diagnostics into readable messages
            error_messages = []
            for diag in diagnostics:
                # Extract position safely
                try:
                    line_pos = f"Line {diag.Start.Line}, Position {diag.Start.Column}"
                except:
                    line_pos = "Unknown position"
                
                # Extract message safely
                try:
                    message = diag.Message
                except:
                    message = str(diag)
                
                error_messages.append(f"{line_pos}: {message}")
            return False, error_messages
        
        return True, []
    except Exception as e:
        # Handle validation errors
        return False, [f"Error validating query: {type(e).__name__}"]
```

#### Secure Error Handling Implementation

```python
async def execute_query(query: str, workspace_id: str, timespan: Union[str, timedelta]) -> Dict[str, Any]:
    """
    Execute KQL query securely.
    
    Args:
        query: The KQL query to execute
        workspace_id: Target workspace ID
        timespan: Query time window
        
    Returns:
        Query results or error information
    """
    # Convert timespan to appropriate type
    time_delta = timespan if isinstance(timespan, timedelta) else parse_timespan(timespan)
    
    try:
        # Execute query with timeout
        response = await run_in_thread(
            self.logs_client.query_workspace,
            workspace_id=workspace_id,
            query=query,
            timespan=time_delta,
            name=f"query_{hash(query) % 10000}",  # Safe hash for identification
            timeout=60.0  # Hard timeout
        )
        
        # Process and return results
        if response and response.tables:
            # Format and return data safely
            return {
                "success": True,
                "rows": len(response.tables[0].rows),
                "data": format_query_results(response)
            }
        else:
            return {
                "success": True,
                "rows": 0,
                "data": "Query executed successfully but returned no results"
            }
    except Exception as e:
        # Secure error handling
        error_type = type(e).__name__
        error_message = str(e)
        
        # Remove any sensitive information
        sanitized_message = sanitize_error_message(error_message)
        
        logger.error(f"Query execution error: {error_type}: {sanitized_message}")
        
        return {
            "success": False,
            "error_type": error_type,
            "message": sanitized_message
        }
```
````

## File: docs/architecture/system-flow-document.md
````markdown
# System Flow Document
## Microsoft Sentinel MCP Server

The Microsoft Sentinel MCP Server transforms how security operations teams interact with their Sentinel data by creating a bridge between AI assistants and the wealth of security information stored in Azure. When the server first initializes, it loads its configuration from environment variables, attempting to authenticate with Azure services using the DefaultAzureCredential method. This versatile approach tries multiple authentication methods including environment variables, managed identities, and interactive browser authentication, making the server adaptable to various deployment scenarios. Once authentication succeeds, the server establishes connections to several Azure services simultaneously: the Log Analytics client for querying data, the Security Insights client for managing incidents, and optionally the Log Analytics Management client for workspace configuration.

During this initialization phase, the server also dynamically discovers and loads its components from predefined directories. It scans the resources directory, automatically registering any KQL reference materials, examples, and documentation. Similarly, it searches the tools directory to register operational tools like query execution and validation functions, and it checks the prompts directory for conversation templates. This dynamic loading system ensures the server remains extensible, allowing developers to add new capabilities simply by dropping compatible files into the appropriate directories.

After initializing all components and establishing Azure connections, the server starts listening for incoming MCP protocol messages. This communication follows the standardized MCP protocol, which defines specific message types for discovering server capabilities, listing available resources and tools, and making requests. The MCP transport layer handles serialization, message routing, and connection management, freeing the server implementation to focus on the actual security functionality.

When an AI assistant needs information about available server capabilities, it sends a capabilities request. The server responds with a comprehensive list of its features, indicating support for resources, tools, and prompts. It also communicates which optional features are supported, such as live resource updates or logging. This capabilities exchange forms the foundation for all subsequent interactions, ensuring the client and server understand each other's abilities.

For exploration, the AI assistant typically begins by discovering what the server offers. It might request a list of available resources, which would include KQL reference documentation, example security queries, and information about Sentinel tables. Alternatively, it could request a list of available tools or prompts. The server processes these discovery requests by gathering metadata about all registered components and formatting structured responses according to the MCP protocol specification. This discovery phase is crucial for the AI assistant to understand what functionality is available and how to access it.

When an actual security investigation begins, the AI often accesses reference materials first. It might request a KQL cheatsheet to understand query syntax or examples of security hunting queries. When the assistant makes such a request, the server looks up the appropriate resource by URI, retrieves its content, and returns it in the specified format (typically Markdown text). These resources are typically static and don't require Azure connectivity, making them reliable even in environments with connectivity issues.

The real power becomes evident when security analysts need to explore actual security data. When the analyst asks about recent security incidents, the AI assistant determines it needs to call the incident listing tool. The assistant sends a tool call request specifying the tool name ("sentinel_incidents_list") and parameters like the maximum number of incidents to return or severity filters. The server receives this request, validates the parameters, and then executes the appropriate function. This function authenticates with Azure using the previously established credentials, constructs the appropriate API call to the Security Insights client, and retrieves incident data. 

If the Azure API call succeeds, the server formats the results and returns them to the assistant. If any errors occur—connection timeouts, authentication failures, permission issues—the server catches these exceptions and returns meaningful error messages that explain the problem. This comprehensive error handling ensures the AI assistant receives actionable information even when operations fail.

Query execution follows a similar pattern but introduces additional complexity. When a security analyst wants to search for suspicious login attempts, the AI might determine it needs to run a KQL query. Before executing the query, the assistant may first validate it using the KQL validation tool. This validation tool leverages the Kusto Language library through Python.NET bindings to analyze the query syntax without executing it. The library parses the query, checks for syntax errors, validates references to tables and columns, and returns detailed diagnostic information. If validation succeeds, the assistant proceeds to execute the query.

Query execution is one of the most complex operations. When the assistant calls the query execution tool, the server first validates that all required parameters are present. It then converts any time-related parameters from human-readable formats like "7d" (7 days) to the appropriate datetime objects. Next, it establishes the connection to the Log Analytics workspace using the workspace ID from configuration and credentials from initialization. The query executes asynchronously within a task management system that handles timeouts and retries. For long-running queries, the server provides progress updates. When results return, they're processed into a structured format before being sent back to the assistant.

Throughout all these operations, the server maintains careful security boundaries. It never returns raw exception traces that might contain sensitive information. It validates all input parameters before using them in Azure API calls. And it carefully manages authentication state to ensure credentials aren't misused or leaked.

The server also handles complex operational patterns like paginated results. When retrieving large datasets like incident lists, the server implements pagination logic, making multiple API calls and combining results before returning them to the client. Similarly, for resource-intensive operations, the server implements rate limiting to prevent overloading Azure services.

For visualization creation, the server supports a unique workflow. When analysts need to understand their workspace configuration, the assistant calls a workspace visualization prompt. This prompt takes raw workspace information and transforms it into a comprehensive dashboard with explanations of settings, security recommendations, and potential configuration issues. The prompt processing happens within the server, allowing it to apply specialized formatting and domain knowledge before returning the enhanced content to the assistant.

In situations where direct Azure connectivity isn't available—perhaps during development or testing—the server gracefully degrades functionality. Core reference materials remain accessible, and some tools implement fallback behaviors that return simulated or cached data. This allows the assistant to maintain a consistent interaction pattern even when backend services are unavailable.

When the server needs to shut down—perhaps due to a deployment update or system maintenance—it initiates a graceful shutdown sequence. It cancels any running tasks, closes Azure connections, and releases system resources. This clean shutdown ensures no operations are left hanging and no resources are leaked.

Throughout its operation, the server maintains clear boundaries between its components. Resources provide static information, tools perform operations with potential side effects, and prompts define structured conversation patterns. This separation of concerns ensures the server remains maintainable and testable, with each component focused on a specific responsibility.

This architectural approach creates a powerful bridge between the structured world of security data and the natural language capabilities of AI assistants, allowing security teams to leverage both simultaneously for more efficient and effective security operations.
````

## File: docs/architecture/tech-stack-document.md
````markdown
# Tech Stack Document
## Microsoft Sentinel MCP Server

### 1. Programming Languages
- **Primary Language**: Python 3.13+
  - Chosen for its strong async support, type hinting, and extensive Azure SDK availability
  - All server code is written in Python with type annotations
- **Supporting Languages**:
  - C# (.NET): Used indirectly via the Kusto.Language library for KQL validation

### 2. Frontend Technologies
*Not applicable* - The Microsoft Sentinel MCP Server is a backend service that communicates using the MCP protocol and doesn't include a frontend component. AI assistants act as the interface to users.

### 3. Backend Technologies

#### Server Framework
- **MCP Python SDK v1.6.0+**
  - Core framework that implements the Model Context Protocol
  - Handles message routing, serialization, and communication patterns
  - Provides the `FastMCP` high-level API for server development

#### API Framework
- **No separate API framework**
  - All API endpoints are defined through MCP protocol handlers
  - Communication uses standard MCP message formats via stdin/stdout or SSE

#### Runtime Environment
- **Python Async/Await**
  - Uses Python's asyncio for handling concurrent operations
  - Async context managers for resource management
  - Task tracking for proper cleanup and timeout handling

#### HTTP Client
- **Azure SDK HTTP Pipeline**
  - Uses Azure SDK's built-in HTTP pipeline for Azure service communication
  - Handles retries, authentication, and error processing

### 4. Database Technologies
- **No local database**
  - The server acts as a bridge to Microsoft Sentinel/Log Analytics
  - Azure Monitor Logs (Kusto) serves as the query backend
  - No local state persistence beyond the current session

#### Query Languages
- **Kusto Query Language (KQL)**
  - Used for querying Microsoft Sentinel data
  - Server validates and executes KQL queries against Azure Monitor

### 5. Authentication/Authorization
- **Azure Identity Library**
  - Uses DefaultAzureCredential for flexible authentication methods
  - Supports environment variables, managed identity, and interactive login
  - Credential objects are created during server initialization

- **Azure RBAC (Role-Based Access Control)**
  - Relies on Azure's built-in RBAC system for authorization
  - The service principal or user identity must have appropriate permissions in Azure

### 6. Infrastructure
- **Local Process**
  - Runs as a standalone Python process on the local system
  - Can be installed in Claude Desktop for direct integration
  - No containerization in the base implementation

- **Hosting**
  - Primarily designed for local execution
  - Can be adapted for server deployment with appropriate transport changes

### 7. Third-Party Services
- **Azure Monitor Query API** (v1.4.1+)
  - Used for executing KQL queries against Log Analytics workspaces
  - Provides access to logs and metrics data

- **Azure Security Insights API** (v1.0.0+)
  - Used for accessing Microsoft Sentinel resources
  - Provides incident management, watchlists, and security settings

- **Azure Log Analytics Management API** (v12.0.0+)
  - Used for workspace management and configuration
  - Provides workspace metadata and settings

- **Python.NET** (v3.0.1+)
  - Bridge for using .NET libraries from Python
  - Used specifically for the Kusto Language library

- **Kusto.Language .NET Library**
  - Used for KQL syntax validation
  - Downloaded and loaded during server initialization

### 8. Development Tools
- **uv**
  - Modern Python package installer and virtual environment manager
  - Used for dependency management

- **Black**
  - Python code formatter for consistent style
  - Set to line length of 88 characters

- **isort**
  - Import sorter for organizing imports
  - Configured to be compatible with Black

- **mypy**
  - Static type checker for Python
  - Set to basic type checking mode

- **flake8**
  - Linter for style guide enforcement
  - Used alongside Black and isort

### 9. Rationale for Choices

#### Python as Primary Language
Python was chosen for its strong support in the Azure ecosystem, excellent async capabilities, and widespread use in security tooling. Python's type hints allow for better IDE support and code verification while maintaining readability. The language's extensive library ecosystem provides robust tools for handling complex operations like authentication and HTTP communication.

#### MCP Python SDK
The MCP Python SDK was the natural choice as it's the official implementation of the Model Context Protocol. It provides a well-designed API that abstracts away the complexities of the protocol while maintaining compliance with the specification. The FastMCP high-level API significantly reduces boilerplate code compared to using the low-level protocol interfaces.

#### Azure SDK Components
Official Azure SDK components were selected to ensure compatibility and proper handling of authentication, token management, and API versioning. These libraries are well-maintained, follow consistent patterns, and receive regular updates for security and functionality.

#### Python.NET and Kusto.Language
Validating KQL syntax requires complex parsing logic that would be difficult to implement from scratch. By using the official Kusto.Language library through Python.NET, the server leverages the same validation engine used by Microsoft tools, ensuring consistent and accurate results. This approach trades some deployment complexity for significantly improved validation capabilities.

#### Local Process Execution
The server is designed to run locally to minimize deployment complexity and security concerns. This design choice keeps sensitive credentials on the user's system and simplifies integration with Claude Desktop. The server can be adapted for remote deployment if needed, but the default configuration prioritizes simplicity and security.

### 10. Compatibility Notes

#### Component Interoperability
- The Azure SDK components are designed to work together seamlessly
- Python.NET may require specific .NET runtime versions depending on the environment
- MCP SDK is compatible with any reasonable Python async implementation

#### Version Requirements
- Azure Identity ≥ 1.21.0
- Azure Monitor Query ≥ 1.4.1
- Azure Security Insights ≥ 1.0.0
- Azure Log Analytics Management ≥ 12.0.0
- Python.NET ≥ 3.0.1
- MCP ≥ 1.6.0

#### Operating System Compatibility
- Primary: Windows 10/11, due to Python.NET and .NET requirements
- Limited: macOS and Linux support may require additional setup for the .NET runtime
- The core functionality (except KQL validation) works on all platforms that support Python 3.13+

#### MCP Protocol Compatibility
- Implements MCP 1.0 specification
- Compatible with Claude Desktop and other MCP-compliant clients
- Supports both stdin/stdout and SSE transports
````

## File: docs/architecture/tool-architecture-and-implementation-requirements.md
````markdown
# MCP Tool Architecture and Implementation Requirements

## CRITICAL REQUIREMENT: CLASS-BASED, MODULE-LEVEL TOOLS ONLY

> **ALL MCP TOOLS MUST BE DEFINED AS CLASS-BASED TOOLS AT THE MODULE LEVEL.**
>
> - Each tool must be implemented as a class that inherits from MCPToolBase (imported from tools.base). The class must implement the async def run(self, ctx, **kwargs) method, and provide clear documentation for parameters, return values, and errors.

**Import Convention:**
All MCP tools must import MCPToolBase from 'tools.base', not from 'mcp' or any other module. Example:

```python
from tools.base import MCPToolBase
```

> - No tool may be implemented as a function, nor registered via decorators (such as `@mcp.tool`).
> - All tool classes MUST be defined at the top (module) level of the file—**never** nested inside functions, other classes, or conditional blocks.
> - This is a strict requirement for MCP compliance, discoverability, maintainability, and future extensibility. Any tool not following this pattern will be rejected and removed.

## Purpose
This document defines the comprehensive requirements, conventions, and best practices for implementing any new tools for the Microsoft Sentinel MCP server. It is intended as the single source of truth for contributors, ensuring all tools are robust, maintainable, testable, and MCP-compliant.

---

## 1. Tool Structure and Base Class
- **ALL TOOLS MUST BE CLASS-BASED AND MODULE-LEVEL.**
    - Every tool must be a class that inherits from `MCPToolBase`.
    - No function-based or decorator-registered tools are permitted under any circumstances.
    - Tool classes must be defined at the module (file) level, never nested inside functions or other classes.
    - **No nested classes are allowed.**
- The main entrypoint must be an `async def run(self, ctx: Context, **kwargs)` method.
- All parameters must be extracted from `kwargs`, supporting both direct keys and `kwargs["kwargs"]` for compatibility with MCP/SSE invocation patterns.
    - **Robust pattern:**
      ```python
      param = kwargs.get("param")
      if param is None and "kwargs" in kwargs:
          param = kwargs["kwargs"].get("param")
      ```
- **All tools that call Microsoft APIs (Azure SDK, SecurityInsights, etc.) or any other blocking/non-async APIs must use `run_in_thread` from `utilities.task_manager` to wrap such calls.**
    - This is required for any synchronous SDK/API call, including but not limited to Azure, Microsoft Graph, REST, or other network/file/database I/O, to prevent blocking the event loop and ensure MCP server responsiveness.
    - Example usage:
      ```python
      from utilities.task_manager import run_in_thread
      ...
      result = await run_in_thread(client.some_blocking_method, ...)
      ```
- Never duplicate context or Azure client extraction logic; always use base class properties/methods for context, clients, and workspace information.
    - **Important:** When using context or Azure client extraction helpers, always call them via `self` (e.g., `self.get_azure_context(ctx)`), not via the `ctx` object. These are base class methods, not context methods.

### MCPToolBase Context and Client Helper Methods

The `MCPToolBase` class provides standardized helper methods for extracting Azure context and clients. **All tools must use these helpers instead of duplicating context/client extraction logic.**

| Method | Purpose | Usage Example |
|--------|---------|--------------|
| `get_logs_client_and_workspace(ctx)` | Returns a tuple `(logs_client, workspace_id)` for querying Log Analytics tables. Supports both MCP server and direct invocation (integration tests). | `logs_client, workspace_id = self.get_logs_client_and_workspace(ctx)` |
| `get_azure_context(ctx)` | Returns a tuple `(workspace_name, resource_group, subscription_id)` using environment variables or context attributes as fallback. | `workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)` |
| `_extract_param(kwargs, name, default=None)` | Extracts a parameter value from kwargs, supporting both direct and nested patterns. Handles type checking for nested kwargs. | `param_value = self._extract_param(kwargs, "param_name", default_value)` |
| `get_loganalytics_client(subscription_id)` | Returns an authenticated `LogAnalyticsManagementClient` for the given subscription. | `client = self.get_loganalytics_client(subscription_id)` |
| `validate_azure_context(sdk_available, workspace_name, resource_group, subscription_id, logger=None)` | Checks if all required Azure context is present and SDK is available. Logs warning and returns `False` if not valid, otherwise `True`. | `valid = self.validate_azure_context(sdk_available, workspace_name, resource_group, subscription_id, logger)` |

- **IMPORTANT: Always check the MCPToolBase class for utility functions before implementing your own.** Prefer reusable code within the base class rather than creating separate implementations across tools. This ensures consistent behavior, reduces code duplication, and centralizes bug fixes. If you find yourself implementing a utility function that could be useful across multiple tools, consider adding it to the MCPToolBase class instead.

**Tool authors must use these helpers for all Azure context and client extraction.** This ensures robust, testable, and MCP-compliant code. Do not instantiate Azure SDK clients or extract environment variables directly in tool logic; always delegate to the base class helpers.
- The `run` method should focus on parameter extraction, error handling, and business logic only.
- Tools **must** support direct invocation for integration tests (i.e., if `ctx.request_context` is not present, fall back to environment variables for Azure context and credentials).
- For stub/unimplemented tools, return a minimal stub such as `{ "error": "[TODO] Not yet implemented." }` or a clear TODO string for consistency.
- **Canonical tool registration code example:**
  ```python
  from mcp import MCPToolBase

  class MyTool(MCPToolBase):
      async def run(self, ctx: Context, **kwargs):
          # Tool logic here
          pass
  ```
- **Migration note for legacy decorator/function tools:** If you have existing tools implemented as functions or registered via decorators, you must migrate them to class-based tools at the module level to ensure MCP compliance.

---

## 2. Naming Conventions
- Tool class names: `PascalCase` (e.g., `SentinelAnalyticsRuleListTool`).
- Tool registration names: `snake_case` following the `<domain>_<product>_<category>_<action>` pattern (see [Naming Convention](naming_convention.md)).
- Use singular nouns for single-item operations (`get`), plural for collections (`list`).
- Consistently use verbs: `get`, `list`, `search`, `create`, `validate`, `update`, `delete`.
- **File structure:** Tools should be organized in a directory structure that mirrors their registration names, with each set of tools per topic/function in a single file.

---

## 3. MCP-Compliant Tool Output
- Tool logic should always return a **dict** (not a wrapped content list); the base class (`MCPToolBase`) will wrap this dict into the correct MCP-compliant output structure.
- All tool results **must** return a list of content objects, each with a `type` field (`"json"`, `"text"`, etc.)—this is handled by the base class.
- For structured data, return a dict; the base class will wrap as `{ "type": "json", "json": ... }`.
- For errors, tool logic **must** include an `"error"` key in the returned dict (e.g., `{ "error": "..." }`) for testability. Do not rely solely on server or base class error wrapping.
- The final result returned from the server will be `{ "content": [...], "isError": <bool> }`.
- Do **not** return raw strings or JSON-serialized strings from tool logic.
- Centralize result wrapping in the base class so tool authors only return native Python objects.
- Document the output structure for each tool.
- **Always return all expected output keys** (such as `valid`, `errors`, etc.) in the result dict, even when returning an error. This ensures test and consumer robustness.

---

## 4. Error Handling and Logging
- Return clear, structured error messages if required context or parameters are missing.
- Log all errors using the tool's logger for traceability.
- Never log or include secrets in error messages.
- For Azure SDK errors, include the exception type and message in the error output.
- **When calling `ctx.warning` or similar context hooks, always check for existence/callability before invoking to avoid errors in tests or custom contexts.**

---

## 5. Context and Direct Invocation Support
- Tools must support both MCP server invocation and direct invocation (for integration/unit tests).
- If `ctx.request_context` is not available, construct Azure clients and context directly from environment variables.
- Environment variables required (always present for tests): `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_SUBSCRIPTION_ID`, `AZURE_RESOURCE_GROUP`, `AZURE_WORKSPACE_NAME`.
- Document this fallback pattern in every tool that requires Azure context.
- **When mocking or extending the `Context` object (a Pydantic model) for tests, all new attributes must be declared as Pydantic fields or set using `object.__setattr__`. Dynamic attribute assignment is not supported by default.**

---

## 6. Testing Requirements

### Code Coverage
- All tools must be covered by automated code coverage analysis using the `coverage` tool (e.g., `coverage run -m pytest` and `coverage report`).
- All main code paths and use cases must have matching unit tests; strive for 100% coverage of business logic, parameter validation, error handling, and edge cases.
- Pull requests should not be merged unless code coverage is maintained or improved, and all new features are tested.

### Unit Tests
- All unit tests must use `@pytest.mark.asyncio` and `async def` for async tools.
- Always call the tool as `await tool(ctx, ...)`, not `tool.run`.
- Use `MagicMock` and `patch` for context and dependencies; patch `run_in_thread` if used.
- At the top of every test file, insert:
  ```python
  import sys
  import os
  sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
  ```
- Assert on all major fields and nested structures in the tool's output.
- Pass parameters via `kwargs` (or `kwargs={...}`) to match real invocation patterns.
- Mock Azure SDK clients with realistic objects mirroring actual API responses.
- Name test files as `test_<tool>_unit.py`.
- **Tests must cover all edge cases:** missing parameters, valid and invalid input, and both direct and nested kwargs patterns.

### Integration Tests
- The following environment variables **must** be present and correctly set for integration tests (see `.env.example`):
  - `AZURE_TENANT_ID`  # Azure Credentials
  - `AZURE_CLIENT_ID`
  - `AZURE_CLIENT_SECRET`
  - `AZURE_SUBSCRIPTION_ID`  # Azure Resources
  - `AZURE_RESOURCE_GROUP`
  - `AZURE_WORKSPACE_NAME`
  - `AZURE_WORKSPACE_ID`
- These are required for authentication and configuration with Azure services and the Sentinel workspace.
- Call the tool with real data and assert presence/structure of key fields in the output.

---

## 7. Linting and Code Quality
- Run `ruff check --fix` after every code change to ensure linting compliance.
- Use `coverage` to measure and enforce test coverage.
- Ensure all files are fully lint-compliant before merging.
- Organize imports as per linter or project conventions.

---

## 8. MCP Server Restart and Testing Workflow
- After any tool code change, **restart the MCP server** to load new code before testing output.
- Once MCP output is correct, ensure comprehensive unit test coverage for the tool in `/tests/unit`.
- Run coverage tests and add any missing tests to achieve full coverage.
- Capture the full output of all pytest runs to `/dev/full_test_output.txt` for diagnostics.
- Store all temporary troubleshooting scripts/outputs in `/dev`.

---

## 9. Security and Credential Handling
- Use `DefaultAzureCredential` or `ClientSecretCredential` for Azure authentication.
- Never log or expose secrets.
- Credentials must be loaded from environment variables, not hardcoded or committed.
- Handle authentication and permission errors gracefully, with actionable error messages.

---

## 10. Documentation and Discoverability
- Every tool **must** have a dedicated markdown documentation file in `resources/tool_docs`, named after the tool (e.g., `sentinel_logs_table_get.md`).
- **All tool documentation files must follow this structure:**
  1. **Purpose** — A short description of the tool's purpose and behavior.
  2. **Parameters** — Table listing all accepted arguments, with type, required/optional, and description.
  3. **Output Fields** — Table describing each output key and its meaning, including types.
  4. **Example Request** — Example input for the tool.
  5. **Example Response** — Example output from the tool.
  6. **Usage Notes** — Any relevant notes (API dependencies, edge cases, limitations, etc.).
  7. **Error Cases** — List of possible errors and their meanings.
  8. **See Also** — References to related tools or documentation.
- This structure is modeled in `resources/tool_docs/sentinel_incident_details_get.md` and must be used for all new tool docs.
- Document every tool's parameters, output structure, and error cases.
- Follow the project's file and directory structure for new tools and tests.

---

## 11. Additional Guidelines
- When adding new tools, review `/docs/architecture/naming_convention.md`, `/docs/architecture/security-guideline-document.md`, and `/docs/architecture/system-flow-document.md` for further requirements.
- For troubleshooting, create all direct-call scripts and outputs in `/dev`.
- Always validate tool output via the MCP interface after code changes and before finalizing tests.

---

## 12. Example Patterns
### Context Extraction
```python
if hasattr(ctx, "request_context") and getattr(ctx, "request_context", None) is not None:
    client = getattr(ctx.request_context.lifespan_context, "security_insights_client", None)
    workspace = getattr(ctx.request_context.lifespan_context, "workspace_name", None)
    resource_group = getattr(ctx.request_context.lifespan_context, "resource_group", None)
    subscription_id = getattr(ctx.request_context.lifespan_context, "subscription_id", None)
else:
    import os
    from azure.identity import ClientSecretCredential
    from azure.security.insights import SecurityInsightsClient
    tenant_id = os.environ["AZURE_TENANT_ID"]
    client_id = os.environ["AZURE_CLIENT_ID"]
    client_secret = os.environ["AZURE_CLIENT_SECRET"]
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    resource_group = os.environ["AZURE_RESOURCE_GROUP"]
    workspace = os.environ["AZURE_WORKSPACE_NAME"]
    credential = ClientSecretCredential(tenant_id, client_id, client_secret)
    client = SecurityInsightsClient(credential, subscription_id)
```

### MCP Output Wrapping
```python
def wrap_result(self, result):
    if isinstance(result, list) and all(isinstance(x, dict) and "type" in x for x in result):
        return result
    elif isinstance(result, (dict, list)):
        return [{"type": "json", "json": result}]
    else:
        return [{"type": "text", "text": str(result)}]
```

---

## 13. Checklist for New Tools
- [ ] **ALL TOOLS MUST BE CLASS-BASED AND MODULE-LEVEL.**
- [ ] Inherit from `MCPToolBase` and implement `async def run(self, ctx, **kwargs)`
- [ ] Use all Azure context/client extraction helpers via `self` (e.g., `self.get_azure_context(ctx)`), not via the `ctx` object
- [ ] **Wrap all synchronous Microsoft API (Azure SDK, SecurityInsights, etc.) and other blocking/non-async API calls with `await run_in_thread(...)` from `utilities.task_manager`.**
- [ ] Use MCP-compliant output structure
- [ ] Support both server and direct invocation
- [ ] Provide comprehensive unit and integration tests
- [ ] Follow naming, security, and linting conventions
- [ ] Document parameters, output, and errors
- [ ] Register the tool for discovery
- [ ] Validate via MCP and ensure full test coverage
- [ ] **No nested classes are allowed.**
- [ ] Run `ruff check --fix` after every code change to ensure linting compliance.
- [ ] Use `coverage` to measure and enforce test coverage.

---

## 14. References
- [Naming Convention](naming_convention.md)
- [Security Guidelines](security-guideline-document.md)
- [System Flow](system-flow-document.md)
- [Implementation Plan](implementation-plan.md)

---

_This document supersedes previous ad-hoc instructions and should be updated as the MCP architecture evolves._
````

## File: docs/llm_instructions.md
````markdown
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
````

## File: resources/markdown_templates/sentinel_workspace_get.md
````markdown
# Azure Sentinel Workspace Details

**Workspace Name:** `{{ workspace_name }}`
**Resource Group:** `{{ resource_group }}`  
**Subscription:** `{{ subscription_id }}`  
**Location:** `{{ direct_info.location }}`  
**SKU:** `{{ direct_info.sku }}`
{% if direct_info.sku_description %}  _Description:_ {{ direct_info.sku_description }}{% endif %}
{% if direct_info.last_sku_update %}  _Last SKU Update:_ {{ direct_info.last_sku_update }}{% endif %}
**Retention (days):** `{{ direct_info.retention_period_days }}`  
**Daily Quota (GB):** `{{ direct_info.daily_quota_gb }}`  
**Quota Reset Time:** `{{ direct_info.quota_reset_time }}`  
**Ingestion Status:** `{{ direct_info.ingestion_status }}`  
**Public Network Access (Ingestion):** `{{ direct_info.public_network_access_ingestion }}`  
**Public Network Access (Query):** `{{ direct_info.public_network_access_query }}`  
**Created:** `{{ direct_info.created }}`  
**Last Modified:** `{{ direct_info.last_modified }}`  

{% if direct_info.features %}
## Workspace Features
{% if direct_info.features.additional_properties %}
{% for k, v in direct_info.features.additional_properties.items() %}- **{{ k }}:** `{{ v }}`
{% endfor %}
{% endif %}
{% for k, v in direct_info.features.items() %}{% if k != "additional_properties" %}- **{{ k }}:** `{{ v }}`
{% endif %}{% endfor %}
{% endif %}

{% if additional_information %}
## Additional Information
{% for line in additional_information %}- {{ line }}
{% endfor %}
{% endif %}
````

## File: resources/tool_docs/entra_id_get_group.md
````markdown
# Entra ID Get Group Tool

**Tool Name:** `entra_id_get_group`

**Description:**
Retrieves a single group from Microsoft Entra ID (Azure AD) by object ID, using the Microsoft Graph API.

---

## Parameters
- `group_id` (string, required): The object ID of the group to retrieve (e.g., `06adad8d-89b3-4b64-82b0-7d5e17dfac3f`).

---

## Returns
A JSON object representing the group, with fields including:
- `displayName`: The group's display name.
- `description`: The group's description.
- `id`: The unique object ID of the group.
- Additional fields may include `mail`, `mailNickname`, `securityEnabled`, etc.

---

## Example Output
```json
{
  "displayName": "sg-IT",
  "description": "All IT personnel",
  "id": "06adad8d-89b3-4b64-82b0-7d5e17dfac3f"
}
```

---

## Permissions Required
- `Group.Read.All` (Microsoft Graph)

---

## Error Handling
- Returns a permission error if the caller lacks the required Graph API permissions.
- Returns a clear error if the specified group does not exist or if the Graph API is unreachable.
- Returns an error if `group_id` is missing or invalid.

---

## Example Use Case
Use this tool to retrieve details for a specific group in your Azure AD tenant, for group lookups, automation, or audit purposes.

---

## Notes
NIL
````

## File: resources/tool_docs/entra_id_get_user.md
````markdown
# Entra ID Get User Tool

**Tool Name:** `entra_id_get_user`

**Description:**
Retrieves a single user from Microsoft Entra ID (Azure AD) by object ID, UPN (User Principal Name), or email address, using the Microsoft Graph API.

---

## Parameters
- `user_id` (string, optional): The object ID (e.g., `31d6905a-fb48-4e75-a41e-dbd214689352`) of the user to retrieve.
- `upn` (string, optional): The User Principal Name (UPN) of the user (e.g., `AdeleV@example.OnMicrosoft.com`).
- `email` (string, optional): The user's primary email address (e.g., `AdeleV@example.OnMicrosoft.com`).
 
**At least one of `user_id`, `upn`, or `email` must be provided.**

---

## Returns
A JSON object representing the user, with fields including:
- `displayName`: The user's display name.
- `userPrincipalName`: The user's UPN (login name).
- `mail`: The user's primary email address.
- `id`: The unique object ID of the user.
- Additional fields may include `givenName`, `surname`, `businessPhones`, etc.

---

## Example Output
```json
{
  "displayName": "Adele Vance",
  "userPrincipalName": "AdeleV@example.OnMicrosoft.com",
  "mail": "AdeleV@example.OnMicrosoft.com",
  "id": "31d6905a-fb48-4e75-a41e-dbd214689352"
}
```

## Example Usage
- Lookup by object ID:
  ```json
  { "user_id": "31d6905a-fb48-4e75-a41e-dbd214689352" }
  ```
- Lookup by UPN:
  ```json
  { "upn": "AdeleV@example.OnMicrosoft.com" }
  ```
- Lookup by email:
  ```json
  { "email": "AdeleV@example.OnMicrosoft.com" }
  ```

---

## Permissions Required
- `User.Read.All` (Microsoft Graph)

---

## Error Handling
- Returns a permission error if the caller lacks the required Graph API permissions.
- Returns a clear error if the specified user does not exist or if the Graph API is unreachable.
- Returns an error if none of `user_id`, `upn`, or `email` is provided.
- Returns an error if the specified user does not exist.

---

## Example Use Case
Use this tool to retrieve details for a specific user in your Azure AD tenant, for user lookups, automation, or audit purposes.

---

## Notes
NIL
````

## File: resources/tool_docs/entra_id_list_groups.md
````markdown
# Entra ID List Groups Tool

**Tool Name:** `entra_id_list_groups`

**Description:**
Lists all groups in Microsoft Entra ID (Azure AD) via the Microsoft Graph API.

---

## Parameters
_None_

---

## Returns
A JSON array of group objects, each containing (at minimum):
- `displayName`: The group's display name.
- `description`: The group's description.
- `id`: The unique object ID of the group.
- Additional fields may include `mail`, `mailNickname`, `securityEnabled`, etc.

---

## Example Output
```json
[
  {
    "displayName": "sg-IT",
    "description": "All IT personnel",
    "id": "06adad8d-89b3-4b64-82b0-7d5e17dfac3f"
  },
  // ...more groups
]
```

---

## Permissions Required
- `Group.Read.All` (Microsoft Graph)

---

## Error Handling
- Returns a permission error if the caller lacks the required Graph API permissions.
- Returns a clear error if the Graph API is unreachable or misconfigured.

---

## Example Use Case
Use this tool to enumerate all groups in your Azure AD tenant, for reporting, automation, or auditing.

---

## Notes
- For large tenants, paging is handled automatically.
````

## File: resources/tool_docs/entra_id_list_users.md
````markdown
# Entra ID List Users Tool

**Tool Name:** `entra_id_list_users`

**Description:**
Lists all users in Microsoft Entra ID (Azure AD) via the Microsoft Graph API.

---

## Parameters
_None_

---

## Returns
A JSON array of user objects, each containing (at minimum):
- `displayName`: The user's display name.
- `userPrincipalName`: The user's UPN (login name).
- `mail`: The user's primary email address.
- `id`: The unique object ID of the user.
- Additional fields may include `givenName`, `surname`, `businessPhones`, etc.

---

## Example Output
```json
[
  {
    "displayName": "Adele Vance",
    "userPrincipalName": "AdeleV@example.OnMicrosoft.com",
    "mail": "AdeleV@example.OnMicrosoft.com",
    "id": "31d6905a-fb48-4e75-a41e-dbd214689352"
  },
  {
    "displayName": "Alex Wilber",
    "userPrincipalName": "AlexW@example.OnMicrosoft.com",
    "mail": "AlexW@example.OnMicrosoft.com",
    "id": "4c56c3b6-a237-40ca-8d53-1ea68a4961d8"
  }
  // ...more users
]
```

---

## Permissions Required
- `User.Read.All` (Microsoft Graph)

---

## Error Handling
- Returns a permission error if the caller lacks the required Graph API permissions.
- Returns a clear error if the Graph API is unreachable or misconfigured.

---

## Example Use Case
Use this tool to enumerate all users in your Azure AD tenant, e.g., for reporting, auditing, or automation workflows.

---

## Notes
- For large tenants, paging is handled automatically.
````

## File: resources/tool_docs/llm_instructions_get.md
````markdown
# LLM Instructions Get Tool

**Tool Name:** `llm_instructions_get`

## Overview
Retrieves the LLM usage instructions for the Sentinel MCP Server. This tool should be called before all other tools to understand LLM-specific guidelines and requirements.

## Parameters
- None

## Output
- `content` (str): Raw markdown content of the LLM instructions file (typically `docs/llm_instructions.md`).
- If error, returns a dict with `error` (str).

## Example Requests
### Get LLM usage instructions
```
{}
```

## Example Output
```
{
  "content": "# LLM Usage Instructions

- Use fictional placeholders for all workspace details...
..."
}
```

## Error Handling
- Returns `error` if the instructions file cannot be read.

## MCP Compliance
- Inherits from `MCPToolBase`.
- Implements `async def run(self, ctx, **kwargs)`.
- Registered in `register_tools()`.
- Uses robust error handling.
````

## File: resources/tool_docs/log_analytics_saved_search_get.md
````markdown
# Log Analytics Saved Search Get

## Purpose

This tool retrieves detailed information about a specific saved search in the Log Analytics workspace by its ID. Saved searches are stored queries that can be reused and shared, and are often used for common monitoring scenarios or as the basis for alert rules in Microsoft Sentinel.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| saved_search_id | String | Yes | The ID of the saved search to retrieve. This is the name portion of the saved search resource ID, such as "LogManagement(workspace-name)_General\|StaleComputers" |

## Output Fields

| Field | Type | Description |
|-------|------|-------------|
| savedSearch | Object | The saved search details |
| savedSearch.id | String | Full resource ID of the saved search |
| savedSearch.name | String | Name/identifier of the saved search |
| savedSearch.type | String | Resource type (Microsoft.OperationalInsights/savedSearches) |
| savedSearch.category | String | Category of the saved search (e.g., "General Exploration") |
| savedSearch.displayName | String | Human-readable name of the saved search |
| savedSearch.query | String | The KQL query text of the saved search |
| savedSearch.version | Integer | Version number of the saved search |
| savedSearch.functionAlias | String | Function alias if the saved search is published as a function (may be null) |
| valid | Boolean | Indicates if the operation was successful |
| error | String | Error message if the operation failed (only present on error) |

## Example Request

```json
{
  "tool": "log_analytics_saved_search_get",
  "saved_search_id": "LogManagement(workspace-name)_General|StaleComputers"
}
```

## Example Response

```json
{
  "savedSearch": {
    "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/savedSearches/LogManagement(<workspace-name>)_General|StaleComputers",
    "name": "LogManagement(<workspace-name>)_General|StaleComputers",
    "type": "Microsoft.OperationalInsights/savedSearches",
    "category": "General Exploration",
    "displayName": "Stale Computers (data older than 24 hours)",
    "query": "search not(ObjectName == \"Advisor Metrics\" or ObjectName == \"ManagedSpace\") | summarize lastdata = max(TimeGenerated) by Computer | limit 500000 | where lastdata < ago(24h)
// Oql: NOT(ObjectName=\"Advisor Metrics\" OR ObjectName=ManagedSpace) | measure max(TimeGenerated) as lastdata by Computer | top 500000 | where lastdata < NOW-24HOURS",
    "version": 2
  },
  "valid": true
}
```

## Usage Notes

- This tool requires proper Azure authentication and permissions to access the Log Analytics workspace.
- The saved search ID is the name portion of the resource ID, not the full resource ID.
- To find available saved search IDs, use the `log_analytics_saved_searches_list` tool first.
- The response includes the full KQL query text, which can be used to understand or modify the saved search.
- Some fields may be null or missing depending on the saved search configuration.

## Error Cases

| Error | Description |
|-------|-------------|
| "saved_search_id parameter is required" | The required saved_search_id parameter was not provided |
| "Missing Azure SDK or workspace details." | The required Azure SDK modules are not available or workspace configuration is missing |
| "Azure LogAnalytics client initialization failed: {error}" | Failed to initialize the Azure LogAnalytics client |
| "Azure LogAnalytics client is not initialized" | The Azure LogAnalytics client could not be initialized |
| "Error retrieving saved search ID {saved_search_id}: {error}" | An error occurred while retrieving the saved search from the Azure API |

## See Also

- [log_analytics_saved_searches_list](log_analytics_saved_searches_list.md) - List all saved searches in a workspace
- [Azure Log Analytics Documentation](https://docs.microsoft.com/azure/azure-monitor/logs/log-analytics-overview)
````

## File: resources/tool_docs/log_analytics_saved_searches_list.md
````markdown
# Log Analytics Saved Searches List

## Purpose

This tool retrieves a list of all saved searches in the current Log Analytics workspace. Saved searches are stored queries that can be reused and shared, and are often used for common monitoring scenarios or as the basis for alert rules in Microsoft Sentinel.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| None | | | This tool does not require any parameters |

## Output Fields

| Field | Type | Description |
|-------|------|-------------|
| savedSearches | Array | List of saved search objects |
| savedSearches[].id | String | Full resource ID of the saved search |
| savedSearches[].name | String | Name/identifier of the saved search |
| savedSearches[].type | String | Resource type (Microsoft.OperationalInsights/savedSearches) |
| count | Integer | Total number of saved searches returned |
| valid | Boolean | Indicates if the operation was successful |
| error | String | Error message if the operation failed (only present on error) |

## Example Request

```json
{
  "tool": "log_analytics_saved_searches_list"
}
```

## Example Response

```json
{
  "savedSearches": [
    {
      "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/savedSearches/LogManagement(<workspace-name>)_General|StaleComputers",
      "name": "LogManagement(<workspace-name>)_General|StaleComputers",
      "type": "Microsoft.OperationalInsights/savedSearches"
    },
    {
      "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/savedSearches/LogManagement(<workspace-name>)_General|dataTypeDistribution",
      "name": "LogManagement(<workspace-name>)_General|dataTypeDistribution",
      "type": "Microsoft.OperationalInsights/savedSearches"
    }
    // Additional saved searches...
  ],
  "count": 76,
  "valid": true
}
```

## Usage Notes

- This tool requires proper Azure authentication and permissions to access the Log Analytics workspace.
- The tool returns basic information about each saved search. To get detailed information about a specific saved search, use the `log_analytics_saved_search_get` tool with the saved search ID.
- The response may be large if there are many saved searches in the workspace.
- The saved searches are returned in the order provided by the Azure API.

## Error Cases

| Error | Description |
|-------|-------------|
| "Missing Azure SDK or workspace details." | The required Azure SDK modules are not available or workspace configuration is missing |
| "Azure LogAnalytics client initialization failed: {error}" | Failed to initialize the Azure LogAnalytics client |
| "Azure LogAnalytics client is not initialized" | The Azure LogAnalytics client could not be initialized |
| "Error retrieving saved searches: {error}" | An error occurred while retrieving saved searches from the Azure API |

## See Also

- [log_analytics_saved_search_get](log_analytics_saved_search_get.md) - Get details for a specific saved search
- [Azure Log Analytics Documentation](https://docs.microsoft.com/azure/azure-monitor/logs/log-analytics-overview)
````

## File: resources/tool_docs/markdown_template_get.md
````markdown
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
  "content": "# Azure Sentinel Workspace Details

**Workspace Name:** `{{ workspace_name }}`
**Resource Group:** `{{ resource_group }}`
**Subscription:** `{{ subscription_id }}`
**Location:** `{{ direct_info.location }}`
**SKU:** `{{ direct_info.sku }}`
{% if direct_info.sku_description %}  _Description:_ {{ direct_info.sku_description }}{% endif %}
..."
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
````

## File: resources/tool_docs/markdown_templates_list.md
````markdown
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
      "content": "# Azure Sentinel Workspace Details

**Workspace Name:** `{{ workspace_name }}`
**Resource Group:** `{{ resource_group }}`
**Subscription:** `{{ subscription_id }}`
**Location:** `{{ direct_info.location }}`
**SKU:** `{{ direct_info.sku }}`
{% if direct_info.sku_description %}  _Description:_ {{ direct_info.sku_description }}{% endif %}
..."
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
````

## File: resources/tool_docs/sentinel_analytics_rule_get.md
````markdown
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
````

## File: resources/tool_docs/sentinel_analytics_rule_list.md
````markdown
# Sentinel Analytics Rule List Tool

**Tool Name:** `sentinel_analytics_rule_list`

## Overview
Lists all Microsoft Sentinel analytics rules in the current workspace, returning key fields for each rule.

## Parameters
- None required. Uses workspace context from MCP server or environment variables.

## Output
- List of dicts, each containing:
    - `id` (str): Rule ID.
    - `name` (str): Rule name.
    - `display_name` (str): Display name of the rule.
    - `enabled` (bool): Whether the rule is enabled.
    - `severity` (str): Severity level.
    - `description` (str): Description of the rule.
    - `last_modified_utc` (str): Last modification date/time (UTC).
    - `kind` (str): Rule kind/type.
    - ... (other available summary fields)
- If error, returns a dict with `error` (str).

## Example Output
```
[
  {
    "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace>/providers/Microsoft.SecurityInsights/alertRules/BuiltInFusion",
    "name": "BuiltInFusion",
    "kind": "Fusion",
    "displayName": "Advanced Multistage Attack Detection",
    "severity": "High",
    "enabled": true
  },
  {
    "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace>/providers/Microsoft.SecurityInsights/alertRules/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "name": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "kind": "Scheduled",
    "displayName": "New CloudShell User",
    "severity": "Low",
    "enabled": true
  },
  ...
]
```

## Error Handling
- Returns `error` field if context is missing or SDK/API errors occur.

## MCP Compliance
- Inherits from `MCPToolBase`.
- Implements `async def run(self, ctx, **kwargs)`.
- Registered in `register_tools()`.
- Uses robust Azure context extraction and error handling.
````

## File: resources/tool_docs/sentinel_analytics_rule_template_get.md
````markdown
# Sentinel Analytics Rule Template Get Tool

**Tool Name:** `sentinel_analytics_rule_template_get`

## Overview
Retrieves details for a specific Microsoft Sentinel analytics rule template by its ID or name.

## Parameters
- `id` (str, required): The full resource ID or unique name of the analytics rule template.

## Output
- Dict containing all available fields for the template, e.g.:
    - `id` (str): Template ID.
    - `name` (str): Template name.
    - `display_name` (str): Display name.
    - `description` (str): Description.
    - `tactics` (list): List of MITRE tactics (if available).
    - `techniques` (list): List of MITRE techniques (if available).
    - ... (all other template properties)
- If error, returns a dict with `error` (str).

## Example Output
```
{
  "id": "/subscriptions/.../AlertRuleTemplates/abcde",
  "name": "TemplateName",
  "display_name": "Template Display Name",
  "description": "Detects ...",
  "tactics": ["collection", "exfiltration"],
  "techniques": ["T1005", "T1020"]
  ...
}
```

## Error Handling
- Returns `error` field if context is missing, template not found, or SDK/API errors occur.

## MCP Compliance
- Inherits from `MCPToolBase`.
- Implements `async def run(self, ctx, **kwargs)`.
- Registered in `register_tools()`.
- Uses robust Azure context extraction and error handling.
````

## File: resources/tool_docs/sentinel_analytics_rule_templates_count_by_tactic.md
````markdown
# Sentinel Analytics Rule Templates Count By Tactic Tool

**Tool Name:** `sentinel_analytics_rule_templates_count_by_tactic`

## Overview
Counts Microsoft Sentinel analytics rule templates by MITRE ATT&CK tactic. Returns a mapping of each tactic to the count and a list of template summaries.

## Parameters
- None required. Uses workspace context from MCP server or environment variables.

## Output
- `valid` (bool): True if query succeeded.
- `error` (str or None): Error message if any.
- `results` (dict):
    - Each key is a tactic (lowercase string or "unknown").
    - Each value is a dict with:
        - `count` (int): Number of templates for this tactic.
        - `templates` (list): List of dicts with `id` and `display_name` for each template.
- `errors` (list): List of error strings if any.

## Example Output
```
{
  "initialaccess": {
    "count": 115,
    "templates": [
      {"id": "...", "display_name": "Sign-ins from IPs that attempt sign-ins to disabled accounts"},
      ...
    ]
  },
  ...
}
```

## Error Handling
- Returns `error` and `errors` fields if context is missing or SDK/API errors occur.

## MCP Compliance
- Inherits from `MCPToolBase`.
- Implements `async def run(self, ctx, **kwargs)`.
- Registered in `register_tools()`.
- Uses robust Azure context extraction and error handling.
````

## File: resources/tool_docs/sentinel_analytics_rule_templates_count_by_technique.md
````markdown
# Sentinel Analytics Rule Templates Count By Technique Tool

**Tool Name:** `sentinel_analytics_rule_templates_count_by_technique`

## Overview
Counts Microsoft Sentinel analytics rule templates by MITRE ATT&CK technique (or comma-separated list of techniques). Returns a mapping of each technique to the count and a list of template summaries.

## Parameters
- None required. Uses workspace context from MCP server or environment variables.

## Output
- `valid` (bool): True if query succeeded.
- `error` (str or None): Error message if any.
- `results` (dict):
    - Each key is a technique (lowercase string or "unknown").
    - Each value is a dict with:
        - `count` (int): Number of templates for this technique.
        - `templates` (list): List of dicts with `id` and `display_name` for each template.
- `errors` (list): List of error strings if any.

## Example Output
```
{
  "unknown": {
    "count": 477,
    "templates": [
      {"id": "...", "display_name": "Sign-ins from IPs that attempt sign-ins to disabled accounts"},
      ...
    ]
  },
  ...
}
```

## Error Handling
- Returns `error` and `errors` fields if context is missing or SDK/API errors occur.

## MCP Compliance
- Inherits from `MCPToolBase`.
- Implements `async def run(self, ctx, **kwargs)`.
- Registered in `register_tools()`.
- Uses robust Azure context extraction and error handling.
````

## File: resources/tool_docs/sentinel_analytics_rule_templates_list.md
````markdown
# Sentinel Analytics Rule Templates List Tool

**Tool Name:** `sentinel_analytics_rule_templates_list`

## Overview
Lists all Microsoft Sentinel analytics rule templates in the current workspace, returning key fields for each template.

## Parameters
- None required. Uses workspace context from MCP server or environment variables.

## Output
- List of dicts, each containing:
    - `id` (str): Template ID.
    - `name` (str): Template name.
    - `display_name` (str): Display name of the template.
    - `description` (str): Description of the template.
    - `tactics` (list): List of MITRE tactics (if available).
    - `techniques` (list): List of MITRE techniques (if available).
    - ... (other available summary fields)
- If error, returns a dict with `error` (str).

## Example Output
```
[
  {
    "id": "/subscriptions/.../AlertRuleTemplates/abcde",
    "name": "TemplateName",
    "display_name": "Template Display Name",
    "description": "Detects ...",
    "tactics": ["collection", "exfiltration"],
    "techniques": ["T1005", "T1020"]
  },
  ...
]
```

## Error Handling
- Returns `error` field if context is missing or SDK/API errors occur.

## MCP Compliance
- Inherits from `MCPToolBase`.
- Implements `async def run(self, ctx, **kwargs)`.
- Registered in `register_tools()`.
- Uses robust Azure context extraction and error handling.
````

## File: resources/tool_docs/sentinel_analytics_rules_count_by_tactic.md
````markdown
# Sentinel Analytics Rules Count By Tactic Tool

**Tool Name:** `sentinel_analytics_rules_count_by_tactic`

## Overview
Counts Microsoft Sentinel analytics rules by MITRE ATT&CK tactic. Returns a mapping of each tactic to the count and a list of rule summaries.

## Parameters
- None required. Uses workspace context from MCP server or environment variables.

## Output
- `valid` (bool): True if query succeeded.
- `error` (str or None): Error message if any.
- `results` (dict):
    - Each key is a tactic (lowercase string or "unknown").
    - Each value is a dict with:
        - `count` (int): Number of rules for this tactic.
        - `rules` (list): List of dicts with `id` and `display_name` for each rule.
- `errors` (list): List of error strings if any.

## Example Output
```
{
  "collection": {
    "count": 5,
    "rules": [
      {"id": "...", "display_name": "Advanced Multistage Attack Detection"},
      ...
    ]
  },
  ...
}
```

## Error Handling
- Returns `error` and `errors` fields if context is missing or SDK/API errors occur.

## MCP Compliance
- Inherits from `MCPToolBase`.
- Implements `async def run(self, ctx, **kwargs)`.
- Registered in `register_tools()`.
- Uses robust Azure context extraction and error handling.
````

## File: resources/tool_docs/sentinel_analytics_rules_count_by_technique.md
````markdown
# Sentinel Analytics Rules Count By Technique Tool

**Tool Name:** `sentinel_analytics_rules_count_by_technique`

## Overview
Counts Microsoft Sentinel analytics rules by MITRE ATT&CK technique (or comma-separated list of techniques). Returns a mapping of each technique to the count and a list of rule summaries.

## Parameters
- None required. Uses workspace context from MCP server or environment variables.

## Output
- `valid` (bool): True if query succeeded.
- `error` (str or None): Error message if any.
- `results` (dict):
    - Each key is a technique (lowercase string or "unknown").
    - Each value is a dict with:
        - `count` (int): Number of rules for this technique.
        - `rules` (list): List of dicts with `id` and `display_name` for each rule.
- `errors` (list): List of error strings if any.

## Example Output
```
{
  "unknown": {
    "count": 28,
    "rules": [
      {"id": "...", "display_name": "Advanced Multistage Attack Detection"},
      ...
    ]
  },
  ...
}
```

## Error Handling
- Returns `error` and `errors` fields if context is missing or SDK/API errors occur.

## MCP Compliance
- Inherits from `MCPToolBase`.
- Implements `async def run(self, ctx, **kwargs)`.
- Registered in `register_tools()`.
- Uses robust Azure context extraction and error handling.
````

## File: resources/tool_docs/sentinel_authorization_summary.md
````markdown
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
````

## File: resources/tool_docs/sentinel_connectors_get.md
````markdown
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
````

## File: resources/tool_docs/sentinel_connectors_list.md
````markdown
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
````

## File: resources/tool_docs/sentinel_domain_whois_get.md
````markdown
# sentinel_domain_whois_get

## Description
Get WHOIS information for a domain using Microsoft Sentinel's enrichment API.

## Parameters

| Parameter | Type   | Required | Description                     |
|-----------|--------|----------|---------------------------------|
| domain    | string | Yes      | The domain name to look up      |

## Returns

| Field   | Type   | Description                                |
|---------|--------|--------------------------------------------|
| whois   | object | WHOIS data for the specified domain        |
| valid   | bool   | Whether the operation was successful       |

### WHOIS Object Fields

| Field       | Type   | Description                                       |
|-------------|--------|---------------------------------------------------|
| domain      | string | The domain that was looked up                     |
| server      | string | WHOIS server used for the lookup                  |
| created     | string | Domain creation date (ISO 8601 format)            |
| updated     | string | Last update date (ISO 8601 format)                |
| expires     | string | Expiration date (ISO 8601 format)                 |
| parsed_whois| object | Structured WHOIS data                             |

### parsed_whois Object Fields

| Field       | Type   | Description                                       |
|-------------|--------|---------------------------------------------------|
| registrar   | object | Information about the domain registrar            |
| contacts    | object | Contact information for domain roles              |
| name_servers| array  | List of domain name servers                       |
| statuses    | array  | Domain status codes                               |

#### registrar Object Fields

| Field              | Type   | Description                                       |
|--------------------|--------|---------------------------------------------------|
| name               | string | Registrar company name                            |
| abuse_contact_email| string | Email for abuse reports                           |
| abuse_contact_phone| string | Phone number for abuse reports                    |
| iana_id            | string | IANA ID of the registrar                          |
| url                | string | Registrar URL                                     |
| whois_server       | string | Registrar's WHOIS server                          |

#### contacts Object Fields
Contains admin, billing, registrant, and tech objects, each with the following fields:

| Field       | Type   | Description                                       |
|-------------|--------|---------------------------------------------------|
| name        | string | Contact name                                      |
| org         | string | Organization name                                 |
| street      | array  | Street address lines                              |
| city        | string | City                                              |
| state       | string | State or province                                 |
| postal      | string | Postal code                                       |
| country     | string | Country code                                      |
| phone       | string | Phone number                                      |
| fax         | string | Fax number                                        |
| email       | string | Email address                                     |

## Error Response

| Field   | Type   | Description                                |
|---------|--------|--------------------------------------------|
| error   | string | Error message if the operation failed      |
| valid   | bool   | false                                      |

## Examples

### Request
```json
{
  "domain": "microsoft.com"
}
```

### Response
```json
{
  "whois": {
    "domain": "microsoft.com",
    "server": "whois.markmonitor.com",
    "created": "1991-05-02T04:00:00.000Z",
    "updated": "2023-08-18T16:15:54.000Z",
    "expires": "2025-05-03T00:00:00.000Z",
    "parsed_whois": {
      "registrar": {
        "name": "MarkMonitor Inc.",
        "abuse_contact_email": "abusecomplaints@markmonitor.com",
        "abuse_contact_phone": "+1.2086851750",
        "iana_id": "292",
        "url": "292",
        "whois_server": "whois.markmonitor.com"
      },
      "contacts": {
        "admin": {
          "name": "Domain Administrator",
          "org": "Microsoft Corporation",
          "street": ["One Microsoft Way"],
          "city": "Redmond",
          "state": "WA",
          "postal": "98052",
          "country": "US",
          "phone": "+1.4258828080",
          "fax": "+1.4259367329",
          "email": "admin@domains.microsoft"
        },
        "billing": {
          "name": "",
          "org": "",
          "street": [""],
          "city": "",
          "state": "",
          "postal": "",
          "country": "",
          "phone": "+1.2086851750",
          "fax": "",
          "email": "abusecomplaints@markmonitor.com"
        },
        "registrant": {
          "name": "Domain Administrator",
          "org": "Microsoft Corporation",
          "street": ["One Microsoft Way"],
          "city": "Redmond",
          "state": "WA",
          "postal": "98052",
          "country": "US",
          "phone": "+1.4258828080",
          "fax": "+1.4259367329",
          "email": "admin@domains.microsoft"
        },
        "tech": {
          "name": "MSN Hostmaster",
          "org": "Microsoft Corporation",
          "street": ["One Microsoft Way"],
          "city": "Redmond",
          "state": "WA",
          "postal": "98052",
          "country": "US",
          "phone": "+1.4258828080",
          "fax": "+1.4259367329",
          "email": "msnhst@microsoft.com"
        }
      },
      "name_servers": [
        "ns1-39.azure-dns.com",
        "ns2-39.azure-dns.net",
        "ns3-39.azure-dns.org",
        "ns4-39.azure-dns.info"
      ],
      "statuses": ["ACTIVE"]
    }
  },
  "valid": true
}
```

### Error Example
```json
{
  "error": "Error retrieving WHOIS data for example.invalid: Domain not found",
  "valid": false
}
```

## Notes
- This tool uses Microsoft Sentinel's domain WHOIS enrichment API
- Unlike other Sentinel APIs, this enrichment API does not require a workspace_name parameter
- The tool returns structured WHOIS data that has been parsed from the raw WHOIS response
- Some fields may be empty or missing depending on the domain's registration information
- All dates are returned in ISO 8601 format (YYYY-MM-DDThh:mm:ss.sssZ)

## Permissions Required
- Azure Resource Group Reader access or higher
- Microsoft.SecurityInsights/enrichment/read permission

## Related Tools
- sentinel_ip_geodata_get - Get geolocation data for an IP address
````

## File: resources/tool_docs/sentinel_hunting_queries_count_by_tactic.md
````markdown
# Sentinel Hunting Queries Count By Tactic Tool Documentation

## Purpose
Count Sentinel hunting queries (saved searches) by tactic.

## Parameters
| Name   | Type   | Required | Description                     |
|--------|--------|----------|---------------------------------|
| None   |        |          | This tool takes no parameters.  |

## Output Fields
| Name    | Type   | Description                                         |
|---------|--------|-----------------------------------------------------|
| valid   | bool   | True if the operation was successful                |
| error   | str    | Error message if any                                |
| results | dict   | Mapping of tactic name to count                     |
| errors  | list   | List of error messages                              |

## Example Request
```json
{
}
```

## Example Response
```json
{
  "valid": true,
  "error": null,
  "results": {
    "unknown": {
      "count": 76,
      "queries": [
        {"id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/savedSearches/<query-id>", "display_name": "SharePointFileOperation via devices with previously unseen user agents"},
        {"id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/savedSearches/<query-id>", "display_name": "Microsoft Sentinel Connectors Administrative Operations"}
      ]
    }
  },
  "errors": []
}
```

## Usage Notes
- Useful for reporting and dashboarding.

## Error Cases
- Azure API or credential errors

## See Also
- sentinel_hunting_queries_list
- sentinel_hunting_query_get
````

## File: resources/tool_docs/sentinel_hunting_queries_list.md
````markdown
# Sentinel Hunting Queries List Tool Documentation

## Purpose
List all Sentinel hunting queries (saved searches) with optional tactic/technique filtering.

## Parameters
| Name         | Type   | Required | Description                                              |
|--------------|--------|----------|----------------------------------------------------------|
| tactic       | string | No       | Filter queries by tactic (case-insensitive, optional)    |
| technique    | string | No       | Filter queries by technique (case-insensitive, optional) |

## Output Fields
| Name    | Type   | Description                                         |
|---------|--------|-----------------------------------------------------|
| valid   | bool   | True if the operation was successful                |
| error   | str    | Error message if any                                |
| results | list   | List of hunting queries (dicts)                     |
| errors  | list   | List of error messages                              |

## Example Request
```json
{
}
```

## Example Response
```json
{
  "valid": true,
  "error": null,
  "results": [
    {
      "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/savedSearches/<query-id>",
      "name": "0dd4c9dd-5d2c-4c2d-a0e5-eafeca5d9910",
      "display_name": "SharePointFileOperation via devices with previously unseen user agents",
      "category": "Hunt Queries",
      "query": "let starttime = todatetime('{{StartTimeISO}}'); ...",
      "tags": [
        {"name": "description", "value": "Tracking via user agent is one way ..."},
        {"name": "tactics", "value": "Exfiltration"},
        {"name": "techniques", "value": "T1030"}
      ],
      "tactics": ["Exfiltration"],
      "techniques": ["T1030"],
      "description": "Tracking via user agent is one way to differentiate ...",
      "version": 2
    },
    {"id": "...", "name": "...", "display_name": "...", "category": "...", "query": "...", "tags": [], "tactics": [], "techniques": [], "description": null, "version": 2}
  ],
  "errors": []
}
```

## Usage Notes
- Filters are optional. Returns all queries if not specified.

## Error Cases
- Azure API or credential errors

## See Also
- sentinel_hunting_search
- sentinel_hunting_query_get
````

## File: resources/tool_docs/sentinel_hunting_query_get.md
````markdown
# Sentinel Hunting Query Get Tool Documentation

## Purpose
Retrieve the full details of a Sentinel hunting query (saved search) by name or ID.

## Parameters
| Name     | Type   | Required | Description                                                    |
|----------|--------|----------|----------------------------------------------------------------|
| query_id | string | No       | The full resource ID or GUID of the saved search (optional)    |
| name     | string | No       | The display name or name of the saved search (optional)        |

## Output Fields
| Name        | Type   | Description                                         |
|-------------|--------|-----------------------------------------------------|
| valid       | bool   | True if the operation was successful                |
| error       | str    | Error message if any                                |
| results     | dict   | Full hunting query details if found                 |
| errors      | list   | List of error messages                              |

## Example Request
```json
{
  "query_id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/savedSearches/<query-id>"
}
```

## Example Response
```json
{
  "valid": true,
  "error": null,
  "results": {
    "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/savedSearches/<query-id>",
    "name": "0dd4c9dd-5d2c-4c2d-a0e5-eafeca5d9910",
    "display_name": "SharePointFileOperation via devices with previously unseen user agents",
    "category": "Hunt Queries",
    "query": "let starttime = todatetime('{{StartTimeISO}}'); ...",
    "tags": [
      {"name": "description", "value": "Tracking via user agent is one way ..."},
      {"name": "tactics", "value": "Exfiltration"},
      {"name": "techniques", "value": "T1030"}
    ],
    "tactics": ["Exfiltration"],
    "techniques": ["T1030"],
    "description": "Tracking via user agent is one way to differentiate ...",
    "version": 2
  },
  "errors": []
}
```

## Usage Notes
- At least one of `query_id` or `name` must be provided.
- Returns error if no match found.

## Error Cases
- Missing both query_id and name
- No matching query found
- Azure API or credential errors

## See Also
- sentinel_hunting_queries_list
- sentinel_hunting_search
````

## File: resources/tool_docs/sentinel_incident_details_get.md
````markdown
# sentinel_incident_get

## Purpose
Retrieves detailed information about a specific Microsoft Sentinel incident, including all available fields and calculated counts for related alerts, bookmarks, and comments. Also returns up to 5 related alerts if present.

## Parameters
| Name           | Type   | Required | Description                                                      |
|----------------|--------|----------|------------------------------------------------------------------|
| incident_number| int    | Yes      | The IncidentNumber of the Sentinel incident to retrieve.          |
| kwargs         | dict   | No       | Additional parameters (for nested invocation compatibility).      |

## Output Fields
The tool returns a dictionary with the following structure:

| Key            | Type    | Description                                                         |
|----------------|---------|---------------------------------------------------------------------|
| incident       | dict    | All columns from the `SecurityIncident` table, plus calculated fields: `AlertsCount`, `BookmarksCount`, `CommentsCount`. |
| related_alerts | list    | Up to 5 related alerts (dicts) from the `SecurityAlert` table, joined by `AlertIds`/`SystemAlertId`. |
| error          | string  | Present only if an error occurred.                                  |
| message        | string  | Present if no incident was found.                                   |

### Example `incident` fields (non-exhaustive):
- IncidentNumber
- Title
- Description
- Severity
- Status
- Classification
- ClassificationComment
- CreatedTime
- LastModifiedTime
- IncidentUrl
- ProviderName
- AlertsCount (calculated)
- BookmarksCount (calculated)
- CommentsCount (calculated)
- AlertIds (list)
- ... (all other columns from SecurityIncident)

### Example `related_alerts` fields:
- Time
- Name
- Severity
- Status
- Description
- Entities

## Example Request
```
{
  "incident_number": 3
}
```

## Example Response
```
{
  "incident": {
    "IncidentNumber": 3,
    "Title": "Suspicious Resource deployment",
    "Description": "Identifies when a rare Resource and ResourceGroup deployment occurs by a previously unseen caller.",
    "Severity": "Low",
    "Status": "New",
    "Classification": "",
    "ClassificationComment": "",
    "CreatedTime": "2025-04-17T12:34:13.422179Z",
    ...
    "AlertsCount": 1,
    "BookmarksCount": 0,
    "CommentsCount": 0,
    "AlertIds": ["40cefd90-2f07-b1ea-bcd0-ae811cbde0ed"],
    ...
  },
  "related_alerts": [
    {
      "Time": "2025-04-17T12:34:13.422179Z",
      "Name": "AlertName",
      "Severity": "High",
      "Status": "Active",
      "Description": "desc",
      "Entities": ["entity"]
    }
  ]
}
```

## Usage Notes
- Returns all available fields from the incident, including any new columns added to the schema.
- If no incident is found, returns a dict with a `message` key.
- If `AlertIds` is empty or missing, `related_alerts` will be an empty list.
- Handles both MCP server and direct invocation (using environment variables for Azure context if needed).
- All errors are returned as a dict with an `error` key.

## Error Cases
- Missing or invalid `incident_number` parameter.
- Incident not found.
- Azure authentication or query errors.

## See Also
- [sentinel_incident_list](sentinel_incident_list.md) — for listing incidents.
- [sentinel_logs_table_schema_get](sentinel_logs_table_schema_get.md) — for table schema details.
````

## File: resources/tool_docs/sentinel_ip_geodata_get.md
````markdown
# sentinel_ip_geodata_get

## Description
Get geolocation data for an IP address using Microsoft Sentinel's enrichment API.

## Parameters

| Parameter | Type   | Required | Description                     |
|-----------|--------|----------|---------------------------------|
| ip        | string | Yes      | The IP address to look up       |

## Returns

| Field   | Type   | Description                                |
|---------|--------|--------------------------------------------|
| geodata | object | Geolocation data for the specified IP address |
| valid   | bool   | Whether the operation was successful       |

### Geodata Object Fields

| Field              | Type   | Description                                       |
|--------------------|--------|---------------------------------------------------|
| ip                 | string | The IP address that was looked up                 |
| ip_addr            | string | The IP address in standard format                 |
| asn                | string | Autonomous System Number                          |
| carrier            | string | Network carrier name                              |
| city               | string | City name                                         |
| city_cf            | number | City confidence factor (0-100)                    |
| continent          | string | Continent name                                    |
| country            | string | Country name                                      |
| country_cf         | number | Country confidence factor (0-100)                 |
| ip_routing_type    | string | Routing type (e.g., "fixed")                      |
| latitude           | string | Geographic latitude                               |
| longitude          | string | Geographic longitude                              |
| organization       | string | Organization name                                 |
| organization_type  | string | Type of organization                              |
| region             | string | Geographic region                                 |
| state              | string | State or province name                            |
| state_cf           | number | State confidence factor (0-100)                   |
| state_code         | string | State or province code                            |

## Error Response

| Field   | Type   | Description                                |
|---------|--------|--------------------------------------------|
| error   | string | Error message if the operation failed      |
| valid   | bool   | false                                      |

## Examples

### Request
```json
{
  "ip": "8.8.8.8"
}
```

### Response
```json
{
  "geodata": {
    "asn": "15169",
    "carrier": "google",
    "city": "glenmont",
    "city_cf": 80,
    "continent": "north america",
    "country": "united states",
    "country_cf": 99,
    "ip_addr": "8.8.8.8",
    "ip_routing_type": "fixed",
    "latitude": "40.537",
    "longitude": "-82.12859",
    "organization": "google",
    "organization_type": "Internet Service Provider",
    "region": "great lakes",
    "state": "ohio",
    "state_cf": 95,
    "state_code": "oh",
    "ip": "8.8.8.8"
  },
  "valid": true
}
```

### Error Example
```json
{
  "error": "Error retrieving IP geodata for 8.8.8.8: Invalid IP address format",
  "valid": false
}
```

## Notes
- This tool uses Microsoft Sentinel's IP geodata enrichment API
- Unlike other Sentinel APIs, this enrichment API does not require a workspace_name parameter
- Confidence factors (CF) indicate the reliability of the location data on a scale of 0-100
- The tool will return all available geolocation data for the IP address
- Some fields may be missing if the data is not available for the specific IP address

## Permissions Required
- Azure Resource Group Reader access or higher
- Microsoft.SecurityInsights/enrichment/read permission

## Related Tools
- sentinel_domain_whois_get - Get WHOIS information for a domain
````

## File: resources/tool_docs/sentinel_logs_search_with_dummy_data.md
````markdown
# Sentinel Query With Dummy Data Tool

## Overview
The `sentinel_logs_search_with_dummy_data` tool allows security analysts to safely test Microsoft Sentinel KQL queries against mock data without accessing or modifying production data. It leverages the KQL `datatable` construct to create a temporary table from user-supplied mock records, then rebinds the original query's table reference to this mock table. The query logic remains unchanged, ensuring high-fidelity testing and validation.

---

## Parameters
| Name           | Type    | Required | Description                                                |
|----------------|---------|----------|------------------------------------------------------------|
| query          | string  | Yes      | The original KQL query to test.                            |
| mock_data_xml  | string  | No*      | XML string containing mock records (preferred format).     |
| mock_data_csv  | string  | No*      | CSV string with header row and mock records.               |
| table_name     | string  | No       | The table name to substitute in the query (default: TestTable). |

*At least one of mock_data_xml or mock_data_csv must be provided.

---

## Output Fields
| Field           | Type    | Description                                                                 |
|-----------------|---------|-----------------------------------------------------------------------------|
| valid           | bool    | Whether the query executed successfully.                                     |
| errors          | array   | List of error messages, if any.                                             |
| error           | string  | Main error message, if any.                                                 |
| original_query  | string  | The original KQL query as provided.                                         |
| table_name      | string  | The table name used in substitution.                                        |
| datatable_var   | string  | The variable name for the generated datatable.                              |
| test_query      | string  | The full KQL query executed (with datatable and let binding).               |
| result          | object  | Results from query execution (see below).                                   |

### Result Object
- `valid`: bool
- `errors`: array
- `query`: string (the full executed query)
- `result_count`: int
- `columns`: array of column descriptors
- `rows`: array of result records
- `execution_time_ms`: int
- `warnings`: array
- `message`: string

---

## Example Usage
### Example 1: Device Code Authentication Detection
**Example 1: Using XML Format (Preferred)**
```
query:
SigninLogs
| where TimeGenerated > ago(1d)
| where AuthenticationProtocol =~ "deviceCode" \
    or OriginalTransferMethod =~ "deviceCodeFlow"
| project TimeGenerated,
    UserPrincipalName,
    UserDisplayName,
    UserId,
    IPAddress,
    Location,
    AppDisplayName,
    ClientAppUsed,
    AuthenticationProtocol,
    OriginalTransferMethod,
    DeviceDetail,
    Status,
    ResourceDisplayName
| extend AlertDetails = pack(
    "UserId", UserId,
    "ClientApp", ClientAppUsed,
    "AppDisplayName", AppDisplayName,
    "Protocol", AuthenticationProtocol,
    "TransferMethod", OriginalTransferMethod,
    "DeviceInfo", DeviceDetail
)
| extend Reason = "Device Code Authentication Flow detected which may indicate unauthorized access if not used with input-constrained devices"
| extend timestamp = TimeGenerated, AccountCustomEntity = UserPrincipalName, IPCustomEntity = IPAddress

mock_data_xml:
<rows>
  <row>
    <TimeGenerated>2025-04-22T10:15:00Z</TimeGenerated>
    <UserPrincipalName>alice@contoso.com</UserPrincipalName>
    <UserDisplayName>Alice Smith</UserDisplayName>
    <UserId>alice123</UserId>
    <IPAddress>192.168.1.1</IPAddress>
    <Location>Sydney, Australia</Location>
    <AppDisplayName>Microsoft Office</AppDisplayName>
    <ClientAppUsed>Mobile App</ClientAppUsed>
    <AuthenticationProtocol>deviceCode</AuthenticationProtocol>
    <OriginalTransferMethod></OriginalTransferMethod>
    <DeviceDetail>
      <deviceId>dev123</deviceId>
      <displayName>iPhone 15</displayName>
      <operatingSystem>iOS</operatingSystem>
      <browser>Edge</browser>
    </DeviceDetail>
    <Status>
      <errorCode>0</errorCode>
      <additionalDetails>Success</additionalDetails>
    </Status>
    <ResourceDisplayName>Microsoft Graph</ResourceDisplayName>
  </row>
  <row>
    <TimeGenerated>2025-04-22T11:30:00Z</TimeGenerated>
    <UserPrincipalName>bob@contoso.com</UserPrincipalName>
    <UserDisplayName>Bob Jones</UserDisplayName>
    <UserId>bob456</UserId>
    <IPAddress>10.0.0.5</IPAddress>
    <Location>Melbourne, Australia</Location>
    <AppDisplayName>Azure Portal</AppDisplayName>
    <ClientAppUsed>Browser</ClientAppUsed>
    <AuthenticationProtocol>oauth2</AuthenticationProtocol>
    <OriginalTransferMethod>deviceCodeFlow</OriginalTransferMethod>
    <DeviceDetail>
      <deviceId>dev456</deviceId>
      <displayName>Windows Laptop</displayName>
      <operatingSystem>Windows</operatingSystem>
      <browser>Chrome</browser>
    </DeviceDetail>
    <Status>
      <errorCode>0</errorCode>
      <additionalDetails>Success</additionalDetails>
    </Status>
    <ResourceDisplayName>Azure Portal</ResourceDisplayName>
  </row>
</rows>

table_name: SigninLogs
```

**Example 2: Using CSV Format (Alternative)**
```
query:
SecurityEvent 
| where EventID == 4624
| where AccountType == "User"
| project TimeGenerated, Computer, Account, IpAddress

mock_data_csv:
TimeGenerated,Computer,Account,AccountType,EventID,IpAddress
2025-04-22T10:15:00Z,DC01,JohnDoe,User,4624,192.168.1.100
2025-04-22T11:30:00Z,DC01,JaneDoe,User,4624,192.168.1.101
2025-04-22T12:45:00Z,DC02,AdminUser,User,4624,10.0.0.50

table_name: SecurityEvent
```

**Output**
```
{
  "valid": true,
  "errors": [],
  "error": "",
  "original_query": "SigninLogs | where TimeGenerated > ago(1d) ...",
  "table_name": "SigninLogs",
  "datatable_var": "SigninLogsDummy",
  "test_query": "let SigninLogsDummy = datatable( ... ); let SigninLogs = SigninLogsDummy; ...",
  "result": {
    "valid": true,
    "errors": [],
    "result_count": 3,
    "columns": [ ... ],
    "rows": [ ... ],
    "execution_time_ms": 3325,
    "warnings": [],
    "message": "Query executed successfully"
  }
}
```

---

## Usage Notes
- Supports two data input formats:
  - **XML Format (preferred)**: Better for complex data with nested structures
  - **CSV Format**: Simpler option for flat tabular data
- The tool automatically infers the correct KQL types for each column, including `datetime` for ISO8601 strings.
- Handles nested structures in XML (converted to dynamic objects in KQL)
- The original query logic is preserved; only the data source is swapped for the mock datatable.
- No production or sensitive data is accessed or modified.
- Useful for detection rule development, debugging, documentation, and training.

---

## Error Cases
- If no mock data is provided in either XML or CSV format, the tool will return a helpful error with examples.
- If the XML or CSV data cannot be parsed, specific parsing errors will be returned.
- If the mock data is missing required columns referenced in the query, appropriate errors will be provided.
- KQL syntax errors in the original query will be reported.
- Any query execution errors are surfaced in the `errors` and `error` fields.

---

## References
- [KQL datatable documentation](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/datatableoperator)
- [Microsoft Sentinel KQL documentation](https://learn.microsoft.com/en-us/azure/sentinel/)

---

## Security and Privacy
- No workspace or environment-specific details are included in the documentation or output.
- All testing is performed in-memory and does not affect production data or configuration.

---
````

## File: resources/tool_docs/sentinel_logs_search.md
````markdown
# Sentinel Logs Search Tool Documentation

## Purpose
Runs a KQL query against Azure Monitor Logs (Log Analytics workspace) and returns structured results. Supports both MCP server and direct invocation for integration testing.

---

## Parameters
| Name        | Type   | Required | Description                                                         |
|-------------|--------|----------|---------------------------------------------------------------------|
| query       | string | Yes      | The Kusto Query Language (KQL) query to run.                        |
| timespan    | string | No       | Time window for the query (e.g., '1d', '12h', '30m'). Default: '1d' |

---

## Output Fields
| Name               | Type     | Description                                                                                 |
|--------------------|----------|---------------------------------------------------------------------------------------------|
| valid              | bool     | True if the query ran successfully, False otherwise.                                         |
| errors             | list     | List of error messages (empty if none).                                                      |
| error              | string   | Single error message (empty if none).                                                        |
| query              | string   | The KQL query that was executed.                                                             |
| timespan           | string   | The timespan used for the query.                                                             |
| result_count       | int      | Number of rows returned.                                                                     |
| columns            | list     | List of dicts describing columns: name, type, ordinal.                                       |
| rows               | list     | List of result rows (each is a dict mapping column name to value).                           |
| execution_time_ms  | int      | Query execution time in milliseconds.                                                        |
| warnings           | list     | List of warning messages (e.g., for large result sets).                                      |
| message            | string   | Human-readable status message.                                                                |

---

## Example Request
```
{
  "query": "Heartbeat | take 5"
}
```

---

## Example Response
```
{
  "valid": true,
  "errors": [],
  "query": "Heartbeat | take 5",
  "timespan": "1d",
  "result_count": 0,
  "columns": [
    {"name": "TenantId", "type": "string", "ordinal": 0},
    {"name": "SourceSystem", "type": "string", "ordinal": 1},
    {"name": "TimeGenerated", "type": "string", "ordinal": 2},
    ...
  ],
  "rows": [],
  "execution_time_ms": 1099,
  "warnings": [],
  "message": "Query executed successfully"
}
```

---

## Usage Notes
- The tool supports any valid KQL query against the configured Log Analytics workspace.
- If no results are returned, `rows` will be an empty list but `columns` will describe the expected schema.
- If the query requests a large result set (e.g., `take 10000`), a warning will be included in `warnings`.
- Timespan defaults to '1d' if not specified.

---

## Error Cases
| Error Message                                              | When it Occurs                                                    |
|-----------------------------------------------------------|-------------------------------------------------------------------|
| Missing required parameter: query                         | The `query` parameter was not provided.                           |
| Azure Monitor Logs client or workspace_id is not initialized. Check your credentials and configuration. | Azure credentials or workspace info missing or invalid.           |
| Query timed out after 60 seconds                          | The query did not complete within the timeout window.              |
| Error executing query: <details>                          | Any other unexpected error during query execution.                 |

---

## See Also
- [sentinel_query_validate.md](sentinel_query_validate.md)
- [Azure Monitor KQL documentation](https://docs.microsoft.com/azure/azure-monitor/logs/query-language)

---

*This documentation uses only fictional or placeholder values and never exposes real workspace or credential details.*
````

## File: resources/tool_docs/sentinel_logs_table_details_get.md
````markdown
# Tool: sentinel_logs_table_details_get

## Purpose
Get details (metadata, retention, row count, etc.) for a Log Analytics table.

## Parameters
| Name       | Type | Required | Description                                 |
|------------|------|----------|---------------------------------------------|
| table_name | str  | Yes      | Name of the table to retrieve details for.  |

## Output Fields
| Name                     | Type   | Description                                |
|--------------------------|--------|--------------------------------------------|
| table                    | str    | Name of the table.                         |
| lastUpdated              | str    | ISO timestamp of last data update.         |
| rowCount                 | int    | Number of rows in the table.               |
| retentionInDays          | int    | Hot retention period (days).               |
| archiveRetentionInDays   | int    | Archive retention period (days), if present|
| totalRetentionInDays     | int    | Total retention period (days).             |
| plan                     | str    | Table plan (if available).                 |
| provisioningState        | str    | Provisioning state (if available).         |
| restoredLogs             | any    | Restored logs information (if available).  |
| tableSubType             | str    | Table subtype (if available).              |
| tableType                | str    | Table type (if available).                 |
| systemData               | any    | System data (if available).                |
| description              | str    | Table description (if available).          |
| isInherited              | bool   | If retention is inherited.                 |
| isTotalRetentionInherited| bool   | If total retention is inherited.           |
| errors                   | list   | List of error messages (if any).           |
| error                    | str    | Error message (optional, present if error occurred)|

## Example Request
```json
{
  "table_name": "SignInLogs"
}
```

## Example Response

### Typical Response (with available metadata)
```json
{
  "table": "AzureActivity",
  "lastUpdated": "2025-04-25T03:00:46.511607Z",
  "rowCount": 871,
  "retentionInDays": 90,
  "totalRetentionInDays": null,
  "archiveRetentionInDays": null,
  "plan": null,
  "provisioningState": null,
  "tableType": null,
  "description": null,
  "isInherited": null,
  "isTotalRetentionInherited": null
}
```

### Response with Errors
```json
{
  "table": "NonExistentTable",
  "retentionInDays": null,
  "totalRetentionInDays": null,
  "archiveRetentionInDays": null,
  "plan": null,
  "provisioningState": null,
  "tableType": null,
  "description": null,
  "isInherited": null,
  "isTotalRetentionInherited": null,
  "lastUpdated": null,
  "rowCount": 0,
  "errors": ["REST API: No data returned for table metadata.", "KQL error (lastUpdated): Table not found"]
}
```

## Usage Notes
- Combines KQL and REST API metadata for completeness.
- Returns all fields even if some are None.
- Uses direct REST API calls with API version 2017-04-26-preview for metadata retrieval.
- Retention information (retentionInDays) is typically available for most tables.
- Some metadata fields may be null depending on the table type and Azure environment configuration.

## Error Cases
| Error Message                                        | Cause                                       |
|----------------------------------------------------|---------------------------------------------|
| Missing required parameter: table_name               | Table name parameter is missing             |
| REST API: Missing required parameters...            | Missing Azure resource configuration        |
| REST API: No data returned for table metadata.      | API returned no data for the specified table|
| REST API: No properties found in table metadata...  | API response missing properties field       |
| REST API call error: ...                            | Error during REST API call                  |
| KQL error (lastUpdated): ...                        | Error querying for last updated timestamp   |
| KQL error (rowCount): ...                           | Error querying for row count                |
| KQL timeout: ...                                    | KQL query exceeded time limit               |

## See Also
- [sentinel_logs_tables_list.md](sentinel_logs_tables_list.md)
- [sentinel_logs_table_schema_get.md](sentinel_logs_table_schema_get.md)
````

## File: resources/tool_docs/sentinel_logs_table_schema_get.md
````markdown
# Tool: sentinel_logs_table_schema_get

## Purpose
Get schema (columns/types) for a Log Analytics table.

## Parameters
| Name      | Type | Required | Description                                   |
|-----------|------|----------|-----------------------------------------------|
| table     | str  | Yes      | Name of the table to retrieve schema for.     |

## Output Fields
| Name   | Type | Description                                        |
|--------|------|----------------------------------------------------|
| table  | str  | Name of the table.                                 |
| schema | list | List of columns with keys: name (str), type (str)  |
| error  | str  | Error message (optional, present if error occurred)|

## Example Request
```json
{
  "table": "SignInLogs"
}
```

## Example Response
```json
{
  "table": "SignInLogs",
  "schema": [
    { "name": "TimeGenerated", "type": "datetime" },
    { "name": "UserPrincipalName", "type": "string" },
    { "name": "AppDisplayName", "type": "string" },
    { "name": "IPAddress", "type": "string" },
    { "name": "ResultType", "type": "int" }
  ]
}
```

## Usage Notes
- Returns all columns and their types for the specified table.
- Uses KQL to fetch schema.

## Error Cases
| Error Message                    | Cause                        |
|----------------------------------|------------------------------|
| Table name is required.          | Missing required parameter   |
| KQL error: ...                   | KQL query failed             |
| REST API client error: ...       | REST API call failed         |

## See Also
- [sentinel_logs_tables_list.md](sentinel_logs_tables_list.md)
- [sentinel_logs_table_details_get.md](sentinel_logs_table_details_get.md)
````

## File: resources/tool_docs/sentinel_logs_tables_list.md
````markdown
# Tool: sentinel_logs_tables_list

## Purpose
List available tables in the Log Analytics workspace.

## Parameters
| Name           | Type   | Required | Description                                                    |
|----------------|--------|----------|----------------------------------------------------------------|
| filter_pattern | str    | No       | Pattern to filter table names (case-insensitive substring).    |

## Output Fields
| Name         | Type   | Description                                                      |
|--------------|--------|------------------------------------------------------------------|
| found        | int    | Number of tables found.                                          |
| tables       | list   | List of tables with keys: name (str), lastUpdated (str), rowCount (int) |
| error        | str    | Error message (optional, present if an error occurred).           |

## Example Request
```json
{
  "filter_pattern": "SignIn"
}
```

## Example Response
```json
{
  "found": 2,
  "tables": [
    { "name": "SignInLogs", "lastUpdated": "2025-04-22T14:53:00Z", "rowCount": 485120 },
    { "name": "SignInSummary", "lastUpdated": "2025-04-22T14:50:00Z", "rowCount": 12480 }
  ]
}
```

## Usage Notes
- Returns all tables if `filter_pattern` is not provided.
- Uses KQL and REST API for comprehensive table info.
- Caches results for performance.

## Error Cases
| Error Message                                               | Cause                                      |
|------------------------------------------------------------|--------------------------------------------|
| Azure Logs client is not initialized. Check your credentials and configuration. | Credentials or config missing/invalid       |
| No tables found.                                           | No tables exist or filter excludes all      |
| KQL error: ...                                             | KQL query failed                           |
| REST API client error: ...                                 | REST API call failed                       |

## See Also
- [sentinel_logs_table_schema_get.md](sentinel_logs_table_schema_get.md)
- [sentinel_logs_table_details_get.md](sentinel_logs_table_details_get.md)
````

## File: resources/tool_docs/sentinel_metadata_get.md
````markdown
# sentinel_metadata_get

**Description:**
Get details for specific Sentinel metadata by ID.

**Parameters:**
- `metadata_id` (str, required): The ID or short name of the metadata object to retrieve (can be either the full ARM resource ID or just the short name, e.g., `analyticsrule-<guid>`).

**Output:**
```json
{
  "metadata": {
    "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/metadata/analyticsrule-<guid>",
    "name": "analyticsrule-<guid>",
    "kind": "AnalyticsRule",
    "content_id": "<content-id>",
    "version": "2.0.4",
    "parent_id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/alertRules/<guid>",
    "author": {
      "name": "Microsoft",
      "email": "support@microsoft.com"
    },
    "source": {
      "kind": "Solution",
      "name": "Microsoft 365",
      "source_id": "azuresentinel.azure-sentinel-solution-office365"
    },
    "support": {
      "tier": "Microsoft",
      "name": "Microsoft Corporation",
      "email": "support@microsoft.com",
      "link": "https://support.microsoft.com/"
    },
    "categories": null,
    "dependencies": null,
    "created": "",
    "last_modified": ""
  },
  "valid": true,
  "errors": []
}
```

**Error Handling:**
If the metadata ID is invalid or not found, the output will look like:
```json
{
  "metadata": {},
  "valid": false,
  "errors": ["Error retrieving metadata: Operation returned an invalid status 'Not Found'"],
  "error": "Error retrieving metadata: Operation returned an invalid status 'Not Found'"
}
```


**Error Handling:**
If the ID is invalid or any error occurs, the output includes an `error` key and a descriptive message. The `errors` list will contain error messages, if any.

**Azure Context Fallback:**
Supports both MCP server and direct invocation. Falls back to environment variables if MCP context is unavailable.

**Example Usage:**
Request with short name:
```json
{
  "tool": "sentinel_metadata_get",
  "kwargs": {"metadata_id": "analyticsrule-<guid>"}
}
```
Request with full ARM resource ID:
```json
{
  "tool": "sentinel_metadata_get",
  "kwargs": {"metadata_id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/metadata/analyticsrule-<guid>"}
}
```

**Example Response:**
```json
{
  "metadata": {
    "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/metadata/analyticsrule-<guid>",
    "name": "analyticsrule-<guid>",
    "kind": "AnalyticsRule",
    "content_id": "<content-id>",
    "version": "2.0.4",
    "parent_id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/alertRules/<guid>",
    "author": {
      "name": "Microsoft",
      "email": "support@microsoft.com"
    },
    "source": {
      "kind": "Solution",
      "name": "Microsoft 365",
      "source_id": "azuresentinel.azure-sentinel-solution-office365"
    },
    "support": {
      "tier": "Microsoft",
      "name": "Microsoft Corporation",
      "email": "support@microsoft.com",
      "link": "https://support.microsoft.com/"
    },
    "categories": null,
    "dependencies": null,
    "created": "",
    "last_modified": ""
  },
  "valid": true,
  "errors": []
}
```

**Example Error Response:**
```json
{
  "metadata": {},
  "valid": false,
  "errors": ["Error retrieving metadata: Operation returned an invalid status 'Not Found'"],
  "error": "Error retrieving metadata: Operation returned an invalid status 'Not Found'"
}
```
````

## File: resources/tool_docs/sentinel_metadata_list.md
````markdown
# sentinel_metadata_list

**Description:**
List all Sentinel metadata in the current workspace.

**Parameters:**
_None required. Context is extracted from MCP server or environment variables._

**Output:**
```
{
  "metadata": [
    {
      "id": "<metadata-id>",
      "name": "<metadata-name>",
      "kind": "<kind>",
      "content_id": "<content-id>",
      "version": "<version>",
      "parent_id": "<parent-id>",
      "author": { /* author object */ },
      "source": { /* source object */ },
      "support": { /* support object */ },
      "categories": null,
      "dependencies": null,
      "created": "<timestamp>",
      "last_modified": "<timestamp>"
      // ...additional fields depending on Azure API
    }
  ],
  "valid": true,
  "errors": [],
  "error": "<error-message-if-any>"
}
```

**Error Handling:**
If any error occurs, the output includes an `error` key and a descriptive message. The `errors` list will contain error messages, if any.

**Azure Context Fallback:**
Supports both MCP server and direct invocation. Falls back to environment variables if MCP context is unavailable.

**Example Usage:**
```json
{
  "tool": "sentinel_metadata_list",
  "kwargs": {}
}
```

**Example Response:**
```json
{
  "metadata": [
    {
      "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/metadata/analyticsrule-<guid>",
      "name": "analyticsrule-<guid>",
      "kind": "AnalyticsRule",
      "content_id": "<content-id>",
      "version": "2.0.4",
      "parent_id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/alertRules/<guid>",
      "author": "<author-object>",
      "source": "<source-object>",
      "support": "<support-object>",
      "categories": null,
      "dependencies": null,
      "created": "",
      "last_modified": ""
    },
    {
      "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/metadata/huntingquery-<guid>",
      "name": "huntingquery-<guid>",
      "kind": "HuntingQuery",
      "content_id": "<content-id>",
      "version": "2.0.1",
      "parent_id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/savedSearches/<guid>",
      "author": "<author-object>",
      "source": "<source-object>",
      "support": "<support-object>",
      "categories": null,
      "dependencies": null,
      "created": "",
      "last_modified": ""
    }
    // ...more metadata items
  ],
  "valid": true,
  "errors": [],
  "error": null
}
```
{
  "tool": "sentinel_metadata_list",
  "kwargs": {}
}
```
````

## File: resources/tool_docs/sentinel_ml_analytics_setting_get.md
````markdown
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
````

## File: resources/tool_docs/sentinel_ml_analytics_settings_list.md
````markdown
# sentinel_ml_analytics_settings_list

**Description:**
List all Sentinel ML analytics settings in the current workspace.

**Parameters:**
_None required. Context is extracted from MCP server or environment variables._

**Output:**
```
{
  "settings": [
    {
      "id": "<setting-id>",
      "name": "<setting-name>",
      "description": "<description>",
      "enabled": true|false
      // ...additional fields depending on Azure API
    }
  ],
  "valid": true,
  "errors": [],
  "error": "<error-message-if-any>"
}
```

**Error Handling:**
If any error occurs, the output includes an `error` key and a descriptive message. The `errors` list will contain error messages, if any.

**Azure Context Fallback:**
Supports both MCP server and direct invocation. Falls back to environment variables if MCP context is unavailable.

**Example Usage:**
```json
{
  "tool": "sentinel_ml_analytics_settings_list",
  "kwargs": {}
}
```

**Example Response:**
```json
{
  "settings": [
    {
      "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/securityMLAnalyticsSettings/<setting-guid>",
      "name": "b40a7a5b-5d39-46fe-a79e-2acdb38e1ce7",
      "description": "This algorithm detects an unusually high volume of AWS cloud trail log console failed login events per group user account within the last day. The model is trained on the previous 21 days of AWS cloud trail log events on group user account basis. This activity may indicate that the account is compromised.",
      "enabled": true
    },
    {
      "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/securityMLAnalyticsSettings/<setting-guid>",
      "name": "29094df8-e0c7-4475-a74c-bda74a07affb",
      "description": "This algorithm detects an unusually high volume of successful logins per user account by different logon types. The model is trained on the previous 21 days of security event ID 4624 on an account. It indicates anomalous high volume of successful logins in the last day.",
      "enabled": true
    }
    // ...more settings
  ],
  "valid": true,
  "errors": [],
  "error": null
}
```
{
  "tool": "sentinel_ml_analytics_settings_list",
  "kwargs": {}
}
```
````

## File: resources/tool_docs/sentinel_query_validate.md
````markdown
# Tool: sentinel_query_validate (KQLValidateTool)

## Purpose
Validates the syntax of a provided KQL (Kusto Query Language) query string locally, without executing it against a workspace. This tool is used to check for KQL syntax errors before attempting to run a query in Microsoft Sentinel or Log Analytics.

## Parameters
| Name       | Type   | Required | Description                                                      |
|------------|--------|----------|------------------------------------------------------------------|
| query      | string | Yes      | The KQL query string to validate.                                |

- The parameter can be provided directly as `query` or nested within a `kwargs` dictionary for compatibility with various invocation patterns.

## Output Fields
| Name    | Type    | Description                                                                 |
|---------|---------|-----------------------------------------------------------------------------|
| valid   | bool    | True if the KQL syntax is valid; False otherwise.                            |
| errors  | list    | List of error messages if validation fails; empty if valid.                   |
| result  | string  | Success message if valid, omitted if invalid.                                |
| error   | string  | Error message if validation fails or if a required parameter is missing.      |

## Example Requests and Responses

### 1. Simple Filter Query
**Request:**
```json
{
  "query": "SecurityEvent | where EventID == 4625"
}
```
**Response:**
```json
{
  "result": "Query validation passed. The KQL syntax appears to be correct.",
  "valid": true,
  "errors": []
}
```

### 2. Aggregation by Account and Hour
**Request:**
```json
{
  "query": "SecurityEvent | where EventID = 4625 | summarize Count=count() by Account, bin(TimeGenerated, 1h)"
}
```
**Response:**
```json
{
  "result": "Query validation passed. The KQL syntax appears to be correct.",
  "valid": true,
  "errors": []
}
```

### 3. Multi-step Aggregation and Projection
**Request:**
```json
{
  "query": "SecurityEvent | summarize Count=count() by Account, bin(TimeGenerated, 1h) | where Count > 10 | project Account, Count, TimeGenerated"
}
```
**Response:**
```json
{
  "result": "Query validation passed. The KQL syntax appears to be correct.",
  "valid": true,
  "errors": []
}
```

### 4. Query with Syntax Error (Missing Parenthesis)
**Request:**
```json
{
  "query": "SecurityEvent | where EventID = 4625 | summarize Count=count() by Account, bin(TimeGenerated, 1h | project Account, Count, TimeGenerated"
}
```
**Response:**
```json
{
  "error": "KQL validation failed:
Unknown position: Expected: )",
  "valid": false,
  "errors": ["Unknown position: Expected: )"]
}
```

## Usage Notes
- This tool does not execute the query or check for schema correctness; it only validates KQL syntax.
- If the required parameter `query` is missing, the tool returns an error and sets `valid` to false.
- Supports both MCP server and direct invocation (integration tests).
- The tool leverages the local `utilities.kql_validator.validate_kql` function for validation logic.

## Error Cases
| Error Condition                | Error Message                                         |
|-------------------------------|------------------------------------------------------|
| Missing query                  | "Missing required parameter: query"                  |
| KQL validation unavailable     | "KQL validation unavailable" (from validator errors) |
| General exception              | "An error occurred while validating the query..."    |

## See Also

- [sentinel_logs_search](sentinel_logs_table_get.md): Executes KQL queries against Log Analytics tables.

---

_This documentation follows the MCP tool documentation template as required by project architecture guidelines._
````

## File: resources/tool_docs/sentinel_source_control_get.md
````markdown
# sentinel_source_control_get

**Description:**
Get details for a specific Sentinel source control by ID.

**Parameters:**
- `source_control_id` (str, required): The ID of the source control to retrieve.

**Output:**
```
{
  "source_control": {
    "id": "<source-control-id>",
    "name": "<source-control-name>",
    "description": "<description>"
    // ...additional fields depending on Azure API
  },
  "valid": true|false,
  "errors": [<error-messages>],
  "error": "<error-message-if-any>"
}
```

**Error Handling:**
If the ID is invalid or any error occurs, the output includes an `error` key and a descriptive message. The `errors` list will contain error messages, if any.

**Azure Context Fallback:**
Supports both MCP server and direct invocation. Falls back to environment variables if MCP context is unavailable.

**Example Usage:**
```json
{
  "tool": "sentinel_source_control_get",
  "kwargs": {"source_control_id": "<source-control-id>"}
}
```

**Example Response (invalid ID):**
```json
{
  "source_control": {},
  "valid": false,
  "errors": [
    "Error retrieving source control: (BadRequest) The value '<source-control-id>' is not valid.
Code: BadRequest
Message: The value '<source-control-id>' is not valid."
  ],
  "error": "Error retrieving source control: (BadRequest) The value '<source-control-id>' is not valid.
Code: BadRequest
Message: The value '<source-control-id>' is not valid."
}
```
{
  "tool": "sentinel_source_control_get",
  "kwargs": {"source_control_id": "<source-control-id>"}
}
```
````

## File: resources/tool_docs/sentinel_source_controls_list.md
````markdown
# sentinel_source_controls_list

**Description:**
List all Sentinel source controls in the current workspace.

**Parameters:**
_None required. Context is extracted from MCP server or environment variables._

**Output:**
```
{
  "source_controls": [
    {
      "id": "<source-control-id>",
      "name": "<source-control-name>",
      "description": "<description>"
      // ...additional fields depending on Azure API
    }
  ],
  "valid": true,
  "errors": [],
  "error": "<error-message-if-any>"
}
```

**Error Handling:**
If any error occurs, the output includes an `error` key and a descriptive message. The `errors` list will contain error messages, if any.

**Azure Context Fallback:**
Supports both MCP server and direct invocation. Falls back to environment variables if MCP context is unavailable.

**Example Usage:**
```json
{
  "tool": "sentinel_source_controls_list",
  "kwargs": {}
}
```

**Example Response:**
```json
{
  "source_controls": [],
  "valid": true,
  "errors": [],
  "error": null
}
```
{
  "tool": "sentinel_source_controls_list",
  "kwargs": {}
}
```
````

## File: resources/tool_docs/sentinel_watchlist_get.md
````markdown
# sentinel_watchlist_get

## Purpose
Retrieves detailed information about a specific Microsoft Sentinel watchlist by its alias. Provides comprehensive metadata about the watchlist including its properties, creation time, and item count.

## Parameters
| Name           | Type   | Required | Description                                                      |
|----------------|--------|----------|------------------------------------------------------------------|
| watchlist_alias| string | Yes      | The alias of the Sentinel watchlist to retrieve.                 |
| kwargs         | dict   | No       | Additional parameters (for nested invocation compatibility).      |

## Output Fields
The tool returns a dictionary with the following structure:

| Key       | Type    | Description                                          |
|-----------|---------|------------------------------------------------------|
| watchlist | dict    | Detailed information about the requested watchlist.  |
| valid     | boolean | Indicates if the operation completed successfully.   |
| error     | string  | Present only if an error occurred.                   |

### Example `watchlist` fields:
- id: Full Azure resource ID of the watchlist
- name: Name of the watchlist
- alias: Alias used to reference the watchlist
- displayName: User-friendly display name of the watchlist
- description: Description of the watchlist's purpose
- provider: Provider of the watchlist (e.g., "Microsoft")
- source: Source of the watchlist data (e.g., "Local file")
- itemsSearchKey: Primary key column for the watchlist items
- created: Creation timestamp
- updated: Last update timestamp
- itemsCount: Number of items in the watchlist

## Example Request
```
{
  "watchlist_alias": "hva"
}
```

## Example Response
```
{
  "watchlist": {
    "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/Watchlists/hva",
    "name": "hva",
    "alias": "hva",
    "displayName": "High Value Assets",
    "description": "List of high value assets in the organization",
    "provider": "Microsoft",
    "source": "Local file",
    "itemsSearchKey": "Hostname",
    "created": "2025-04-20T08:15:30.422179Z",
    "updated": "2025-04-20T08:15:30.422179Z",
    "itemsCount": 10
  },
  "valid": true
}
```

## Usage Notes
- Returns detailed information about a specific watchlist identified by its alias.
- The watchlist_alias is case-sensitive and must exactly match the alias in Sentinel.
- Handles both MCP server and direct invocation (using environment variables for Azure context if needed).
- All errors are returned as a dict with an `error` key.

## Error Cases
- Missing or invalid `watchlist_alias` parameter.
- Watchlist not found with the specified alias.
- Azure SecurityInsights client initialization failure.
- Azure authentication errors.
- Insufficient permissions to access the watchlist.
- Network or service connectivity issues.

## See Also
- [sentinel_watchlists_list](sentinel_watchlists_list.md) — for listing all watchlists.
- [sentinel_watchlist_items_list](sentinel_watchlist_items_list.md) — for listing items in a watchlist.
````

## File: resources/tool_docs/sentinel_watchlist_item_get.md
````markdown
# sentinel_watchlist_item_get

## Purpose
Retrieves detailed information about a specific item in a Microsoft Sentinel watchlist. This tool allows you to get the complete data for an individual watchlist item identified by both the watchlist alias and the item's unique identifier.

## Parameters
| Name             | Type   | Required | Description                                                      |
|------------------|--------|----------|------------------------------------------------------------------|
| watchlist_alias  | string | Yes      | The alias of the Sentinel watchlist containing the item.         |
| watchlist_item_id| string | Yes      | The unique identifier of the watchlist item to retrieve.         |
| kwargs           | dict   | No       | Additional parameters (for nested invocation compatibility).      |

## Output Fields
The tool returns a dictionary with the following structure:

| Key           | Type    | Description                                          |
|---------------|---------|------------------------------------------------------|
| watchlistItem | dict    | Detailed information about the requested item.       |
| valid         | boolean | Indicates if the operation completed successfully.   |
| error         | string  | Present only if an error occurred.                   |

### Example `watchlistItem` fields:
- id: Full Azure resource ID of the watchlist item
- name: Unique identifier of the watchlist item
- itemsKeyValue: Value of the primary key for this item
- properties: Key-value pairs containing the actual data of the watchlist item
- watchlistAlias: The alias of the watchlist the item belongs to

## Example Request
```
{
  "watchlist_alias": "hva",
  "watchlist_item_id": "d3e30fa7-8909-409e-87f8-d087731da067"
}
```

## Example Response
```
{
  "watchlistItem": {
    "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/Watchlists/hva/WatchlistItems/d3e30fa7-8909-409e-87f8-d087731da067",
    "name": "d3e30fa7-8909-409e-87f8-d087731da067",
    "itemsKeyValue": "server001",
    "properties": {
      "Hostname": "server001",
      "IPAddress": "10.0.0.1",
      "Owner": "IT Department",
      "Classification": "Critical"
    },
    "watchlistAlias": "hva"
  },
  "valid": true
}
```

## Usage Notes
- Returns detailed information about a specific watchlist item identified by its ID.
- Both the watchlist_alias and watchlist_item_id are case-sensitive and must exactly match the values in Sentinel.
- The properties field contains the actual data of the watchlist item as key-value pairs.
- Handles both MCP server and direct invocation (using environment variables for Azure context if needed).
- All errors are returned as a dict with an `error` key.

## Error Cases
- Missing or invalid `watchlist_alias` parameter.
- Missing or invalid `watchlist_item_id` parameter.
- Watchlist not found with the specified alias.
- Watchlist item not found with the specified ID.
- Azure SecurityInsights client initialization failure.
- Azure authentication errors.
- Insufficient permissions to access the watchlist item.
- Network or service connectivity issues.

## See Also
- [sentinel_watchlists_list](sentinel_watchlists_list.md) — for listing all watchlists.
- [sentinel_watchlist_get](sentinel_watchlist_get.md) — for retrieving a specific watchlist.
- [sentinel_watchlist_items_list](sentinel_watchlist_items_list.md) — for listing all items in a watchlist.
````

## File: resources/tool_docs/sentinel_watchlist_items_list.md
````markdown
# sentinel_watchlist_items_list

## Purpose
Lists all items in a specific Microsoft Sentinel watchlist identified by its alias. Watchlist items are individual records stored in a watchlist that can be used for lookups and enrichment in Sentinel queries, analytics rules, and hunting.

## Parameters
| Name           | Type   | Required | Description                                                      |
|----------------|--------|----------|------------------------------------------------------------------|
| watchlist_alias| string | Yes      | The alias of the Sentinel watchlist to retrieve items from.      |
| kwargs         | dict   | No       | Additional parameters (for nested invocation compatibility).      |

## Output Fields
The tool returns a dictionary with the following structure:

| Key           | Type    | Description                                          |
|---------------|---------|------------------------------------------------------|
| watchlistItems| list    | List of watchlist item objects with their data.      |
| count         | integer | The number of watchlist items returned.              |
| watchlistAlias| string  | The alias of the watchlist the items belong to.      |
| valid         | boolean | Indicates if the operation completed successfully.   |
| error         | string  | Present only if an error occurred.                   |

### Example `watchlistItems` fields:
- id: Full Azure resource ID of the watchlist item
- name: Unique identifier of the watchlist item
- itemsKeyValue: Value of the primary key for this item
- properties: Key-value pairs containing the actual data of the watchlist item

## Example Request
```
{
  "watchlist_alias": "hva"
}
```

## Example Response
```
{
  "watchlistItems": [
    {
      "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/Watchlists/hva/WatchlistItems/<item-id>",
      "name": "<item-id>",
      "itemsKeyValue": "server001",
      "properties": {
        "Hostname": "server001",
        "IPAddress": "10.0.0.1",
        "Owner": "IT Department",
        "Classification": "Critical"
      }
    },
    {
      "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/Watchlists/hva/WatchlistItems/<item-id>",
      "name": "<item-id>",
      "itemsKeyValue": "server002",
      "properties": {
        "Hostname": "server002",
        "IPAddress": "10.0.0.2",
        "Owner": "Finance Department",
        "Classification": "High"
      }
    }
  ],
  "count": 2,
  "watchlistAlias": "hva",
  "valid": true
}
```

## Usage Notes
- Returns all items in a specific watchlist identified by its alias.
- The watchlist_alias is case-sensitive and must exactly match the alias in Sentinel.
- The properties field contains the actual data of the watchlist item as key-value pairs.
- If no items exist in the watchlist, returns an empty list with count 0.
- Handles both MCP server and direct invocation (using environment variables for Azure context if needed).
- All errors are returned as a dict with an `error` key.

## Error Cases
- Missing or invalid `watchlist_alias` parameter.
- Watchlist not found with the specified alias.
- Azure SecurityInsights client initialization failure.
- Azure authentication errors.
- Insufficient permissions to access the watchlist items.
- Network or service connectivity issues.

## See Also
- [sentinel_watchlists_list](sentinel_watchlists_list.md) — for listing all watchlists.
- [sentinel_watchlist_get](sentinel_watchlist_get.md) — for retrieving a specific watchlist.
- [sentinel_watchlist_item_get](sentinel_watchlist_item_get.md) — for retrieving a specific watchlist item.
````

## File: resources/tool_docs/sentinel_watchlists_list.md
````markdown
# sentinel_watchlists_list

## Purpose
Lists all Microsoft Sentinel watchlists in the current workspace. Watchlists are user-created tables that can be used to store data for lookups and enrichment in Sentinel queries, analytics rules, and hunting.

## Parameters
| Name   | Type | Required | Description                                                 |
|--------|------|----------|-------------------------------------------------------------|
| kwargs | dict | No       | Additional parameters (for nested invocation compatibility). |

## Output Fields
The tool returns a dictionary with the following structure:

| Key       | Type    | Description                                          |
|-----------|---------|------------------------------------------------------|
| watchlists| list    | List of watchlist objects with their metadata.       |
| count     | integer | The number of watchlists returned.                   |
| valid     | boolean | Indicates if the operation completed successfully.   |
| error     | string  | Present only if an error occurred.                   |

### Example `watchlists` fields:
- id: Full Azure resource ID of the watchlist
- name: Name of the watchlist
- alias: Alias used to reference the watchlist
- displayName: User-friendly display name of the watchlist
- description: Description of the watchlist's purpose
- provider: Provider of the watchlist (e.g., "Microsoft")
- source: Source of the watchlist data (e.g., "Local file")
- itemsSearchKey: Primary key column for the watchlist items
- created: Creation timestamp
- updated: Last update timestamp
- itemsCount: Number of items in the watchlist

## Example Request
```
{}
```

## Example Response
```
{
  "watchlists": [
    {
      "id": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.OperationalInsights/workspaces/<workspace-name>/providers/Microsoft.SecurityInsights/Watchlists/hva",
      "name": "hva",
      "alias": "hva",
      "displayName": "High Value Assets",
      "description": "List of high value assets in the organization",
      "provider": "Microsoft",
      "source": "Local file",
      "itemsSearchKey": "Hostname",
      "created": "2025-04-20T08:15:30.422179Z",
      "updated": "2025-04-20T08:15:30.422179Z",
      "itemsCount": 10
    }
  ],
  "count": 1,
  "valid": true
}
```

## Usage Notes
- Returns all watchlists in the current Microsoft Sentinel workspace.
- The response includes basic metadata about each watchlist.
- If no watchlists exist, returns an empty list with count 0.
- Handles both MCP server and direct invocation (using environment variables for Azure context if needed).
- All errors are returned as a dict with an `error` key.

## Error Cases
- Azure SecurityInsights client initialization failure.
- Azure authentication errors.
- Insufficient permissions to access watchlists.
- Network or service connectivity issues.

## See Also
- [sentinel_watchlist_get](sentinel_watchlist_get.md) — for retrieving a specific watchlist.
- [sentinel_watchlist_items_list](sentinel_watchlist_items_list.md) — for listing items in a watchlist.
````

## File: resources/tool_docs/sentinel_workspace_get.md
````markdown
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
````

## File: resources/tool_docs/tool_docs_get.md
````markdown
# Tool Docs Get Tool

**Tool Name:** `tool_docs_get`

## Overview
Returns the raw markdown content for a given documentation path in the `resources/tool_docs` directory.

## Parameters
- `path` (str, required): Relative path to the markdown doc (as returned by `tool_docs_list`).

## Output
- `content` (str): Raw markdown content of the file.
- If error, returns a dict with `error` (str) and may include `available_docs` (list[str]).

## Example Requests
### Get a specific documentation file
```
{
  "path": "sentinel_analytics_rule_get.md"
}
```

## Example Output
```
{
  "content": "# Sentinel Analytics Rule Get Tool

**Tool Name:** `sentinel_analytics_rule_get`
..."
}
```

## Error Handling
- Returns `error` if the file does not exist or is outside the docs directory.
- Returns `available_docs` if the requested file is missing, listing all available docs.

## MCP Compliance
- Inherits from `MCPToolBase`.
- Implements `async def run(self, ctx, **kwargs)`.
- Registered in `register_tools()`.
- Uses robust error handling.
````

## File: resources/tool_docs/tool_docs_list.md
````markdown
# Tool Docs List Tool

**Tool Name:** `tool_docs_list`

## Overview
Enumerates available Sentinel server documentation markdown paths in the `resources/tool_docs` directory.

## Parameters
- `prefix` (str, optional): Only include docs whose relative path starts with this prefix.

## Output
- `paths` (list[str]): List of relative markdown doc paths.
- If error, returns a dict with `error` (str).

## Example Requests
### List all documentation files
```
{
  "prefix": ""
}
```

### List documentation files starting with a specific prefix
```
{
  "prefix": "sentinel_analytics"
}
```

## Example Output
```
{
  "paths": [
    "sentinel_analytics_rule_get.md",
    "sentinel_analytics_rule_list.md",
    "sentinel_analytics_rules_count_by_tactic.md"
  ]
}
```

## Error Handling
- Returns `error` field if the docs directory cannot be read or other errors occur.

## MCP Compliance
- Inherits from `MCPToolBase`.
- Implements `async def run(self, ctx, **kwargs)`.
- Registered in `register_tools()`.
- Uses robust error handling.
````

## File: resources/tool_docs/tool_docs_search.md
````markdown
# Tool Docs Search Tool

**Tool Name:** `tool_docs_search`

## Overview
Performs a full-text search across documentation in the `resources/tool_docs` directory and returns matching paths.

## Parameters
- `query` (str, required): Regex or text to search for in docs.
- `k` (int, optional): Max number of results to return (default: 10).

## Output
- `hits` (list[str]): Relative doc paths containing a match.
- If error, returns a dict with `error` (str).

## Example Requests
### Search for docs containing the word "analytics"
```
{
  "query": "analytics"
}
```

### Search for docs containing the word "incident" (limit 2 results)
```
{
  "query": "incident",
  "k": 2
}
```

## Example Output
```
{
  "hits": [
    "sentinel_analytics_rule_get.md",
    "sentinel_analytics_rule_list.md"
  ]
}
```

## Error Handling
- Returns `error` if the search fails or required parameters are missing.

## MCP Compliance
- Inherits from `MCPToolBase`.
- Implements `async def run(self, ctx, **kwargs)`.
- Registered in `register_tools()`.
- Uses robust error handling.
````

## File: README.md
````markdown
# Microsoft Sentinel MCP Server

A [Model Context Protocol][mcp] (MCP) server for Microsoft Sentinel. This server enables read-only access to a Microsoft Sentinel instance, including advanced querying, incident viewing, and resource exploration for Azure Sentinel environments. It provides a modular and extensible platform for observation-only security operations and analysis.

---

## ⚠️ IMPORTANT SECURITY NOTICE ⚠️

**TEST ENVIRONMENTS ONLY**: This Microsoft Sentinel MCP server only supports read-only operations and is intended exclusively for TEST environments. It is not intended to be connected to production Sentinel instances.

**PRIVACY WARNING**: Connecting this server to a production Microsoft Entra ID (Azure AD) or Sentinel environment may expose sensitive user and directory data to LLM operators or public LLMs. Use only with non-production/test tenants, or a private LLM with MCP support.

**SECURITY WARNING**: Connecting a production Microsoft Sentinel instance to a public LLM poses significant privacy and security risks. Use only private, secured environments for production security operations.

---

## ✨ Features

- **KQL Query Execution**: Run and validate KQL queries, test with mock data
- **Log Analytics Management**: Workspace info, table listings and schemas
- **Security Incidents**: List and view detailed incident information
- **Analytics Rules**: List, view, and analyze by MITRE tactics/techniques
- **Rule Templates**: Access and analyze templates by MITRE framework
- **Hunting Queries**: List, view details, and analyze by tactic
- **Data Connectors**: List and view connector details
- **Watchlists**: Manage watchlists and their items
- **Threat Intelligence**: Domain WHOIS and IP geolocation lookups

- **Metadata & Source Control**: List and view repository details
- **ML Analytics**: Access ML analytics settings
- **Authorization**: View RBAC role assignments
- **Entra ID Users & Groups**: View user and group details from Microsoft Entra ID

---

## 🚀 Quick Start

### 1. Authenticate with Azure CLI

Before using the MCP server, you must have authenticated to Azure with an account that has access to a Microsoft Sentinel workspace:

```bash
az login
```

### 2. Clone the Repository

```bash
git clone https://github.com/dstreefkerk/ms-sentinel-mcp-server.git
cd ms-sentinel-mcp-server
```

### 3. Install with PowerShell Script (Recommended)

Use the provided PowerShell installation script to set up the MCP server:

```powershell
# Run from the repository root directory
.\install.ps1
```

The script will:
- Check for Python installation
- Create a virtual environment and install dependencies
- Generate a Claude Desktop configuration file
- Copy the configuration to your clipboard

After running the script, you can paste the configuration directly into your MCP client (Claude Desktop, Cursor, etc.).

### 4. Use the MCP server

The MCP server will be ready for use after you've configured your MCP client config with the relevant workspace info. 

Just remember that if you're using Azure CLI auth, you need to remove 
`AZURE_CLIENT_ID` and `AZURE_CLIENT_SECRET` from your MCP client config.

---

## 🧰 Tool Reference

Below are the available tools. For full documentation, see the `resources/tool_docs/` directory. Tool names and descriptions are kept in sync with the MCP server's tool registry, so that the MCP Client can retrieve them.

| Tool                                      | Category           | Description                                                      |
|-------------------------------------------|-------------------|------------------------------------------------------------------|
| `entra_id_list_users`                     | Entra ID          | List all users in Microsoft Entra ID (Azure AD)                  |
| `entra_id_get_user`                       | Entra ID          | Get a user by UPN or object ID from Entra ID                     |
| `entra_id_list_groups`                    | Entra ID          | List all groups in Microsoft Entra ID (Azure AD)                 |
| `entra_id_get_group`                      | Entra ID          | Get a group by object ID from Entra ID                           |
| `sentinel_logs_search`                    | KQL               | Run a KQL query against Azure Monitor Logs                       |
| `sentinel_query_validate`                 | KQL               | Validate KQL query syntax locally                                |
| `sentinel_logs_search_with_dummy_data`    | KQL               | Test a KQL query with mock data                                  |
| `sentinel_logs_tables_list`               | Log Analytics     | List available tables in the Log Analytics workspace             |
| `sentinel_logs_table_details_get`         | Log Analytics     | Get details for a Log Analytics table                            |
| `sentinel_logs_table_schema_get`          | Log Analytics     | Get schema for a Log Analytics table                             |
| `sentinel_workspace_get`                  | Log Analytics     | Get workspace information                                        |
| `sentinel_incident_details_get`           | Incidents         | Get detailed information about a specific Sentinel incident      |
| `sentinel_incident_list`                  | Incidents         | List security incidents in Microsoft Sentinel                    |
| `sentinel_analytics_rule_list`            | Analytics Rules   | List all analytics rules with key fields                         |
| `sentinel_analytics_rule_get`             | Analytics Rules   | Get details for a specific analytics rule                        |
| `sentinel_analytics_rules_count_by_tactic`| Analytics Rules   | Count Sentinel analytics rules by tactic                         |
| `sentinel_analytics_rules_count_by_technique` | Analytics Rules | Count Sentinel analytics rules by MITRE technique                |
| `sentinel_analytics_rule_templates_list`  | Rule Templates    | List all Sentinel analytics rule templates                       |
| `sentinel_analytics_rule_template_get`    | Rule Templates    | Get a specific Sentinel analytics rule template                  |
| `sentinel_analytics_rule_templates_count_by_tactic` | Rule Templates | Count Sentinel analytics rule templates by tactic         |
| `sentinel_analytics_rule_templates_count_by_technique` | Rule Templates | Count Sentinel analytics rule templates by MITRE technique |
| `sentinel_hunting_queries_list`           | Hunting           | List all Sentinel hunting queries with optional filtering         |
| `sentinel_hunting_query_get`              | Hunting           | Get full details of a Sentinel hunting query by name or ID       |
| `sentinel_hunting_queries_count_by_tactic`| Hunting           | Count Sentinel hunting queries by tactic                         |
| `sentinel_connectors_list`                | Data Connectors   | List data connectors                                             |
| `sentinel_connectors_get`                 | Data Connectors   | Get a specific data connector by ID                              |
| `sentinel_watchlists_list`                | Watchlists        | List all Sentinel watchlists                                     |
| `sentinel_watchlist_get`                  | Watchlists        | Get a specific Sentinel watchlist                                |
| `sentinel_watchlist_items_list`           | Watchlists        | List all items in a Sentinel watchlist                           |
| `sentinel_watchlist_item_get`             | Watchlists        | Get a specific item from a Sentinel watchlist                    |
| `sentinel_domain_whois_get`               | Threat Intel      | Get WHOIS information for a domain                               |
| `sentinel_ip_geodata_get`                 | Threat Intel      | Get geolocation data for an IP address                           |
| `sentinel_metadata_list`                  | Metadata          | List all Sentinel metadata in the current workspace              |
| `sentinel_metadata_get`                   | Metadata          | Get details for specific Sentinel metadata by ID                 |
| `sentinel_source_controls_list`           | Source Control    | List all Sentinel source controls in the current workspace       |
| `sentinel_source_control_get`             | Source Control    | Get details for a specific Sentinel source control by ID         |
| `sentinel_ml_analytics_settings_list`     | ML Analytics      | List all Sentinel ML analytics settings                          |
| `sentinel_ml_analytics_setting_get`       | ML Analytics      | Get a specific Sentinel ML analytics setting by name             |
| `sentinel_authorization_summary`          | Authorization     | Summarize Azure RBAC role assignments for Sentinel access        |
| `log_analytics_saved_searches_list`       | Saved Searches    | List all saved searches in a Log Analytics workspace             |
| `log_analytics_saved_search_get`          | Saved Searches    | Get a specific saved search from a Log Analytics workspace       |
---

## 🛠️ Usage

### Installing in Claude Desktop or similar Environments

Use the provided PowerShell installation script to set up the MCP server for Claude Desktop or other MCP-compatible clients:

```powershell
# Run from the repository root directory
.\install.ps1
```

The script will:
1. Check for Python installation
2. Create a virtual environment and install dependencies
3. Run post-installation steps
4. Generate a Claude Desktop configuration file
5. Copy the configuration to your clipboard

After running the script, you can paste the configuration directly into your MCP client (Claude Desktop, Cursor, etc.). The script generates Claude-compatible MCP Server configuration. Keep this in mind if you're going to use a different MCP client.

### Advanced Installation Options

#### Manual Environment Setup

If you prefer to set up the environment manually:

1. **Configure Environment Variables**

   Copy the provided template and fill in your Azure credentials:

   ```bash
   cp .env.example .env
   # Edit .env and set:
   # AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_SUBSCRIPTION_ID, AZURE_RESOURCE_GROUP, AZURE_WORKSPACE_NAME, AZURE_WORKSPACE_ID
   ```

2. **Install Dependencies (with uv)**

   ```bash
   uv venv
   uv pip install -e .
   ```

3. **Alternative Server Run Options**

   **Using MCP CLI:**
   ```bash
   mcp run wrapper.py
   ```

   **Development & Hot Reload:**
   ```bash
   mcp dev wrapper.py
   ```

   **SSE Mode (for IDEs):**
   ```bash
   python wrapper.py --sse
   ```

### Inspector UI

The MCP Inspector UI is available at http://127.0.0.1:6274 when running in dev mode (`mcp dev wrapper.py`).

---

## 🧩 Development

- **Resources:** Add Python files to `resources/` and implement a `register_resources(mcp)` function.
- **Tools:** Add Python files to `tools/` and implement a `register_tools(mcp)` function. Tools must follow the structure defined in `docs/tool-architecture-and-implementation-requirements.md`.
- **Prompts:** Add prompt templates to `prompts/` for LLM-driven workflows.

All components in the `resources/`, `tools/`, and `prompts/` directories are auto-discovered and registered at server startup. No manual imports are needed.

---

## 🔐 Authentication & Environment Variables

The MCP Server supports any authentication method supported by the Azure Python SDK's `DefaultAzureCredential`.

### Service Principal authentication instead of Azure CLI

Set up an App Registration in Azure and assign the following roles:

- `Log Analytics Reader`
- `Microsoft Sentinel Reader`

If you're feeling brave, you can also grant the App Registration the following Microsoft Graph permissions:

- `User.Read.All`
- `Group.Read.All`

Then, use the following environment variables in your `.env` file or MCP Server configuration:

- `AZURE_TENANT_ID`
- **`AZURE_CLIENT_ID`**
- **`AZURE_CLIENT_SECRET`**
- `AZURE_SUBSCRIPTION_ID`
- `AZURE_RESOURCE_GROUP`
- `AZURE_WORKSPACE_NAME`
- `AZURE_WORKSPACE_ID`

See `.env.example` for a template.

### Azure CLI Authentication

```bash
az login
```

If you use Azure CLI authentication, you can omit `AZURE_CLIENT_SECRET` and `AZURE_CLIENT_ID` from your config.

---

## 🐛 Debugging

Enable debug mode by setting the `MCP_DEBUG_LOG` environment variable to `true` in your `.env` file:

```
MCP_DEBUG_LOG=true
```

Logs are written to your temp directory as `sentinel_mcp_server.log`.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

[mcp]: https://modelcontextprotocol.io/
````
