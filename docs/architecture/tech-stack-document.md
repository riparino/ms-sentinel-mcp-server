# Tech Stack Document
## Microsoft Sentinel MCP Server

### 1. Programming Languages
- **Primary Language**: Python 3.13+
  - Chosen for its strong async support, type hinting, and extensive Azure SDK availability
  - All server code is written in Python with type annotations
- **Supporting Languages**:
  - C# (.NET): Used indirectly via the Kusto.Language library for KQL validation

### 2. Frontend Technologies
*Not applicable* - The Microsoft Sentinel MCP Server is a backend service that communicates using the MCP protocol and doesn't include a frontend component. AI assistants act as the interface to users.

### 3. Backend Technologies

#### Server Framework
- **MCP Python SDK v1.6.0+**
  - Core framework that implements the Model Context Protocol
  - Handles message routing, serialization, and communication patterns
  - Provides the `FastMCP` high-level API for server development

#### API Framework
- **No separate API framework**
  - All API endpoints are defined through MCP protocol handlers
  - Communication uses standard MCP message formats via stdin/stdout or SSE

#### Runtime Environment
- **Python Async/Await**
  - Uses Python's asyncio for handling concurrent operations
  - Async context managers for resource management
  - Task tracking for proper cleanup and timeout handling

#### HTTP Client
- **Azure SDK HTTP Pipeline**
  - Uses Azure SDK's built-in HTTP pipeline for Azure service communication
  - Handles retries, authentication, and error processing

### 4. Database Technologies
- **No local database**
  - The server acts as a bridge to Microsoft Sentinel/Log Analytics
  - Azure Monitor Logs (Kusto) serves as the query backend
  - No local state persistence beyond the current session

#### Query Languages
- **Kusto Query Language (KQL)**
  - Used for querying Microsoft Sentinel data
  - Server validates and executes KQL queries against Azure Monitor

### 5. Authentication/Authorization
- **Azure Identity Library**
  - Uses DefaultAzureCredential for flexible authentication methods
  - Supports environment variables, managed identity, and interactive login
  - Credential objects are created during server initialization

- **Azure RBAC (Role-Based Access Control)**
  - Relies on Azure's built-in RBAC system for authorization
  - The service principal or user identity must have appropriate permissions in Azure

### 6. Infrastructure
- **Local Process**
  - Runs as a standalone Python process on the local system
  - Can be installed in Claude Desktop for direct integration
  - No containerization in the base implementation

- **Hosting**
  - Primarily designed for local execution
  - Can be adapted for server deployment with appropriate transport changes

### 7. Third-Party Services
- **Azure Monitor Query API** (v1.4.1+)
  - Used for executing KQL queries against Log Analytics workspaces
  - Provides access to logs and metrics data

- **Azure Security Insights API** (v1.0.0+)
  - Used for accessing Microsoft Sentinel resources
  - Provides incident management, watchlists, and security settings

- **Azure Log Analytics Management API** (v12.0.0+)
  - Used for workspace management and configuration
  - Provides workspace metadata and settings

- **Python.NET** (v3.0.1+)
  - Bridge for using .NET libraries from Python
  - Used specifically for the Kusto Language library

- **Kusto.Language .NET Library**
  - Used for KQL syntax validation
  - Downloaded and loaded during server initialization

### 8. Development Tools
- **uv**
  - Modern Python package installer and virtual environment manager
  - Used for dependency management

- **Black**
  - Python code formatter for consistent style
  - Set to line length of 88 characters

- **isort**
  - Import sorter for organizing imports
  - Configured to be compatible with Black

- **mypy**
  - Static type checker for Python
  - Set to basic type checking mode

- **flake8**
  - Linter for style guide enforcement
  - Used alongside Black and isort

### 9. Rationale for Choices

#### Python as Primary Language
Python was chosen for its strong support in the Azure ecosystem, excellent async capabilities, and widespread use in security tooling. Python's type hints allow for better IDE support and code verification while maintaining readability. The language's extensive library ecosystem provides robust tools for handling complex operations like authentication and HTTP communication.

#### MCP Python SDK
The MCP Python SDK was the natural choice as it's the official implementation of the Model Context Protocol. It provides a well-designed API that abstracts away the complexities of the protocol while maintaining compliance with the specification. The FastMCP high-level API significantly reduces boilerplate code compared to using the low-level protocol interfaces.

#### Azure SDK Components
Official Azure SDK components were selected to ensure compatibility and proper handling of authentication, token management, and API versioning. These libraries are well-maintained, follow consistent patterns, and receive regular updates for security and functionality.

#### Python.NET and Kusto.Language
Validating KQL syntax requires complex parsing logic that would be difficult to implement from scratch. By using the official Kusto.Language library through Python.NET, the server leverages the same validation engine used by Microsoft tools, ensuring consistent and accurate results. This approach trades some deployment complexity for significantly improved validation capabilities.

#### Local Process Execution
The server is designed to run locally to minimize deployment complexity and security concerns. This design choice keeps sensitive credentials on the user's system and simplifies integration with Claude Desktop. The server can be adapted for remote deployment if needed, but the default configuration prioritizes simplicity and security.

### 10. Compatibility Notes

#### Component Interoperability
- The Azure SDK components are designed to work together seamlessly
- Python.NET may require specific .NET runtime versions depending on the environment
- MCP SDK is compatible with any reasonable Python async implementation

#### Version Requirements
- Azure Identity ≥ 1.21.0
- Azure Monitor Query ≥ 1.4.1
- Azure Security Insights ≥ 1.0.0
- Azure Log Analytics Management ≥ 12.0.0
- Python.NET ≥ 3.0.1
- MCP ≥ 1.6.0

#### Operating System Compatibility
- Primary: Windows 10/11, due to Python.NET and .NET requirements
- Limited: macOS and Linux support may require additional setup for the .NET runtime
- The core functionality (except KQL validation) works on all platforms that support Python 3.13+

#### MCP Protocol Compatibility
- Implements MCP 1.0 specification
- Compatible with Claude Desktop and other MCP-compliant clients
- Supports both stdin/stdout and SSE transports
