# Entra ID List Users Tool

**Tool Name:** `entra_id_list_users`

**Description:**
Lists all users in Microsoft Entra ID (Azure AD) via the Microsoft Graph API.

---

## Parameters
_None_

---

## Returns
A JSON array of user objects, each containing (at minimum):
- `displayName`: The user's display name.
- `userPrincipalName`: The user's UPN (login name).
- `mail`: The user's primary email address.
- `id`: The unique object ID of the user.
- Additional fields may include `givenName`, `surname`, `businessPhones`, etc.

---

## Example Output
```json
[
  {
    "displayName": "Adele Vance",
    "userPrincipalName": "AdeleV@example.OnMicrosoft.com",
    "mail": "AdeleV@example.OnMicrosoft.com",
    "id": "31d6905a-fb48-4e75-a41e-dbd214689352"
  },
  {
    "displayName": "Alex Wilber",
    "userPrincipalName": "AlexW@example.OnMicrosoft.com",
    "mail": "AlexW@example.OnMicrosoft.com",
    "id": "4c56c3b6-a237-40ca-8d53-1ea68a4961d8"
  }
  // ...more users
]
```

---

## Permissions Required
- `User.Read.All` (Microsoft Graph)

---

## Error Handling
- Returns a permission error if the caller lacks the required Graph API permissions.
- Returns a clear error if the Graph API is unreachable or misconfigured.

---

## Example Use Case
Use this tool to enumerate all users in your Azure AD tenant, e.g., for reporting, auditing, or automation workflows.

---

## Notes
- For large tenants, paging is handled automatically.
