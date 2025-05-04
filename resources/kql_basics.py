"""
FILE: resources/kql_basics.py
DESCRIPTION:
    Provides KQL basics resource for the MCP server.
"""

from mcp.server.fastmcp import FastMCP


def register_resources(mcp: FastMCP):
    """Register KQL basics resources with the MCP server."""

    @mcp.resource("sentinel://reference/kql/basics")
    def get_kql_basics() -> str:
        """Provides basic information about KQL query structure and syntax"""
        return """# KQL (Kusto Query Language) Basics

## Query Structure
KQL queries typically follow this pattern:
```
Table | Operator1 | Operator2 | ...
```

## Common Operators

### Data Selection
- `where`: Filters rows based on specific conditions
  Example: `SecurityEvent | where EventID == 4624`

- `take`/`limit`: Returns a specified number of random rows
  Example: `SecurityEvent | take 10`

- `search`: Full-text search across columns or tables
  Example: `search "suspicious"`

### Data Transformation
- `project`: Selects and renames columns
  Example: `SecurityEvent | project Computer, EventID, Account`

- `extend`: Creates new calculated columns
  Example: `Perf | extend FreeGB = CounterValue / 1024`

- `summarize`: Aggregates data using functions like count(), sum(), avg()
  Example: `SecurityEvent | summarize count() by Computer`

- `distinct`: Returns unique values
  Example: `SecurityEvent | distinct Computer`

### Data Organisation
- `sort`/`order`: Sorts data by specified columns
  Example: `SecurityEvent | order by TimeGenerated desc`

- `top`: Returns the top N rows sorted by specified columns
  Example: `SecurityEvent | top 100 by TimeGenerated desc`

### Time Filters
- Time range using `ago()`:
  Example: `SecurityEvent | where TimeGenerated > ago(1h)`

- `bin()` for time intervals:
  Example: `SecurityEvent | summarize count() by bin(TimeGenerated, 1d)`

### Combining Data
- `join`: Combines rows from multiple tables
  Example: `SecurityEvent | join Heartbeat on Computer`

- `union`: Combines results from multiple tables
  Example: `SecurityEvent | union Heartbeat`

### Variables
- `let`: Defines reusable variables or subqueries
  Example: `let timeAgo = 7d; SecurityEvent | where TimeGenerated > ago(timeAgo)`

## Common KQL Patterns

### Count events by type
```
SecurityEvent
| where TimeGenerated > ago(1h)
| summarize count() by EventID
```

### Successful vs Failed Logons
```
SecurityEvent
| where TimeGenerated > ago(1h)
| where EventID in (4624, 4625)
| summarize SuccessfulLogons = countif(EventID == 4624), FailedLogons = countif(EventID == 4625) by Computer
```

### Most recent events
```
SecurityEvent
| summarize arg_max(TimeGenerated, *) by Account
```

### Visualising data
```
SecurityEvent
| where TimeGenerated > ago(7d)
| summarize count() by bin(TimeGenerated, 1d)
| render barchart
```
"""
