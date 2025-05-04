# Entra ID Get Group Tool

**Tool Name:** `entra_id_get_group`

**Description:**
Retrieves a single group from Microsoft Entra ID (Azure AD) by object ID, using the Microsoft Graph API.

---

## Parameters
- `group_id` (string, required): The object ID of the group to retrieve (e.g., `06adad8d-89b3-4b64-82b0-7d5e17dfac3f`).

---

## Returns
A JSON object representing the group, with fields including:
- `displayName`: The group's display name.
- `description`: The group's description.
- `id`: The unique object ID of the group.
- Additional fields may include `mail`, `mailNickname`, `securityEnabled`, etc.

---

## Example Output
```json
{
  "displayName": "sg-IT",
  "description": "All IT personnel",
  "id": "06adad8d-89b3-4b64-82b0-7d5e17dfac3f"
}
```

---

## Permissions Required
- `Group.Read.All` (Microsoft Graph)

---

## Error Handling
- Returns a permission error if the caller lacks the required Graph API permissions.
- Returns a clear error if the specified group does not exist or if the Graph API is unreachable.
- Returns an error if `group_id` is missing or invalid.

---

## Example Use Case
Use this tool to retrieve details for a specific group in your Azure AD tenant, for group lookups, automation, or audit purposes.

---

## Notes
NIL
