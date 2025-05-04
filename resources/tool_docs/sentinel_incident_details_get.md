# sentinel_incident_get

## Purpose
Retrieves detailed information about a specific Microsoft Sentinel incident, including all available fields and calculated counts for related alerts, bookmarks, and comments. Also returns up to 5 related alerts if present.

## Parameters
| Name           | Type   | Required | Description                                                      |
|----------------|--------|----------|------------------------------------------------------------------|
| incident_number| int    | Yes      | The IncidentNumber of the Sentinel incident to retrieve.          |
| kwargs         | dict   | No       | Additional parameters (for nested invocation compatibility).      |

## Output Fields
The tool returns a dictionary with the following structure:

| Key            | Type    | Description                                                         |
|----------------|---------|---------------------------------------------------------------------|
| incident       | dict    | All columns from the `SecurityIncident` table, plus calculated fields: `AlertsCount`, `BookmarksCount`, `CommentsCount`. |
| related_alerts | list    | Up to 5 related alerts (dicts) from the `SecurityAlert` table, joined by `AlertIds`/`SystemAlertId`. |
| error          | string  | Present only if an error occurred.                                  |
| message        | string  | Present if no incident was found.                                   |

### Example `incident` fields (non-exhaustive):
- IncidentNumber
- Title
- Description
- Severity
- Status
- Classification
- ClassificationComment
- CreatedTime
- LastModifiedTime
- IncidentUrl
- ProviderName
- AlertsCount (calculated)
- BookmarksCount (calculated)
- CommentsCount (calculated)
- AlertIds (list)
- ... (all other columns from SecurityIncident)

### Example `related_alerts` fields:
- Time
- Name
- Severity
- Status
- Description
- Entities

## Example Request
```
{
  "incident_number": 3
}
```

## Example Response
```
{
  "incident": {
    "IncidentNumber": 3,
    "Title": "Suspicious Resource deployment",
    "Description": "Identifies when a rare Resource and ResourceGroup deployment occurs by a previously unseen caller.",
    "Severity": "Low",
    "Status": "New",
    "Classification": "",
    "ClassificationComment": "",
    "CreatedTime": "2025-04-17T12:34:13.422179Z",
    ...
    "AlertsCount": 1,
    "BookmarksCount": 0,
    "CommentsCount": 0,
    "AlertIds": ["40cefd90-2f07-b1ea-bcd0-ae811cbde0ed"],
    ...
  },
  "related_alerts": [
    {
      "Time": "2025-04-17T12:34:13.422179Z",
      "Name": "AlertName",
      "Severity": "High",
      "Status": "Active",
      "Description": "desc",
      "Entities": ["entity"]
    }
  ]
}
```

## Usage Notes
- Returns all available fields from the incident, including any new columns added to the schema.
- If no incident is found, returns a dict with a `message` key.
- If `AlertIds` is empty or missing, `related_alerts` will be an empty list.
- Handles both MCP server and direct invocation (using environment variables for Azure context if needed).
- All errors are returned as a dict with an `error` key.

## Error Cases
- Missing or invalid `incident_number` parameter.
- Incident not found.
- Azure authentication or query errors.

## See Also
- [sentinel_incident_list](sentinel_incident_list.md) — for listing incidents.
- [sentinel_logs_table_schema_get](sentinel_logs_table_schema_get.md) — for table schema details.
