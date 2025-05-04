"""
FILE: utilities/connection_test.py
DESCRIPTION:
    Utility script to test Azure connections and validate environment configuration.
    This script can be run directly to check if Azure credentials are properly configured.
"""

import os
import sys
import logging
from typing import Dict, Any, Optional, Tuple
from datetime import timedelta

from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ClientAuthenticationError
from azure.monitor.query import LogsQueryClient
from azure.mgmt.securityinsight import SecurityInsights

# Set up logging to stderr
logger = logging.getLogger("connection_test")
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def get_environment_config() -> Dict[str, str]:
    """
    Get Azure configuration from environment variables.

    Returns:
        Dictionary with configuration values
    """
    config = {
        "tenant_id": os.environ.get("AZURE_TENANT_ID", ""),
        "client_id": os.environ.get("AZURE_CLIENT_ID", ""),
        "client_secret": os.environ.get("AZURE_CLIENT_SECRET", ""),
        "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID", ""),
        "resource_group": os.environ.get("AZURE_RESOURCE_GROUP", ""),
        "workspace_id": os.environ.get("AZURE_WORKSPACE_ID", ""),
        "workspace_name": os.environ.get("AZURE_WORKSPACE_NAME", ""),
    }

    # Check for missing variables
    missing_vars = [k for k, v in config.items() if not v]
    if missing_vars:
        logger.warning("Missing environment variables: %s", ", ".join(missing_vars))

    return config


def test_azure_credential() -> Tuple[bool, Optional[DefaultAzureCredential], str]:
    """
    Test if Azure credentials are correctly configured.

    Returns:
        Tuple of (success, credential, message)
    """
    try:
        # Try to create the credential
        credential = DefaultAzureCredential()

        # Test the credential by getting a token
        # This will throw if credentials are invalid
        token = credential.get_token("https://management.azure.com/.default")

        if token:
            return True, credential, "Azure credentials successfully validated"
        else:
            return False, None, "Failed to acquire token with DefaultAzureCredential"

    except ClientAuthenticationError as e:
        return False, None, f"Authentication error: {str(e)}"
    except Exception as e:
        return False, None, f"Unexpected error creating credentials: {str(e)}"


def azure_logs_client_check(
    credential: DefaultAzureCredential, workspace_id: str
) -> Tuple[bool, str]:
    """
    Utility: Test connection to Azure Monitor Logs.
    """
    if not workspace_id:
        msg = "No workspace ID provided"
        if "pytest" in sys.modules:
            assert False, msg
        return False, msg
    try:
        logs_client = LogsQueryClient(credential)

        response = logs_client.query_workspace(
            workspace_id=workspace_id,
            query="Heartbeat | summarize count() | take 1",
            timespan=timedelta(hours=1),
        )
        if hasattr(response, "tables") and getattr(response, "tables", None):
            return True, "Successfully connected to workspace and ran query"
        elif hasattr(response, "partial_data") and getattr(
            response, "partial_data", None
        ):
            return (
                True,
                "Successfully connected to workspace and ran query (partial data)",
            )
        elif hasattr(response, "result") and getattr(response, "result", None):
            return True, "Successfully connected to workspace and ran query"
        else:
            return False, "Connected to workspace but query returned no data"
    except Exception as e:
        return False, f"Error connecting to Log Analytics: {str(e)}"


def azure_security_insights_check(
    credential: DefaultAzureCredential,
    subscription_id: str,
    resource_group: str,
    workspace_name: str,
) -> Tuple[bool, str]:
    """
    Utility: Test connection to Security Insights.
    """
    if not (subscription_id and resource_group and workspace_name):
        msg = "Missing required parameters for Security Insights test"
        if "pytest" in sys.modules:
            assert False, msg
        return False, msg
    try:
        insights_client = SecurityInsights(credential, subscription_id)
        connectors = list(
            insights_client.data_connectors.list(
                resource_group_name=resource_group, workspace_name=workspace_name
            )
        )
        connector_count = len(connectors)
        return (
            True,
            f"Successfully connected to Security Insights. "
            f"Found {connector_count} data connectors.",
        )
    except Exception as e:
        msg = f"Error connecting to Security Insights: {str(e)}"
        if "pytest" in sys.modules:
            assert False, msg
        return False, msg


def run_connection_tests() -> Dict[str, Any]:
    """
    Run all connection tests and return results.

    Returns:
        Dictionary with test results
    """
    test_results = {
        "environment_config": {},
        "credential_test": {},
        "logs_client_test": {},
        "security_insights_test": {},
    }

    # Get environment configuration
    config = get_environment_config()
    test_results["environment_config"] = {
        "tenant_id": "✓" if config["tenant_id"] else "✗",
        "client_id": "✓" if config["client_id"] else "✗",
        "client_secret": "✓" if config["client_secret"] else "✗",
        "subscription_id": "✓" if config["subscription_id"] else "✗",
        "resource_group": "✓" if config["resource_group"] else "✗",
        "workspace_id": "✓" if config["workspace_id"] else "✗",
    }

    # Test credential
    cred_success, credential, cred_message = test_azure_credential()
    test_results["credential_test"] = {"success": cred_success, "message": cred_message}

    # If credential test failed, skip other tests
    if not cred_success or credential is None:
        logger.error("Credential test failed, skipping other tests")
        return test_results

    # Test Log Analytics connection - credential is already checked for None above
    logs_success, logs_message = azure_logs_client_check(
        credential, config["workspace_id"]
    )
    test_results["logs_client_test"] = {
        "success": logs_success,
        "message": logs_message,
    }

    # Test Security Insights connection - credential is already checked for None above
    insights_success, insights_message = azure_security_insights_check(
        credential,
        config["subscription_id"],
        config["resource_group"],
        config["workspace_name"],
    )
    test_results["security_insights_test"] = {
        "success": insights_success,
        "message": insights_message,
    }

    return test_results


if __name__ == "__main__":
    print("Testing Azure connections...", file=sys.stderr)
    results = run_connection_tests()

    # Print results to stderr
    print("\nConnection Test Results:", file=sys.stderr)
    print("========================", file=sys.stderr)

    print("\nEnvironment Configuration:", file=sys.stderr)
    for key, value in results["environment_config"].items():
        print(f"  {key}: {value}", file=sys.stderr)

    print("\nCredential Test:", file=sys.stderr)
    print(f"  Success: {results['credential_test']['success']}", file=sys.stderr)
    print(f"  Message: {results['credential_test']['message']}", file=sys.stderr)

    print("\nLogs Client Test:", file=sys.stderr)
    print(
        f"  Success: {results['logs_client_test'].get('success', 'Not run')}",
        file=sys.stderr,
    )
    print(
        f"  Message: {results['logs_client_test'].get('message', 'Test not performed')}",
        file=sys.stderr,
    )

    print("\nSecurity Insights Test:", file=sys.stderr)
    print(
        f"  Success: {results['security_insights_test'].get('success', 'Not run')}",
        file=sys.stderr,
    )
    print(
        f"  Message: {results['security_insights_test'].get('message', 'Test not performed')}",
        file=sys.stderr,
    )


def test_connection_utilities():
    """Pytest entrypoint for connection utility checks."""
    config = get_environment_config()
    cred_success, credential, cred_message = test_azure_credential()
    assert cred_success, f"Credential check failed: {cred_message}"
    logs_success, logs_msg = azure_logs_client_check(credential, config["workspace_id"])
    assert logs_success, f"Logs client check failed: {logs_msg}"
    insights_success, insights_msg = azure_security_insights_check(
        credential,
        config["subscription_id"],
        config["resource_group"],
        config["workspace_name"],
    )
    assert insights_success, f"Security Insights check failed: {insights_msg}"
