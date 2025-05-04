# sentinel_ip_geodata_get

## Description
Get geolocation data for an IP address using Microsoft Sentinel's enrichment API.

## Parameters

| Parameter | Type   | Required | Description                     |
|-----------|--------|----------|---------------------------------|
| ip        | string | Yes      | The IP address to look up       |

## Returns

| Field   | Type   | Description                                |
|---------|--------|--------------------------------------------|
| geodata | object | Geolocation data for the specified IP address |
| valid   | bool   | Whether the operation was successful       |

### Geodata Object Fields

| Field              | Type   | Description                                       |
|--------------------|--------|---------------------------------------------------|
| ip                 | string | The IP address that was looked up                 |
| ip_addr            | string | The IP address in standard format                 |
| asn                | string | Autonomous System Number                          |
| carrier            | string | Network carrier name                              |
| city               | string | City name                                         |
| city_cf            | number | City confidence factor (0-100)                    |
| continent          | string | Continent name                                    |
| country            | string | Country name                                      |
| country_cf         | number | Country confidence factor (0-100)                 |
| ip_routing_type    | string | Routing type (e.g., "fixed")                      |
| latitude           | string | Geographic latitude                               |
| longitude          | string | Geographic longitude                              |
| organization       | string | Organization name                                 |
| organization_type  | string | Type of organization                              |
| region             | string | Geographic region                                 |
| state              | string | State or province name                            |
| state_cf           | number | State confidence factor (0-100)                   |
| state_code         | string | State or province code                            |

## Error Response

| Field   | Type   | Description                                |
|---------|--------|--------------------------------------------|
| error   | string | Error message if the operation failed      |
| valid   | bool   | false                                      |

## Examples

### Request
```json
{
  "ip": "8.8.8.8"
}
```

### Response
```json
{
  "geodata": {
    "asn": "15169",
    "carrier": "google",
    "city": "glenmont",
    "city_cf": 80,
    "continent": "north america",
    "country": "united states",
    "country_cf": 99,
    "ip_addr": "8.8.8.8",
    "ip_routing_type": "fixed",
    "latitude": "40.537",
    "longitude": "-82.12859",
    "organization": "google",
    "organization_type": "Internet Service Provider",
    "region": "great lakes",
    "state": "ohio",
    "state_cf": 95,
    "state_code": "oh",
    "ip": "8.8.8.8"
  },
  "valid": true
}
```

### Error Example
```json
{
  "error": "Error retrieving IP geodata for 8.8.8.8: Invalid IP address format",
  "valid": false
}
```

## Notes
- This tool uses Microsoft Sentinel's IP geodata enrichment API
- Unlike other Sentinel APIs, this enrichment API does not require a workspace_name parameter
- Confidence factors (CF) indicate the reliability of the location data on a scale of 0-100
- The tool will return all available geolocation data for the IP address
- Some fields may be missing if the data is not available for the specific IP address

## Permissions Required
- Azure Resource Group Reader access or higher
- Microsoft.SecurityInsights/enrichment/read permission

## Related Tools
- sentinel_domain_whois_get - Get WHOIS information for a domain
