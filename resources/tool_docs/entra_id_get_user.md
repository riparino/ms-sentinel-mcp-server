# Entra ID Get User Tool

**Tool Name:** `entra_id_get_user`

**Description:**
Retrieves a single user from Microsoft Entra ID (Azure AD) by object ID, UPN (User Principal Name), or email address, using the Microsoft Graph API.

---

## Parameters
- `user_id` (string, optional): The object ID (e.g., `31d6905a-fb48-4e75-a41e-dbd214689352`) of the user to retrieve.
- `upn` (string, optional): The User Principal Name (UPN) of the user (e.g., `AdeleV@example.OnMicrosoft.com`).
- `email` (string, optional): The user's primary email address (e.g., `AdeleV@example.OnMicrosoft.com`).
 
**At least one of `user_id`, `upn`, or `email` must be provided.**

---

## Returns
A JSON object representing the user, with fields including:
- `displayName`: The user's display name.
- `userPrincipalName`: The user's UPN (login name).
- `mail`: The user's primary email address.
- `id`: The unique object ID of the user.
- Additional fields may include `givenName`, `surname`, `businessPhones`, etc.

---

## Example Output
```json
{
  "displayName": "Adele Vance",
  "userPrincipalName": "AdeleV@example.OnMicrosoft.com",
  "mail": "AdeleV@example.OnMicrosoft.com",
  "id": "31d6905a-fb48-4e75-a41e-dbd214689352"
}
```

## Example Usage
- Lookup by object ID:
  ```json
  { "user_id": "31d6905a-fb48-4e75-a41e-dbd214689352" }
  ```
- Lookup by UPN:
  ```json
  { "upn": "AdeleV@example.OnMicrosoft.com" }
  ```
- Lookup by email:
  ```json
  { "email": "AdeleV@example.OnMicrosoft.com" }
  ```

---

## Permissions Required
- `User.Read.All` (Microsoft Graph)

---

## Error Handling
- Returns a permission error if the caller lacks the required Graph API permissions.
- Returns a clear error if the specified user does not exist or if the Graph API is unreachable.
- Returns an error if none of `user_id`, `upn`, or `email` is provided.
- Returns an error if the specified user does not exist.

---

## Example Use Case
Use this tool to retrieve details for a specific user in your Azure AD tenant, for user lookups, automation, or audit purposes.

---

## Notes
NIL
