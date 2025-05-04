#!/usr/bin/env python3

"""
UTILITIES: api_utils.py
Utility functions for making direct Azure REST API calls.
"""

from typing import Any, Dict, Generator, Optional

import requests
from azure.identity import CredentialUnavailableError, DefaultAzureCredential
from utilities.logging import get_tool_logger

logger = get_tool_logger("api_utils")


class AzureApiClient:
    """
    Client for making authenticated Azure REST API calls using Azure Active Directory credentials.

    Provides token management and utility methods for robust, paginated REST API access.
    """
    def __init__(self, credential: Optional[DefaultAzureCredential] = None):
        """
        Initialize the AzureApiClient.

        Args:
            credential (Optional[DefaultAzureCredential]): An optional Azure credential instance. If not provided, DefaultAzureCredential is used.
        """
        self.credential = credential or DefaultAzureCredential()
        self._token = None

    def get_token(self) -> str:
        """
        Acquire and cache a bearer token for Azure REST API authentication.

        Returns:
            str: The acquired bearer token as a string.

        Raises:
            CredentialUnavailableError: If Azure credentials are unavailable.
            Exception: For any other errors during token acquisition.
        """
        try:
            token = self.credential.get_token(
                "https://management.azure.com/.default"
            ).token
            self._token = token
            return token
        except CredentialUnavailableError as e:
            logger.error("Azure credential unavailable: %s", e)
            raise
        except Exception as e:
            logger.error("Failed to get Azure token: %s", e)
            raise

    def call_azure_rest_api(
        self,
        method: str,
        url: str,
        *,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        body: Optional[dict] = None,
        max_pages: int = 10
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Make a generic Azure REST API call with error and pagination handling.

        Args:
            method (str): HTTP method to use (e.g., 'GET', 'POST').
            url (str): The Azure REST API endpoint URL.
            params (Optional[dict]): Query parameters for the request.
            headers (Optional[dict]): Additional headers to include in the request.
            body (Optional[dict]): JSON body to send with the request.
            max_pages (int): Maximum number of paginated results to fetch.

        Yields:
            Dict[str, Any]: The response data for each page as a dictionary.

        Raises:
            requests.exceptions.HTTPError: If an HTTP error occurs.
            requests.exceptions.Timeout: If the request times out.
            Exception: For any other errors during the REST call.
        """
        if not self._token:
            self.get_token()
        session = requests.Session()
        req_headers = headers.copy() if headers else {}
        req_headers["Authorization"] = f"Bearer {self._token}"
        req_headers["Content-Type"] = "application/json"

        page = 0
        while url and page < max_pages:
            try:
                resp = session.request(
                    method,
                    url,
                    params=params,
                    headers=req_headers,
                    json=body,
                    timeout=30,
                )
                resp.raise_for_status()
                data = resp.json()
                yield data
                # Pagination: Azure REST APIs use 'nextLink' for paging
                url = data.get("nextLink")
                params = None  # nextLink already has all params
                page += 1
            except requests.exceptions.HTTPError as e:
                logger.error(
                    "HTTP error during Azure REST call: %s (Status: %s)",
                    e,
                    getattr(e.response, "status_code", None),
                )
                raise
            except requests.exceptions.Timeout:
                logger.error("Timeout during Azure REST API call.")
                raise
            except Exception as e:
                logger.error("Unexpected error during Azure REST call: %s", e)
                raise
        if page == max_pages:
            logger.warning(
                "Max pages (%s) reached during Azure REST API pagination.", max_pages
            )
