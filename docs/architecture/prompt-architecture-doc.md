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
