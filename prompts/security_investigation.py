"""
FILE: prompts/security_investigation.py
DESCRIPTION:
    Provides security investigation prompts for the MCP server.
"""

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base


def register_prompts(mcp: FastMCP):
    """Register security investigation prompts."""

    @mcp.prompt("sentinel_hunting_investigate_ip", "Investigate an IP address")
    def investigate_ip_address(ip_address: str) -> list[base.Message]:
        """
        Investigate a potentially suspicious IP address in Microsoft Sentinel.

        Args:
            ip_address: The IP address to investigate
        """
        return [
            base.UserMessage(
                f"I need to investigate the IP address {ip_address} that appeared in our logs. What should I check?"
            ),
            base.AssistantMessage(
                """
I'll guide you through a structured investigation of this IP address. Here's what we should check:

First, let's determine where this IP appears in our environment:
1. Check for connections to/from this IP across your network
2. Identify which systems have communicated with this IP
3. Determine the volume and frequency of these communications

Then, we'll analyze the context and behavior:
4. Review the activities associated with this IP
5. Identify any unusual patterns or known malicious behaviors
6. Check if this IP appears in security incidents or alerts

Let me help you create KQL queries for each step of this investigation.
"""
            ),
            base.UserMessage(
                "That sounds like a good approach. Can you provide the KQL queries I should use?"
            ),
            base.AssistantMessage(
                f"""
Here are the KQL queries you can use to investigate IP address {ip_address}:

### 1. Check for connections to/from this IP

```kusto
// Look for this IP in network events
let ip = "{ip_address}";
DeviceNetworkEvents
| where TimeGenerated > ago(7d)
| where RemoteIP == ip or LocalIP == ip
| summarize ConnectionCount=count(), FirstSeen=min(TimeGenerated), LastSeen=max(TimeGenerated) by DeviceName, LocalIP, RemoteIP, RemotePort, InitiatingProcessFileName
| sort by ConnectionCount desc
```

### 2. Check for this IP in security alerts

```kusto
// Find security alerts involving this IP
let ip = "{ip_address}";
SecurityAlert
| where TimeGenerated > ago(30d)
| where ExtendedProperties has ip or Entities has ip
| project TimeGenerated, AlertName, AlertSeverity, Entities, ExtendedProperties
```

### 3. Check authentication attempts from this IP

```kusto
// Check for authentication attempts
let ip = "{ip_address}";
SigninLogs
| where TimeGenerated > ago(30d)
| where IPAddress == ip
| summarize AuthAttempts=count(), SuccessfulAuths=countif(ResultType == 0), FailedAuths=countif(ResultType != 0) by UserPrincipalName, AppDisplayName
| sort by AuthAttempts desc
```

### 4. Check for this IP in firewall logs

```kusto
// Check Common Security Log (firewall) for this IP
let ip = "{ip_address}";
CommonSecurityLog
| where TimeGenerated > ago(7d)
| where SourceIP == ip or DestinationIP == ip
| summarize ConnectionCount=count() by SourceIP, DestinationIP, DestinationPort, DeviceAction
| sort by ConnectionCount desc
```

Let me know if you need any more specific queries or if you want to dive deeper into any of these areas.
"""
            ),
            base.UserMessage(
                "This is very helpful. Should I also check if this IP is known to be malicious?"
            ),
            base.AssistantMessage(
                f"""
Absolutely! Here's how you can check if the IP address {ip_address} is known to be malicious:

### Check against threat intelligence feeds

```kusto
// Check this IP against threat intelligence
let ip = "{ip_address}";
ThreatIntelligenceIndicator
| where TimeGenerated > ago(30d)
| where NetworkIP == ip
| project TimeGenerated, Description, ThreatType, ConfidenceScore, Provider
```

### Check against Microsoft Defender threat analytics

```kusto
// Check Microsoft Defender for Endpoint evaluations
let ip = "{ip_address}";
DeviceNetworkEvents
| where TimeGenerated > ago(7d)
| where RemoteIP == ip
| join kind=inner (
    DeviceThreatEvents
    | where TimeGenerated > ago(7d)
) on DeviceId, Timestamp
| project TimeGenerated, DeviceName, RemoteIP, RemoteUrl, ThreatName, ThreatFamilyName, ThreatLevel
```

### Check for IP geolocation and classification

```kusto
// Get enriched information about the IP
let ip = "{ip_address}";
// Assuming you've enabled IP enrichment features, otherwise use logic to enrich manually
DeviceNetworkEvents
| where TimeGenerated > ago(7d)
| where RemoteIP == ip
| extend GeoIP = geo_info_from_ip_address(RemoteIP) // If geo_info function is available
| project TimeGenerated, DeviceName, RemoteIP, Country = tostring(GeoIP.country), City = tostring(GeoIP.city), Org = tostring(GeoIP.organization)
| limit 10
```

If you're using an IP reputation watchlist, you can also check against that:

```kusto
// Check against IP watchlist (if you maintain one)
let ip = "{ip_address}";
_GetWatchlist('IPReputation')
| where SearchKey == ip
| project IP = SearchKey, Reputation, ThreatType, Source, LastUpdated
```

These queries will help you determine if this IP is known to be malicious based on your threat intelligence data.
"""
            ),
        ]

    @mcp.prompt("sentinel_incident_respond", "Incident response workflow")
    def incident_response_workflow(incident_id: int) -> list[base.Message]:
        """
        Guide through a structured incident response process for a specific security incident.

        Args:
            incident_id: The incident ID number to investigate
        """
        return [
            base.UserMessage(
                f"I need to investigate and respond to security incident #{incident_id}. Can you guide me through the process?"
            ),
            base.AssistantMessage(
                f"""
I'll guide you through a structured incident response process for incident #{incident_id}. Let's follow these steps:

## 1. Assess the Incident

First, let's gather the basic details of this incident:

```kusto
SecurityIncident
| where IncidentNumber == {incident_id}
| project 
    IncidentNumber,
    Title,
    Description,
    Severity,
    Status,
    Classification,
    FirstActivityTime,
    LastActivityTime,
    CreatedTime = TimeGenerated,
    LastModifiedTime,
    Owner = OwnerName
```

## 2. Review Associated Alerts

Next, let's look at the alerts associated with this incident:

```kusto
SecurityIncident
| where IncidentNumber == {incident_id}
| join (
    SecurityAlert
    | where TimeGenerated > ago(30d)
) on $left.IncidentName == $right.SystemAlertId
| project 
    AlertName,
    AlertSeverity,
    AlertDescription = Description,
    TimeGenerated,
    Entities
```

Would you like me to help you run these initial queries?
"""
            ),
            base.UserMessage(
                "Yes, that would be helpful. What should I do after I've gathered that information?"
            ),
            base.AssistantMessage(
                f"""
After gathering the initial information about incident #{incident_id}, follow these next steps:

## 3. Investigate Impacted Entities

Extract and investigate entities (users, hosts, IPs) from the incident:

```kusto
SecurityIncident
| where IncidentNumber == {incident_id}
| join (
    SecurityAlert
    | where TimeGenerated > ago(30d)
) on $left.IncidentName == $right.SystemAlertId
| extend Entities = parse_json(Entities)
| mv-expand Entity = Entities
| extend EntityType = tostring(Entity.Type), EntityName = tostring(Entity.Name)
| summarize AlertCount = count() by EntityType, EntityName
| sort by AlertCount desc
```

For each impacted entity, perform targeted investigation:

- For users: Check authentication logs, unusual activities
- For hosts: Check process executions, network connections
- For IPs: Check connections, reputation, geographic location

## 4. Establish Timeline

Create a chronological timeline of events related to the incident:

```kusto
let incident = SecurityIncident
| where IncidentNumber == {incident_id}
| project IncidentNumber, Title, IncidentName;
let alerts = incident
| join (
    SecurityAlert
    | where TimeGenerated > ago(30d)
) on $left.IncidentName == $right.SystemAlertId
| project TimeGenerated, ItemType="Alert", Title=AlertName, Description;
let entities = alerts
| extend Entities = parse_json(Entities)
| mv-expand Entity = Entities
| extend EntityType = tostring(Entity.Type), EntityName = tostring(Entity.Name)
| distinct EntityType, EntityName;
// You would add more event types here specific to the entities
union alerts
| project TimeGenerated, ItemType, Title, Description
| sort by TimeGenerated asc
```

## 5. Determine Scope & Impact

Assess the scope and potential impact:

- How many systems/users are affected?
- What is the criticality of affected systems?
- Is sensitive data potentially exposed?
- Is the threat contained or active?

## 6. Containment & Remediation

Develop and implement containment and remediation steps:

- Block malicious IPs/domains at the firewall
- Isolate compromised hosts
- Reset compromised credentials
- Remove malware/unauthorized access
- Patch vulnerabilities

## 7. Documentation & Reporting

Document your findings and actions:

- Update the incident with your findings
- Document remediation steps taken
- Record lessons learned
- Prepare reports for stakeholders

## 8. Close the Incident

When appropriate, close the incident with proper classification:

```kusto
// This shows the query to check the current status
// Actual update would be done through the Sentinel UI or APIs
SecurityIncident
| where IncidentNumber == {incident_id}
| project IncidentNumber, Status, Classification, ClassificationComment
```

Would you like me to provide more specific guidance for any of these steps?
"""
            ),
            base.UserMessage(
                "This is comprehensive. Can you also show me how to check for similar incidents that might be related?"
            ),
            base.AssistantMessage(
                f"""
Absolutely! Here's how you can check for similar or related incidents to incident #{incident_id}:

## Finding Related Incidents

### 1. Find incidents with similar entities

```kusto
// First, extract entities from our incident
let incidentEntities = SecurityIncident
| where IncidentNumber == {incident_id}
| join (
    SecurityAlert
    | where TimeGenerated > ago(30d)
) on $left.IncidentName == $right.SystemAlertId
| extend Entities = parse_json(Entities)
| mv-expand Entity = Entities
| extend EntityType = tostring(Entity.Type), EntityName = tostring(Entity.Name)
| distinct EntityType, EntityName;
// Then find other incidents with the same entities
SecurityIncident
| where IncidentNumber != {incident_id}
| where TimeGenerated > ago(30d)
| join (
    SecurityAlert
    | join kind=inner (
        incidentEntities
    ) on $left.Entities contains $right.EntityName
) on $left.IncidentName == $right.SystemAlertId
| summarize AlertCount=count(), Entities=make_set(EntityName) by IncidentNumber, Title, Severity, Status
| sort by IncidentNumber desc
```

### 2. Find incidents with similar title or description

```kusto
// Get our incident's title
let incidentTitle = SecurityIncident
| where IncidentNumber == {incident_id}
| project Title;
// Find incidents with similar titles
SecurityIncident
| where IncidentNumber != {incident_id}
| where TimeGenerated > ago(30d)
| where Title has_any (incidentTitle) or Title has_any (split(toscalar(incidentTitle), " "))
| project IncidentNumber, Title, Severity, Status, TimeGenerated
| sort by TimeGenerated desc
```

### 3. Find incidents across the same timeframe

```kusto
// Get our incident's timeframe
let incidentTimeframe = SecurityIncident
| where IncidentNumber == {incident_id}
| project StartTime = FirstActivityTime, EndTime = LastActivityTime;
// Find incidents in a similar timeframe
let timeRange = toscalar(incidentTimeframe | extend Duration = EndTime - StartTime | project Duration);
SecurityIncident
| where IncidentNumber != {incident_id}
| where TimeGenerated > ago(30d)
| where FirstActivityTime between (toscalar(incidentTimeframe | project StartTime) - timeRange .. toscalar(incidentTimeframe | project EndTime) + timeRange)
| project IncidentNumber, Title, Severity, Status, FirstActivityTime, LastActivityTime
| sort by FirstActivityTime asc
```

### 4. Find incidents affecting the same systems

```kusto
// Get systems affected in our incident
let affectedSystems = SecurityIncident
| where IncidentNumber == {incident_id}
| join (
    SecurityAlert
    | where TimeGenerated > ago(30d)
) on $left.IncidentName == $right.SystemAlertId
| extend Entities = parse_json(Entities)
| mv-expand Entity = Entities
| where Entity.Type == "host" or Entity.Type == "hostName"
| extend HostName = tostring(Entity.Name)
| distinct HostName;
// Find other incidents affecting these systems
SecurityIncident
| where IncidentNumber != {incident_id}
| where TimeGenerated > ago(30d)
| join (
    SecurityAlert
    | where TimeGenerated > ago(30d)
    | extend Entities = parse_json(Entities)
    | mv-expand Entity = Entities
    | where Entity.Type == "host" or Entity.Type == "hostName" 
    | extend HostName = tostring(Entity.Name)
    | where HostName in (affectedSystems)
) on $left.IncidentName == $right.SystemAlertId
| summarize AlertCount=count() by IncidentNumber, Title, Severity, Status, TimeGenerated
| sort by TimeGenerated desc
```

### 5. Check for incident clusters using tactics or techniques

```kusto
// Get techniques used in our incident
let techniques = SecurityIncident
| where IncidentNumber == {incident_id}
| join (
    SecurityAlert
    | where TimeGenerated > ago(30d)
) on $left.IncidentName == $right.SystemAlertId
| extend Techniques = todynamic(AdditionalData).techniques
| mv-expand Technique = Techniques
| distinct tostring(Technique);
// Find incidents with similar techniques
SecurityIncident
| where IncidentNumber != {incident_id}
| where TimeGenerated > ago(30d)
| join (
    SecurityAlert
    | where TimeGenerated > ago(30d)
    | extend Techniques = todynamic(AdditionalData).techniques
    | mv-expand Technique = Techniques
    | where tostring(Technique) in (techniques)
) on $left.IncidentName == $right.SystemAlertId
| summarize AlertCount=count(), Techniques=make_set(tostring(Technique)) by IncidentNumber, Title, Severity, Status, TimeGenerated
| sort by TimeGenerated desc
```

These queries will help you identify incidents that might be related to incident #{incident_id} through common entities, systems, timing, or attack patterns. This can help you identify larger campaigns or persistent threats in your environment.
"""
            ),
        ]
