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
