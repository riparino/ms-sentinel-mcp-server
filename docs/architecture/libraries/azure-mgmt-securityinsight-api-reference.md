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