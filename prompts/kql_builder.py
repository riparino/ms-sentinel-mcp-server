"""
FILE: prompts/kql_builder.py
DESCRIPTION:
    Provides KQL query building prompts for the MCP server.
"""

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base


def register_prompts(mcp: FastMCP):
    """Register KQL query building prompts."""

    @mcp.prompt("sentinel_analytics_create_detection", "Create a detection query")
    def build_detection_query(
        threat_type: str, data_source: str = "SecurityEvent", time_window: str = "1d"
    ) -> list[base.Message]:
        """
        Create a KQL detection query for a specific threat type.

        Args:
            threat_type: Type of threat to detect (e.g., "brute force", "lateral movement")
            data_source: Primary data source table (default: SecurityEvent)
            time_window: Time window for detection (default: 1d)
        """
        return [
            base.UserMessage(
                f"I need to create a KQL detection query for {threat_type} attacks using {data_source} data over a {time_window} time window."
            ),
            base.AssistantMessage(
                "I'll help you build an effective detection query. First, let me show you some relevant KQL examples:"
            ),
            base.AssistantMessage(
                "Please reference the KQL examples at sentinel://examples/hunting"
            ),
            base.UserMessage(
                "These examples are helpful. Can you create a specific query for my use case?"
            ),
            base.AssistantMessage(
                f"""
Here's a custom detection query for {threat_type} using {data_source}:

```kusto
{data_source}
| where TimeGenerated > ago({time_window})
// Add filters specific to {threat_type} attacks
// E.g., for brute force:
// | where EventID == 4625
// | summarize FailureCount = count() by TargetAccount, IpAddress, bin(TimeGenerated, 5m)
// | where FailureCount > 10
```

This query looks for key indicators of {threat_type} by:
1. Filtering to the appropriate time window
2. Looking for specific events related to this threat type
3. Applying appropriate thresholds and aggregations

Would you like me to refine this query further for your environment?
"""
            ),
        ]

    @mcp.prompt("sentinel_hunting_create_query", "Create an advanced KQL query")
    def build_advanced_query(
        objective: str,
        tables: str,
        conditions: str = "",
    ) -> list[base.Message]:
        """
        Create an advanced KQL query based on specific objectives and conditions.

        Args:
            objective: What you're trying to accomplish with the query
            tables: Primary data tables to query (comma-separated if multiple)
            conditions: Optional specific conditions or filters
        """
        return [
            base.UserMessage(
                f"I need to create an advanced KQL query to {objective}. I want to use the {tables} table(s) {f'with these conditions: {conditions}' if conditions else ''}."
            ),
            base.AssistantMessage(
                "I'll help you build an effective KQL query for your objective. Let me first share some KQL basics that will be helpful:"
            ),
            base.AssistantMessage(
                "Please reference the KQL basics at sentinel://reference/kql/basics"
            ),
            base.AssistantMessage("And here are the key operators we might use:"),
            base.AssistantMessage(
                "Please reference the KQL operators at sentinel://reference/kql/operators"
            ),
            base.UserMessage(
                "Thanks for that reference. Can you now build a query for my specific use case?"
            ),
            base.AssistantMessage(
                f"""
Based on your objective to {objective}, here's a tailored KQL query using {tables}:

```kusto
{tables.split(',')[0].strip()}
| where TimeGenerated > ago(24h)
{f'| {conditions}' if conditions else '// Add your specific conditions here'}
// Additional processing for your objective
```

This query structure allows you to:
1. Start with the correct data sources
2. Apply appropriate time filters
3. Add your specific conditions
4. Process the data to meet your objectives

Would you like me to make any specific adjustments to this query?
"""
            ),
        ]
