# sentinel_domain_whois_get

## Description
Get WHOIS information for a domain using Microsoft Sentinel's enrichment API.

## Parameters

| Parameter | Type   | Required | Description                     |
|-----------|--------|----------|---------------------------------|
| domain    | string | Yes      | The domain name to look up      |

## Returns

| Field   | Type   | Description                                |
|---------|--------|--------------------------------------------|
| whois   | object | WHOIS data for the specified domain        |
| valid   | bool   | Whether the operation was successful       |

### WHOIS Object Fields

| Field       | Type   | Description                                       |
|-------------|--------|---------------------------------------------------|
| domain      | string | The domain that was looked up                     |
| server      | string | WHOIS server used for the lookup                  |
| created     | string | Domain creation date (ISO 8601 format)            |
| updated     | string | Last update date (ISO 8601 format)                |
| expires     | string | Expiration date (ISO 8601 format)                 |
| parsed_whois| object | Structured WHOIS data                             |

### parsed_whois Object Fields

| Field       | Type   | Description                                       |
|-------------|--------|---------------------------------------------------|
| registrar   | object | Information about the domain registrar            |
| contacts    | object | Contact information for domain roles              |
| name_servers| array  | List of domain name servers                       |
| statuses    | array  | Domain status codes                               |

#### registrar Object Fields

| Field              | Type   | Description                                       |
|--------------------|--------|---------------------------------------------------|
| name               | string | Registrar company name                            |
| abuse_contact_email| string | Email for abuse reports                           |
| abuse_contact_phone| string | Phone number for abuse reports                    |
| iana_id            | string | IANA ID of the registrar                          |
| url                | string | Registrar URL                                     |
| whois_server       | string | Registrar's WHOIS server                          |

#### contacts Object Fields
Contains admin, billing, registrant, and tech objects, each with the following fields:

| Field       | Type   | Description                                       |
|-------------|--------|---------------------------------------------------|
| name        | string | Contact name                                      |
| org         | string | Organization name                                 |
| street      | array  | Street address lines                              |
| city        | string | City                                              |
| state       | string | State or province                                 |
| postal      | string | Postal code                                       |
| country     | string | Country code                                      |
| phone       | string | Phone number                                      |
| fax         | string | Fax number                                        |
| email       | string | Email address                                     |

## Error Response

| Field   | Type   | Description                                |
|---------|--------|--------------------------------------------|
| error   | string | Error message if the operation failed      |
| valid   | bool   | false                                      |

## Examples

### Request
```json
{
  "domain": "microsoft.com"
}
```

### Response
```json
{
  "whois": {
    "domain": "microsoft.com",
    "server": "whois.markmonitor.com",
    "created": "1991-05-02T04:00:00.000Z",
    "updated": "2023-08-18T16:15:54.000Z",
    "expires": "2025-05-03T00:00:00.000Z",
    "parsed_whois": {
      "registrar": {
        "name": "MarkMonitor Inc.",
        "abuse_contact_email": "abusecomplaints@markmonitor.com",
        "abuse_contact_phone": "+1.2086851750",
        "iana_id": "292",
        "url": "292",
        "whois_server": "whois.markmonitor.com"
      },
      "contacts": {
        "admin": {
          "name": "Domain Administrator",
          "org": "Microsoft Corporation",
          "street": ["One Microsoft Way"],
          "city": "Redmond",
          "state": "WA",
          "postal": "98052",
          "country": "US",
          "phone": "+1.4258828080",
          "fax": "+1.4259367329",
          "email": "admin@domains.microsoft"
        },
        "billing": {
          "name": "",
          "org": "",
          "street": [""],
          "city": "",
          "state": "",
          "postal": "",
          "country": "",
          "phone": "+1.2086851750",
          "fax": "",
          "email": "abusecomplaints@markmonitor.com"
        },
        "registrant": {
          "name": "Domain Administrator",
          "org": "Microsoft Corporation",
          "street": ["One Microsoft Way"],
          "city": "Redmond",
          "state": "WA",
          "postal": "98052",
          "country": "US",
          "phone": "+1.4258828080",
          "fax": "+1.4259367329",
          "email": "admin@domains.microsoft"
        },
        "tech": {
          "name": "MSN Hostmaster",
          "org": "Microsoft Corporation",
          "street": ["One Microsoft Way"],
          "city": "Redmond",
          "state": "WA",
          "postal": "98052",
          "country": "US",
          "phone": "+1.4258828080",
          "fax": "+1.4259367329",
          "email": "msnhst@microsoft.com"
        }
      },
      "name_servers": [
        "ns1-39.azure-dns.com",
        "ns2-39.azure-dns.net",
        "ns3-39.azure-dns.org",
        "ns4-39.azure-dns.info"
      ],
      "statuses": ["ACTIVE"]
    }
  },
  "valid": true
}
```

### Error Example
```json
{
  "error": "Error retrieving WHOIS data for example.invalid: Domain not found",
  "valid": false
}
```

## Notes
- This tool uses Microsoft Sentinel's domain WHOIS enrichment API
- Unlike other Sentinel APIs, this enrichment API does not require a workspace_name parameter
- The tool returns structured WHOIS data that has been parsed from the raw WHOIS response
- Some fields may be empty or missing depending on the domain's registration information
- All dates are returned in ISO 8601 format (YYYY-MM-DDThh:mm:ss.sssZ)

## Permissions Required
- Azure Resource Group Reader access or higher
- Microsoft.SecurityInsights/enrichment/read permission

## Related Tools
- sentinel_ip_geodata_get - Get geolocation data for an IP address
