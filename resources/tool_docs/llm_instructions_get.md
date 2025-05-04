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
  "content": "# LLM Usage Instructions\n\n- Use fictional placeholders for all workspace details...\n..."
}
```

## Error Handling
- Returns `error` if the instructions file cannot be read.

## MCP Compliance
- Inherits from `MCPToolBase`.
- Implements `async def run(self, ctx, **kwargs)`.
- Registered in `register_tools()`.
- Uses robust error handling.
