# Security Guideline Document
## Microsoft Sentinel MCP Server

### 1. Core Security Principles

The Microsoft Sentinel MCP Server adheres to these core security principles:

- **Defense in Depth**: Multiple layers of security controls mitigate different types of attacks
- **Principle of Least Privilege**: Components operate with the minimum permissions needed
- **Secure by Default**: Security measures are enabled by default with secure configuration
- **Data Protection**: Sensitive information is protected at rest and in transit
- **Zero Trust**: No inherent trust in any component or service
- **Transparency**: Clear documentation of security behaviors and limitations
- **Shift Left Security**: Security considerations built into the design from the beginning

### 2. Authentication Security

#### Azure Authentication Mechanisms

- **DefaultAzureCredential**
  - Primary authentication method for Azure services
  - Tries multiple authentication methods in sequence:
    1. Environment variables (AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID)
    2. Managed identity (when running in Azure)
    3. Azure CLI credentials
    4. Interactive browser authentication
  - Credentials must be provided before server startup

- **Service Principal Authentication**
  - Recommended for production deployments
  - Requires Client ID, Client Secret, and Tenant ID
  - Service principal must have the following roles assigned:
    - `Log Analytics Reader` for the workspace
    - `Microsoft Sentinel Reader` for read operations
    - `Microsoft Sentinel Responder` for incident management

- **Credential Lifecycle Management**
  - Credentials are loaded once during server initialization
  - Token refresh is handled automatically by Azure Identity library
  - No credentials are persisted to disk by the server
  - Environment variables should be configured in .env file (not committed to version control)

#### Credential Storage

- **Environment Variables**
  - Preferred method for supplying credentials
  - Set via `.env` file or directly in the environment
  - Example format:
    ```
    AZURE_TENANT_ID=00000000-0000-0000-0000-000000000000
    AZURE_CLIENT_ID=00000000-0000-0000-0000-000000000000
    AZURE_CLIENT_SECRET=client-secret-value
    AZURE_SUBSCRIPTION_ID=00000000-0000-0000-0000-000000000000
    ```

- **Credential Handling**
  - Credentials are never logged
  - Secrets are never included in error messages
  - In-memory credential objects are properly disposed after use
  - No caching of raw credentials

#### Authentication Error Handling

- Detailed authentication error messages without exposing secrets
- Graceful degradation when authentication fails
- Clear guidance for resolving authentication issues
- Authentication errors logged with appropriate severity

### 3. Authorization Framework

#### Azure RBAC Integration

- **Role Requirements**
  - Minimal required roles for full functionality:
    - `Log Analytics Reader`
    - `Microsoft Sentinel Reader`
    - `Microsoft Sentinel Responder`
  - Read-only functionality requires only:
    - `Log Analytics Reader`
    - `Microsoft Sentinel Reader`

- **Permission Verification**
  - Server verifies permissions on startup
  - Missing permissions result in specific warnings
  - Features requiring missing permissions are disabled

#### Server-Side Authorization

- **No Additional Authorization Layer**
  - Server assumes the authenticated Azure identity should have full access
  - No additional user authentication is implemented in the server
  - The MCP client (Claude Desktop) handles user authentication

- **Feature Degradation**
  - Features automatically disable when permissions are insufficient
  - Clear error messages indicate permission requirements
  - Read-only operations remain available when write permissions are missing

### 4. Data Protection

#### Data at Rest

- **No Persistent Storage**
  - The server doesn't store any data persistently
  - All security data remains in Azure Sentinel
  - No caching of query results or incident data to disk
  - Temporary files (if created) are properly cleaned up

- **Environment Variable Protection**
  - Environment variables should be protected by OS-level access controls
  - .env files should never be committed to version control
  - .env.example provides a template without actual values

#### Data in Transit

- **Azure SDK Encryption**
  - All communication with Azure services uses HTTPS/TLS 1.2+
  - Azure SDK handles certificate validation and secure connections
  - Default secure connection settings used for all Azure operations

- **MCP Protocol Security**
  - Local communication via stdio or SSE is not encrypted
  - Server assumes the local environment is trusted
  - For remote operation, an external TLS layer should be added

#### Sensitive Data Handling

- **No Logging of Sensitive Data**
  - Query contents are logged without parameters
  - Error messages exclude sensitive details
  - Authentication details are never logged
  - Log levels control verbosity of information

- **Memory Protection**
  - Sensitive objects cleared from memory when no longer needed
  - No serialization of credential objects
  - Proper handling of exceptions to prevent memory leaks

### 5. Input Validation

#### KQL Query Validation

- **Syntax Validation**
  - All KQL queries validated before execution
  - Kusto.Language library used for accurate validation
  - Detailed error messages for invalid syntax
  - Defense against KQL injection via proper query parameterization

- **Query Size Limits**
  - Maximum query length: 1MB
  - Maximum execution time: 10 minutes
  - Maximum result size: 50MB
  - Limits enforced before query execution

#### Parameter Validation

- **Type Checking**
  - All parameters validated for correct types
  - Conversion errors handled gracefully
  - Strong typing used throughout the codebase

- **Value Validation**
  - Numeric ranges validated (e.g., timeout values, limits)
  - String patterns validated (e.g., UUIDs, resource IDs)
  - Enum values validated against allowed values
  - Default values provided for optional parameters

#### Resource URI Validation

- **URI Format**
  - Resource URIs validated against allowed patterns
  - Protocol-specific validation for different URI types
  - Path traversal prevention for file URIs
  - Sanitization of URI components

- **Safe Resource Loading**
  - Resource contents validated before returning
  - MIME type verification
  - Size limits enforced
  - Content sanity checks

### 6. Vulnerability Mitigation

#### Code Injection Prevention

- **KQL Injection Prevention**
  - All user-provided query components properly validated
  - Parameter values properly escaped when interpolated
  - No dynamic KQL generation without validation
  - Query isolation from control mechanisms

- **Command Injection Prevention**
  - No shell command execution in the codebase
  - Subprocess calls (if needed) use list arguments, not shell=True
  - Proper argument validation before execution
  - Limited subprocess capabilities

#### Denial of Service Protection

- **Query Limiting**
  - Timeout enforcement for all queries
  - Maximum concurrent operations limit
  - Task cancellation for abandoned operations
  - Rate limiting for repetitive operations

- **Resource Consumption Controls**
  - Memory usage monitoring
  - Large result pagination
  - Task priority system
  - Graceful degradation under load

#### Supply Chain Security

- **Dependency Review**
  - All dependencies reviewed for security issues
  - Specific versions pinned in requirements
  - Regular updates for security patches
  - Limited dependency tree depth

- **Secure Dependency Installation**
  - Integrity verification of packages
  - Dependency lockfiles used
  - Installation from trusted sources
  - Vulnerability scanning in CI/CD

### 7. Security Testing

#### Required Security Tests

- **Static Analysis**
  - Run Bandit for Python security analysis
  - mypy for type checking
  - Custom linting rules for security patterns
  - Run on every code change

- **Authentication Testing**
  - Verify credential handling
  - Test authentication failure scenarios
  - Check token refresh behavior
  - Validate permission checks

- **Input Validation Testing**
  - Test with malformed inputs
  - Verify syntax validation
  - Check boundary conditions
  - Ensure proper error messages

- **Dependency Analysis**
  - Regular dependency vulnerability scanning
  - Check for outdated packages
  - Verify license compliance
  - Test compatibility with security patches

### 8. Monitoring and Incident Response

#### Security Logging

- **Log Levels**
  - ERROR: Security-related failures
  - WARNING: Potential security concerns
  - INFO: Normal security operations
  - DEBUG: Detailed security diagnostics

- **Log Content**
  - Authentication attempts (success/failure)
  - Authorization decisions
  - Operation execution
  - Resource access
  - Error conditions

- **Log Protection**
  - Logs directed to stderr by default
  - Sensitive data filtered from logs
  - Structured logging format
  - Log rotation if file logging enabled

#### Alert Thresholds

- **Authentication Failures**
  - Alert on multiple failed authentication attempts
  - Track unusual authentication patterns
  - Monitor for credential misuse

- **Authorization Failures**
  - Alert on repeated permission denied errors
  - Track attempts to access unauthorized resources
  - Monitor for privilege escalation attempts

- **Operational Anomalies**
  - Alert on abnormal query patterns
  - Monitor resource consumption spikes
  - Track unusual error rates

#### Incident Response Procedures

- **Authentication Issues**
  1. Identify the source of authentication failures
  2. Verify credential validity and permissions
  3. Rotate credentials if compromise is suspected
  4. Review logs for unauthorized access attempts

- **Azure Service Disruptions**
  1. Verify Azure service status
  2. Check network connectivity
  3. Validate credential permissions
  4. Implement appropriate fallback behaviors

- **Security Vulnerabilities**
  1. Assess vulnerability impact
  2. Apply temporary mitigations
  3. Update affected dependencies
  4. Implement permanent fixes

### 9. Dependency Security

#### Secure Dependencies

- **Azure SDK Security**
  - Use latest secure versions of Azure SDK components
  - Follow Microsoft security advisories
  - Implement recommended security practices
  - Test compatibility before upgrading

- **Python Package Security**
  - Pin dependency versions for predictability
  - Use trusted package sources
  - Verify package integrity
  - Regularly update for security patches

- **Third-Party Library Security**
  - Review security practices of third-party libraries
  - Limit scope of third-party code
  - Isolate potentially risky dependencies
  - Have fallbacks for critical dependencies

#### Secure Updates

- **Update Verification**
  - Test updates in isolation before deployment
  - Verify security fixes are included
  - Check for breaking changes in security patches
  - Validate compatibility with existing code

- **Update Frequency**
  - Security patches applied immediately
  - Regular updates for all dependencies
  - Version migration planning
  - Update documentation

#### Vulnerability Management

- **Vulnerability Tracking**
  - Monitor security advisories for dependencies
  - Track CVEs affecting the codebase
  - Assess impact of vulnerabilities
  - Prioritize based on severity and exploitability

- **Remediation Processes**
  - Document vulnerability remediation procedures
  - Test patches before deployment
  - Provide workarounds when patches aren't available
  - Communicate security updates to users

### Implementation Specifics

#### Secure Authentication Implementation

```python
def initialize_azure_credentials():
    """Initialize Azure credentials securely."""
    try:
        # DefaultAzureCredential tries multiple authentication methods
        credential = DefaultAzureCredential(
            exclude_shared_token_cache_credential=True,  # More predictable authentication
            logging_enable=False  # Prevent logging sensitive details
        )
        
        # Test credential by requesting a token
        # This validates credentials before proceeding
        token = credential.get_token("https://management.azure.com/.default")
        if not token:
            raise ValueError("Could not acquire token with provided credentials")
        
        return credential
    except Exception as e:
        # Log without revealing secrets
        logger.error(f"Authentication error: {type(e).__name__}")
        # Re-raise with generic message
        raise ValueError("Failed to authenticate with Azure. Check credentials and permissions.") from e
```

#### Secure Input Validation Implementation

```python
def validate_kql_query(query: str, max_length: int = 1024 * 1024) -> Tuple[bool, List[str]]:
    """
    Validate KQL query syntax securely.
    
    Args:
        query: The query to validate
        max_length: Maximum allowed query length
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    # Check size limits
    if not query:
        return False, ["Query is empty"]
    
    if len(query) > max_length:
        return False, [f"Query exceeds maximum length of {max_length} characters"]
    
    try:
        # Use KustoLanguage library for validation
        kql_code = self.KustoCode.Parse(query)
        diagnostics = list(kql_code.GetDiagnostics())
        
        if diagnostics:
            # Format diagnostics into readable messages
            error_messages = []
            for diag in diagnostics:
                # Extract position safely
                try:
                    line_pos = f"Line {diag.Start.Line}, Position {diag.Start.Column}"
                except:
                    line_pos = "Unknown position"
                
                # Extract message safely
                try:
                    message = diag.Message
                except:
                    message = str(diag)
                
                error_messages.append(f"{line_pos}: {message}")
            return False, error_messages
        
        return True, []
    except Exception as e:
        # Handle validation errors
        return False, [f"Error validating query: {type(e).__name__}"]
```

#### Secure Error Handling Implementation

```python
async def execute_query(query: str, workspace_id: str, timespan: Union[str, timedelta]) -> Dict[str, Any]:
    """
    Execute KQL query securely.
    
    Args:
        query: The KQL query to execute
        workspace_id: Target workspace ID
        timespan: Query time window
        
    Returns:
        Query results or error information
    """
    # Convert timespan to appropriate type
    time_delta = timespan if isinstance(timespan, timedelta) else parse_timespan(timespan)
    
    try:
        # Execute query with timeout
        response = await run_in_thread(
            self.logs_client.query_workspace,
            workspace_id=workspace_id,
            query=query,
            timespan=time_delta,
            name=f"query_{hash(query) % 10000}",  # Safe hash for identification
            timeout=60.0  # Hard timeout
        )
        
        # Process and return results
        if response and response.tables:
            # Format and return data safely
            return {
                "success": True,
                "rows": len(response.tables[0].rows),
                "data": format_query_results(response)
            }
        else:
            return {
                "success": True,
                "rows": 0,
                "data": "Query executed successfully but returned no results"
            }
    except Exception as e:
        # Secure error handling
        error_type = type(e).__name__
        error_message = str(e)
        
        # Remove any sensitive information
        sanitized_message = sanitize_error_message(error_message)
        
        logger.error(f"Query execution error: {error_type}: {sanitized_message}")
        
        return {
            "success": False,
            "error_type": error_type,
            "message": sanitized_message
        }
```
