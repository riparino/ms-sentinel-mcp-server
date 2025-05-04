"""
Microsoft Graph API utilities for authentication, token handling, 
permission checking, and REST calls.

This module centralizes all logic for interacting with Microsoft Graph, including:
- GraphApiClient: Handles authentication and REST requests
- check_graph_permissions: Validates required permissions in a JWT token
- Utility functions for token decoding and context detection
"""

import logging
import jwt
from azure.identity import CredentialUnavailableError
from utilities.cache import cache
from utilities.api_utils import AzureApiClient

logger = logging.getLogger(__name__)
GRAPH_SCOPE = "https://graph.microsoft.com/.default"
GRAPH_API_BASE = "https://graph.microsoft.com/v1.0"
REQUIRED_PERMISSIONS = ["User.Read.All", "Group.Read.All"]


class GraphApiClient(AzureApiClient):
    """
    AzureApiClient subclass for Microsoft Graph API calls.

    Provides a method to acquire a Microsoft Graph API access token
    using the configured Azure credential.
    """

    def get_token(self):
        """
        Acquire a Microsoft Graph API access token using the configured Azure credential.

        Returns:
            str: The acquired access token.
        Raises:
            CredentialUnavailableError: If Azure credentials are unavailable.
            Exception: For other errors during token acquisition.
        """
        try:
            token = self.credential.get_token(GRAPH_SCOPE).token
            self._token = token
            return token
        except CredentialUnavailableError as e:
            logger.warning("Azure credential unavailable: %s", e)
            raise
        except Exception as e:
            logger.warning("Failed to get Graph API token: %s", e)
            raise

    def call_graph_api(self, method, url, **kwargs):
        """
        Make a REST call to Microsoft Graph API.
        """
        return self.call_azure_rest_api(method, url, **kwargs)


def decode_graph_token(token):
    """
    Decode a JWT token for Microsoft Graph (without signature verification).
    Returns the claims dict or raises jwt.InvalidTokenError.
    """
    return jwt.decode(token, options={"verify_signature": False})


def detect_graph_context(claims):
    """
    Detects if the token is for an app registration, user account, or unknown.
    Returns one of: 'app registration', 'user account', or 'identity'.
    """
    if "appid" in claims and "upn" not in claims:
        return "app registration"
    elif "upn" in claims or "unique_name" in claims:
        return "user account"
    return "identity"


def check_graph_permissions(
    token,
    required_permissions=None,
    cache_key="entra_id_graph_permissions",
):
    """
    Checks if the current identity (from token) has required Microsoft Graph permissions.
    Caches the result for efficiency.
    Raises:
        Exception: If required permissions are missing.
    """
    if required_permissions is None:
        required_permissions = REQUIRED_PERMISSIONS
    permissions = cache.get(cache_key)
    claims = None
    if permissions is None:
        try:
            claims = decode_graph_token(token)
            permissions = claims.get("roles", []) or claims.get("scp", "").split()
            cache.set(cache_key, permissions)
        except jwt.InvalidTokenError as e:
            logger.warning("Failed to decode Graph token: %s", e)
            permissions = []
        except Exception as e:
            logger.warning("Could not check Graph permissions: %s", e)
            raise Exception(
                "Unable to check Microsoft Graph permissions. Please check your credentials."
            ) from e
    else:
        # If cached, we need to decode token for context_hint
        try:
            claims = decode_graph_token(token)
        except Exception:
            claims = {}
    missing = [perm for perm in required_permissions if perm not in permissions]
    context_hint = detect_graph_context(claims or {})
    if missing:
        error_msg = (
            f"Missing Microsoft Graph permissions: {', '.join(missing)}. "
            f"Please grant these permissions to your {context_hint} "
            f"and ensure admin consent is granted."
        )
        raise Exception(error_msg)
    return True
