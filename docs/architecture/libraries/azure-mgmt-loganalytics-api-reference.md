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