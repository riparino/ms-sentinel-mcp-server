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