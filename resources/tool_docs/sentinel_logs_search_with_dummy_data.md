# Sentinel Query With Dummy Data Tool

## Overview
The `sentinel_logs_search_with_dummy_data` tool allows security analysts to safely test Microsoft Sentinel KQL queries against mock data without accessing or modifying production data. It leverages the KQL `datatable` construct to create a temporary table from user-supplied mock records, then rebinds the original query's table reference to this mock table. The query logic remains unchanged, ensuring high-fidelity testing and validation.

---

## Parameters
| Name           | Type    | Required | Description                                                |
|----------------|---------|----------|------------------------------------------------------------|
| query          | string  | Yes      | The original KQL query to test.                            |
| mock_data_xml  | string  | No*      | XML string containing mock records (preferred format).     |
| mock_data_csv  | string  | No*      | CSV string with header row and mock records.               |
| table_name     | string  | No       | The table name to substitute in the query (default: TestTable). |

*At least one of mock_data_xml or mock_data_csv must be provided.

---

## Output Fields
| Field           | Type    | Description                                                                 |
|-----------------|---------|-----------------------------------------------------------------------------|
| valid           | bool    | Whether the query executed successfully.                                     |
| errors          | array   | List of error messages, if any.                                             |
| error           | string  | Main error message, if any.                                                 |
| original_query  | string  | The original KQL query as provided.                                         |
| table_name      | string  | The table name used in substitution.                                        |
| datatable_var   | string  | The variable name for the generated datatable.                              |
| test_query      | string  | The full KQL query executed (with datatable and let binding).               |
| result          | object  | Results from query execution (see below).                                   |

### Result Object
- `valid`: bool
- `errors`: array
- `query`: string (the full executed query)
- `result_count`: int
- `columns`: array of column descriptors
- `rows`: array of result records
- `execution_time_ms`: int
- `warnings`: array
- `message`: string

---

## Example Usage
### Example 1: Device Code Authentication Detection
**Example 1: Using XML Format (Preferred)**
```
query:
SigninLogs
| where TimeGenerated > ago(1d)
| where AuthenticationProtocol =~ "deviceCode" \
    or OriginalTransferMethod =~ "deviceCodeFlow"
| project TimeGenerated,
    UserPrincipalName,
    UserDisplayName,
    UserId,
    IPAddress,
    Location,
    AppDisplayName,
    ClientAppUsed,
    AuthenticationProtocol,
    OriginalTransferMethod,
    DeviceDetail,
    Status,
    ResourceDisplayName
| extend AlertDetails = pack(
    "UserId", UserId,
    "ClientApp", ClientAppUsed,
    "AppDisplayName", AppDisplayName,
    "Protocol", AuthenticationProtocol,
    "TransferMethod", OriginalTransferMethod,
    "DeviceInfo", DeviceDetail
)
| extend Reason = "Device Code Authentication Flow detected which may indicate unauthorized access if not used with input-constrained devices"
| extend timestamp = TimeGenerated, AccountCustomEntity = UserPrincipalName, IPCustomEntity = IPAddress

mock_data_xml:
<rows>
  <row>
    <TimeGenerated>2025-04-22T10:15:00Z</TimeGenerated>
    <UserPrincipalName>alice@contoso.com</UserPrincipalName>
    <UserDisplayName>Alice Smith</UserDisplayName>
    <UserId>alice123</UserId>
    <IPAddress>192.168.1.1</IPAddress>
    <Location>Sydney, Australia</Location>
    <AppDisplayName>Microsoft Office</AppDisplayName>
    <ClientAppUsed>Mobile App</ClientAppUsed>
    <AuthenticationProtocol>deviceCode</AuthenticationProtocol>
    <OriginalTransferMethod></OriginalTransferMethod>
    <DeviceDetail>
      <deviceId>dev123</deviceId>
      <displayName>iPhone 15</displayName>
      <operatingSystem>iOS</operatingSystem>
      <browser>Edge</browser>
    </DeviceDetail>
    <Status>
      <errorCode>0</errorCode>
      <additionalDetails>Success</additionalDetails>
    </Status>
    <ResourceDisplayName>Microsoft Graph</ResourceDisplayName>
  </row>
  <row>
    <TimeGenerated>2025-04-22T11:30:00Z</TimeGenerated>
    <UserPrincipalName>bob@contoso.com</UserPrincipalName>
    <UserDisplayName>Bob Jones</UserDisplayName>
    <UserId>bob456</UserId>
    <IPAddress>10.0.0.5</IPAddress>
    <Location>Melbourne, Australia</Location>
    <AppDisplayName>Azure Portal</AppDisplayName>
    <ClientAppUsed>Browser</ClientAppUsed>
    <AuthenticationProtocol>oauth2</AuthenticationProtocol>
    <OriginalTransferMethod>deviceCodeFlow</OriginalTransferMethod>
    <DeviceDetail>
      <deviceId>dev456</deviceId>
      <displayName>Windows Laptop</displayName>
      <operatingSystem>Windows</operatingSystem>
      <browser>Chrome</browser>
    </DeviceDetail>
    <Status>
      <errorCode>0</errorCode>
      <additionalDetails>Success</additionalDetails>
    </Status>
    <ResourceDisplayName>Azure Portal</ResourceDisplayName>
  </row>
</rows>

table_name: SigninLogs
```

**Example 2: Using CSV Format (Alternative)**
```
query:
SecurityEvent 
| where EventID == 4624
| where AccountType == "User"
| project TimeGenerated, Computer, Account, IpAddress

mock_data_csv:
TimeGenerated,Computer,Account,AccountType,EventID,IpAddress
2025-04-22T10:15:00Z,DC01,JohnDoe,User,4624,192.168.1.100
2025-04-22T11:30:00Z,DC01,JaneDoe,User,4624,192.168.1.101
2025-04-22T12:45:00Z,DC02,AdminUser,User,4624,10.0.0.50

table_name: SecurityEvent
```

**Output**
```
{
  "valid": true,
  "errors": [],
  "error": "",
  "original_query": "SigninLogs | where TimeGenerated > ago(1d) ...",
  "table_name": "SigninLogs",
  "datatable_var": "SigninLogsDummy",
  "test_query": "let SigninLogsDummy = datatable( ... ); let SigninLogs = SigninLogsDummy; ...",
  "result": {
    "valid": true,
    "errors": [],
    "result_count": 3,
    "columns": [ ... ],
    "rows": [ ... ],
    "execution_time_ms": 3325,
    "warnings": [],
    "message": "Query executed successfully"
  }
}
```

---

## Usage Notes
- Supports two data input formats:
  - **XML Format (preferred)**: Better for complex data with nested structures
  - **CSV Format**: Simpler option for flat tabular data
- The tool automatically infers the correct KQL types for each column, including `datetime` for ISO8601 strings.
- Handles nested structures in XML (converted to dynamic objects in KQL)
- The original query logic is preserved; only the data source is swapped for the mock datatable.
- No production or sensitive data is accessed or modified.
- Useful for detection rule development, debugging, documentation, and training.

---

## Error Cases
- If no mock data is provided in either XML or CSV format, the tool will return a helpful error with examples.
- If the XML or CSV data cannot be parsed, specific parsing errors will be returned.
- If the mock data is missing required columns referenced in the query, appropriate errors will be provided.
- KQL syntax errors in the original query will be reported.
- Any query execution errors are surfaced in the `errors` and `error` fields.

---

## References
- [KQL datatable documentation](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/datatableoperator)
- [Microsoft Sentinel KQL documentation](https://learn.microsoft.com/en-us/azure/sentinel/)

---

## Security and Privacy
- No workspace or environment-specific details are included in the documentation or output.
- All testing is performed in-memory and does not affect production data or configuration.

---

