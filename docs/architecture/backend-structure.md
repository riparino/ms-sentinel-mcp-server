# Backend Structure
## Microsoft Sentinel MCP Server

### 1. Data Models

#### Server Context Model

```python
@dataclass
class AzureServicesContext:
    """Container for Azure service clients and credentials"""
    
    credential: Optional[DefaultAzureCredential]  # Azure authentication credentials
    logs_client: Optional[LogsQueryClient]        # Client for querying logs
    metrics_client: Optional[MetricsQueryClient]  # Client for querying metrics
    security_insights_client: Optional[SecurityInsights]  # Client for security insights
    loganalytics_client: Optional[LogAnalyticsManagementClient]  # Client for workspace management
    workspace_id: str                             # Azure Log Analytics workspace ID
    subscription_id: str                          # Azure subscription ID
    resource_group: str                           # Azure resource group name
    config: Dict[str, Any]                        # Additional configuration values
```

#### Query Models

```python
@dataclass
class QueryRequest:
    """Model for KQL query requests"""
    
    query: str                      # The KQL query text
    timespan: Union[str, timedelta] # Time period for query (e.g., "1d", "PT1H")
    workspace_id: str               # Target workspace ID
    include_statistics: bool = False # Whether to include query statistics
    include_visualization: bool = False # Whether to include visualization data
    server_timeout: Optional[int] = None # Server-side timeout in seconds
```

```python
@dataclass
class QueryResponse:
    """Model for KQL query results"""
    
    tables: List[Dict[str, Any]]    # Result tables with columns and rows
    statistics: Optional[Dict[str, Any]] = None # Query performance statistics
    visualization: Optional[Dict[str, Any]] = None # Visualization data if requested
    error: Optional[str] = None     # Error message if query failed
    partial: bool = False           # Whether results are partial
```

#### Incident Models

```python
@dataclass
class SecurityIncidentListing:
    """Model for security incident list results"""
    
    incidents: List[Dict[str, Any]] # List of incidents with metadata
    total_count: int                # Total number of incidents (for pagination)
    skip_token: Optional[str] = None # Token for retrieving next page
```

#### Task Management Models

```python
@dataclass
class TaskInfo:
    """Information about a running task"""
    
    id: str                     # Unique identifier for the task
    name: str                   # Human-readable name of the task
    start_time: datetime        # When the task was started
    is_complete: bool = False   # Whether the task has completed
    result: Any = None          # The result of the task (if complete)
    error: Optional[str] = None # Error message if task failed
```

### 2. API Contracts

#### Resources API

- **List Resources**
  - URL: (MCP protocol - resources/list)
  - Method: MCP request
  - Parameters: None
  - Response: List of available resources with URIs, names, and descriptions
  - Authentication: None (MCP protocol handles authentication)

- **Read Resource**
  - URL: (MCP protocol - resources/read)
  - Method: MCP request
  - Parameters: 
    - uri: String (resource URI to read)
  - Response: Resource content with mime type
  - Authentication: None (MCP protocol handles authentication)
  - Error responses:
    - Resource not found
    - Invalid URI format
    - Access denied

#### Tools API

- **List Tools**
  - URL: (MCP protocol - tools/list)
  - Method: MCP request
  - Parameters: None
  - Response: List of available tools with names, descriptions, and input schemas
  - Authentication: None (MCP protocol handles authentication)

- **Call Tool**
  - URL: (MCP protocol - tools/call)
  - Method: MCP request
  - Parameters:
    - name: String (tool name to call)
    - arguments: Object (tool-specific parameters)
  - Response: Tool execution results or error
  - Authentication: None (MCP protocol handles authentication)
  - Error responses:
    - Tool not found
    - Invalid parameters
    - Execution error
    - Azure authentication error
    - Access denied

#### Prompts API

- **List Prompts**
  - URL: (MCP protocol - prompts/list)
  - Method: MCP request
  - Parameters: None
  - Response: List of available prompts with names, descriptions, and argument schemas
  - Authentication: None (MCP protocol handles authentication)

- **Get Prompt**
  - URL: (MCP protocol - prompts/get)
  - Method: MCP request
  - Parameters:
    - name: String (prompt name to get)
    - arguments: Object (prompt-specific parameters)
  - Response: Prompt messages
  - Authentication: None (MCP protocol handles authentication)
  - Error responses:
    - Prompt not found
    - Invalid parameters

### 3. Service Architecture

#### Core Server Component
- **FastMCP Server**: Main server instance that handles MCP protocol communication
  - Manages the server lifecycle and component registration
  - Dispatches MCP requests to the appropriate handlers
  - Provides the context for all operations

#### Resource Components
- **KQL Reference Resources**: Provides documentation on KQL syntax and operators
- **Examples Resources**: Provides example KQL queries for common scenarios
- **Tables Resources**: Provides information about Sentinel data tables

#### Tool Components
- **Query Tools**: Executes and validates KQL queries
  - KQL validation using Kusto.Language library
  - Query execution through Azure Monitor API
- **Incident Tools**: Manages security incidents
  - Lists incidents with filtering and pagination
  - Gets detailed incident information
- **Workspace Tools**: Manages workspace information
  - Gets workspace details and configuration
- **Data Connector Tools**: Manages data connectors
  - Lists available data connectors
  - Gets connector details

#### Prompt Components
- **Investigation Prompts**: Templates for security investigations
- **Query Building Prompts**: Templates for building KQL queries
- **Workspace Visualization Prompts**: Templates for visualizing workspace information

#### Utility Components
- **Task Manager**: Manages asynchronous tasks
  - Tracks running tasks
  - Handles timeouts and cancellation
  - Provides progress reporting
- **KQL Validator**: Validates KQL query syntax
  - Uses Kusto.Language library
  - Provides detailed error messages
- **Connection Tester**: Tests Azure connectivity
  - Validates credentials
  - Checks workspace access

### 4. Storage Strategy

The server is primarily stateless and doesn't maintain persistent storage. Data is retrieved from Azure services as needed.

- **In-Memory Storage**:
  - Running tasks are tracked in memory
  - Cached validation results (short-term)
  - Connection state during server lifetime

- **Azure Storage**:
  - All permanent data is stored in Microsoft Sentinel/Log Analytics
  - Query results are retrieved directly from Azure
  - Incidents and other security data remain in Azure

### 5. Access Control Policies

- **Azure Authentication**:
  - All Azure interactions use DefaultAzureCredential
  - Service principals require Reader role for Log Analytics workspace
  - Incident management requires Security Reader role for Sentinel
  - Writing to incidents requires Security Responder role

- **Local Access Control**:
  - Server assumes the local user should have full access to functionality
  - No additional authentication layer in the server itself
  - Relies on MCP client for user authentication

### 6. Integration Patterns

- **Azure Integration**:
  - Uses official Azure SDKs for all Azure service communication
  - Follows Azure authentication best practices
  - Handles Azure API errors and retries

- **MCP Protocol Integration**:
  - Implements MCP protocol specification for client-server communication
  - Supports multiple transports (stdio, SSE)
  - Provides standardized resource, tool, and prompt interfaces

- **Python.NET Integration**:
  - Uses Python.NET bridge to access .NET libraries
  - Loads Kusto.Language DLL for KQL validation
  - Fallback mechanisms when .NET components are unavailable

### 7. Caching Strategy

- **KQL Validation Cache**:
  - Caches validation results for identical queries briefly
  - Invalidates cache when server detects schema changes

- **Schema Information Cache**:
  - Caches table schemas during server lifetime
  - Refreshes periodically to catch schema changes

- **No Result Caching**:
  - Query results are not cached to ensure freshness
  - Each query executes against Azure for current data

### 8. Scaling Considerations

- **Concurrent Operations**:
  - Uses Python async to handle multiple operations concurrently
  - Task manager limits maximum concurrent Azure operations
  - Implements backoff for rate-limited Azure APIs

- **Resource Consumption**:
  - Monitors memory usage for large query results
  - Implements timeouts for long-running operations
  - Cancels abandoned tasks to free resources

### 9. Transaction Management

- **Azure Transaction Guarantees**:
  - Relies on Azure services for transactional guarantees
  - Query operations are inherently read-only
  - Incident updates use Azure API's transaction handling

- **Error Handling**:
  - Catches exceptions during operations
  - Provides clear error messages in responses
  - Avoids partial updates where possible
  - Implements cleanup for failed operations

- **State Management**:
  - Maintains minimal mutable state
  - Uses immutable data structures where possible
  - Isolates side effects to specific components
