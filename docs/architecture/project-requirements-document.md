# Project Requirements Document (PRD)
## Microsoft Sentinel MCP Server

### 1. Project Overview
The Microsoft Sentinel MCP Server is a specialized implementation of the Model Context Protocol (MCP) that provides AI assistants (like Claude) access to Microsoft Sentinel security data and capabilities. The server acts as a bridge between large language models and Azure security infrastructure, allowing AI assistants to query security data, analyze incidents, retrieve threat information, and assist security analysts in their day-to-day operations. This server will enable security teams to leverage AI capabilities within their existing security operations workflows while maintaining security and control over sensitive data.

The primary goal is to create a robust, secure, and efficient MCP server that exposes Microsoft Sentinel's capabilities through standardized MCP resources, tools, and prompts, making complex security tasks more accessible through AI assistance. The server should handle authentication to Azure services, provide error handling for common failure scenarios, and offer a consistent way to access security information.

### 2. Target Users/Systems
- **Primary Users**: 
  - Security Operations Centre (SOC) analysts using AI assistants to accelerate investigations
  - Security engineers who need assistance with creating complex KQL (Kusto Query Language) queries
  - Incident responders who need quick access to incident details and context
  - Security administrators who need to understand their Sentinel workspace configuration

- **Secondary Users**:
  - Security managers seeking summarized security posture information
  - Developers building security tools that integrate with Sentinel
  - AI researchers exploring security analytics use cases

- **Systems**:
  - Microsoft Sentinel instances within Azure
  - Azure Monitor Log Analytics workspaces
  - Claude or other AI assistants that support the MCP protocol
  - Security orchestration platforms that might integrate with the server

### 3. Interaction Flow
Users interact with the server indirectly through an AI assistant. The assistant communicates with the MCP server to fetch data, execute queries, and format results. The AI then presents this information to the user in a natural, conversational manner. When users need security information, they ask the AI assistant questions or request specific analysis. The assistant determines which MCP resources or tools to invoke, sends requests to the MCP server, processes the responses, and presents insights back to the user.

For example, when a security analyst asks, "Show me recent failed login attempts," the AI assistant calls the appropriate query tool on the MCP server, which authenticates to Azure, executes the query against the Sentinel workspace, and returns the results. The AI then formats and explains these results conversationally to the user.

### 4. Technology Stack Overview
The Microsoft Sentinel MCP Server is built on Python 3.13+ using the MCP Python SDK for the protocol implementation. It leverages Azure SDK components for interacting with Microsoft Sentinel and Azure Monitor services. For KQL validation, it uses the Kusto Language library through Python.NET bindings. The server runs as a standalone process that can be connected to an AI assistant directly or through Claude Desktop.

Full details are provided in the Tech Stack Document.

### 5. Core Features/Capabilities

#### Resources
- **KQL Reference Resources**: Provides comprehensive documentation on KQL syntax, operators, and examples
- **Table Reference Resources**: Offers details about common Sentinel data tables and their schemas
- **Security Example Resources**: Includes example KQL queries for common security scenarios
- **Workspace Information Resources**: Delivers information about the Sentinel workspace configuration

#### Tools
- **KQL Query Validation**: Validates KQL syntax without executing queries
- **KQL Query Execution**: Runs KQL queries against the Sentinel workspace
- **Table Schema Explorer**: Retrieves table schemas and available tables
- **Security Incident Management**: Lists, retrieves, and updates security incidents
- **Data Connector Management**: Lists and provides information about data connectors
- **Workspace Information**: Gets detailed information about the Sentinel workspace

#### Prompts
- **Security Investigation Prompts**: Guides through investigating security scenarios
- **KQL Query Building Prompts**: Helps construct complex KQL queries
- **Incident Response Prompts**: Offers structured incident response workflows
- **Workspace Visualization Prompts**: Creates visualizations of workspace configuration

### 6. Scope Limitations
The following items are explicitly excluded from the initial version:

- **No Direct Data Modification**: The server will not allow direct modification of security data or configurations beyond updating incidents
- **No Custom Rule Creation**: The server will not create or modify analytics rules
- **No User Management**: The server will not handle Azure AD user management or permissions
- **Limited Visualizations**: The server will not generate complex visualizations or dashboards
- **No Alerting Functionality**: The server will not create or manage alert notifications
- **No Data Ingestion**: The server will not ingest data into Sentinel
- **No Multi-workspace Support**: The initial version will connect to a single workspace at a time

Future versions may address these limitations as the project evolves.

### 7. Success Criteria
- **Functionality**: Server successfully connects to Azure Sentinel and retrieves data
- **Performance**: Query execution time under 10 seconds for typical KQL queries
- **Reliability**: Server maintains stable connections with proper error handling
- **Security**: All communication with Azure services follows security best practices
- **Usability**: AI assistants can effectively use the server with minimal friction
- **Extensibility**: New tools and resources can be added without major refactoring
- **Validation**: KQL validation provides accurate and helpful feedback
- **Documentation**: Complete documentation of all server capabilities and usage

### 8. Dependencies
- **Azure Subscription**: Active Azure subscription with appropriate permissions
- **Microsoft Sentinel**: Configured Sentinel workspace with data
- **Service Principal**: Azure service principal with appropriate permissions
- **MCP Protocol Support**: AI assistant with MCP protocol support
- **Python Environment**: Python 3.13+ environment for running the server
- **Network Access**: Network connectivity to Azure endpoints
- **Microsoft.NET DLLs**: Kusto.Language DLL for KQL validation
- **Azure SDK Versions**: Compatible versions of Azure SDKs
