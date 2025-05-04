"""
FILE: resources/kql_examples.py
DESCRIPTION:
    Provides KQL examples resource for the MCP server.
"""

from mcp.server.fastmcp import FastMCP


def register_resources(mcp: FastMCP):
    """Register KQL examples resources with the MCP server."""

    @mcp.resource("sentinel://reference/kql/examples")
    def get_kql_examples() -> str:
        """Provides practical KQL query examples for Azure Monitor"""
        return """# Practical KQL Query Examples

## Security Examples

### Successful Logons
```
SecurityEvent 
| where TimeGenerated > ago(1h)
| where EventID == 4624
| where AccountType =~ "user"
| count
```

### Failed Logons
```
SecurityEvent
| where TimeGenerated > ago(1h)
| where EventID == 4625
| where AccountType =~ "user"
| count
```

### Cloud Shell Activity
```
AzureActivity
| where ResourceGroup startswith "CLOUD-SHELL"
| where ResourceProviderValue == "MICROSOFT.STORAGE"
| where ActivityStatusValue == "Start"
| summarize count() by TimeGenerated, ResourceGroup, Caller, CallerIpAddress, ActivityStatusValue
| extend AccountCustomEntity = Caller
| extend IPCustomEntity = CallerIpAddress
```

## Performance Examples

### Free Disk Space
```
Perf
| where CounterName == "Free Megabytes"
| where InstanceName matches regex "^[A-Z]:$"
| extend FreeGB = CounterValue / 1024
| project Computer, CounterName, FreeGB
```

### Find all computers reporting performance data
```
Perf
| distinct Computer
```

## Advanced Queries

### Login and Logout Correlation
```
let login = SecurityEvent
| where TimeGenerated > ago(1h)
| where EventID == '4624'
| project Account, TargetLogonId, loginTime = TimeGenerated;
let logout = SecurityEvent
| where TimeGenerated > ago(1h)
| where EventID == '4634'
| project Account, TargetLogonId, logoutTime = TimeGenerated;
login
| join kind=leftouter logout on TargetLogonId
| project Account, loginTime, logoutTime
```

### Using Watchlists
```
let watchlist = (_GetWatchlist('FeodoTracker') | project DstIP);
Heartbeat
| where ComputerIP in (watchlist)
```

### Visualising data with charts
```
SecurityEvent
| where TimeGenerated > ago(7d)
| summarize count() by bin(TimeGenerated, 1d)
| render barchart
```

## For more comprehensive KQL learning, refer to Rod Trent's "Must Learn KQL" series.
"""

    @mcp.resource("sentinel://reference/kql/examples/security")
    def get_security_examples() -> str:
        """Provides security-focused KQL query examples"""
        return """# Security-Focused KQL Query Examples

## Account Activity Monitoring

### Successful Logons by Account
```
SecurityEvent
| where EventID == 4624
| where TimeGenerated > ago(24h)
| summarize count() by Account, Computer
| sort by count_ desc
```

### Failed Logon Attempts (Possible Brute Force)
```
SecurityEvent
| where EventID == 4625
| where TimeGenerated > ago(24h)
| summarize count() by Account, Computer, IpAddress
| sort by count_ desc
```

### New Process Creation
```
SecurityEvent
| where EventID == 4688
| where TimeGenerated > ago(24h)
| project TimeGenerated, Computer, Account, NewProcessName, CommandLine
```

## Azure Activity Monitoring

### Admin Operations
```
AzureActivity
| where OperationName contains "Microsoft.Authorization/roleAssignments"
| where TimeGenerated > ago(7d)
| project TimeGenerated, Caller, CallerIpAddress, OperationName, ResourceGroup
```

### Security Group Changes
```
AzureActivity
| where ResourceProvider == "Microsoft.Network" and ResourceType == "networkSecurityGroups"
| where TimeGenerated > ago(7d)
| project TimeGenerated, Caller, CallerIpAddress, OperationName, ResourceGroup
```

## Microsoft Sentinel Specific

### Incidents Created
```
SecurityIncident
| where TimeGenerated > ago(7d)
| summarize count() by Title, Severity
| sort by count_ desc
```

### Alert Activity
```
SecurityAlert
| where TimeGenerated > ago(7d)
| summarize count() by AlertName, AlertSeverity
| sort by count_ desc
```
"""
