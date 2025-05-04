# Entra ID List Groups Tool

**Tool Name:** `entra_id_list_groups`

**Description:**
Lists all groups in Microsoft Entra ID (Azure AD) via the Microsoft Graph API.

---

## Parameters
_None_

---

## Returns
A JSON array of group objects, each containing (at minimum):
- `displayName`: The group's display name.
- `description`: The group's description.
- `id`: The unique object ID of the group.
- Additional fields may include `mail`, `mailNickname`, `securityEnabled`, etc.

---

## Example Output
```json
[
  {
    "displayName": "sg-IT",
    "description": "All IT personnel",
    "id": "06adad8d-89b3-4b64-82b0-7d5e17dfac3f"
  },
  // ...more groups
]
```

---

## Permissions Required
- `Group.Read.All` (Microsoft Graph)

---

## Error Handling
- Returns a permission error if the caller lacks the required Graph API permissions.
- Returns a clear error if the Graph API is unreachable or misconfigured.

---

## Example Use Case
Use this tool to enumerate all groups in your Azure AD tenant, for reporting, automation, or auditing.

---

## Notes
- For large tenants, paging is handled automatically.
