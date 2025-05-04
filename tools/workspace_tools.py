"""
MCP-compliant tools for retrieving and managing Microsoft Sentinel workspace
information.

This module provides tools for querying Sentinel workspace details, source controls,
metadata, and ML analytics settings. All tools are implemented using MCPToolBase and
are compatible with both MCP server and direct invocation.
"""

from mcp.server.fastmcp import Context

from tools.base import MCPToolBase
from utilities.task_manager import run_in_thread


class SentinelWorkspaceGetTool(MCPToolBase):
    """
    Tool for retrieving detailed information about the current Sentinel Log Analytics
    workspace.
    """

    name = "sentinel_workspace_get"
    description = "Get workspace information (refactored, MCP-compliant)"

    async def run(self, ctx: Context, **kwargs):
        """
        Get detailed information about the current Sentinel Log Analytics workspace.

        Returns:
            dict: {
                'workspace_name': str,
                'resource_group': str,
                'subscription_id': str,
                'properties': dict,  # workspace properties or empty if unavailable
                'additional_information': list[str],
                'error': str (optional, present only if an error occurs)
            }
        Output Fields:
            - workspace_name: The name of the Sentinel Log Analytics workspace.
            - resource_group: The Azure resource group for the workspace.
            - subscription_id: The Azure subscription ID.
            - properties: Detailed properties about the workspace (location, SKU,
              retention, etc.).
            - additional_information: Guidance on related tools and next steps.
            - error: Error message if an error occurs (optional).
        Error cases will always include an 'error' key for testability.
        Parameters are extracted from both kwargs and kwargs['kwargs'] for MCP
        compatibility.

        Azure Context Fallback:
            - Supports both MCP server and direct invocation.
            - If ctx.request_context is not available, falls back to environment
              variables for Azure context:
              AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET,
              AZURE_SUBSCRIPTION_ID, AZURE_RESOURCE_GROUP, AZURE_WORKSPACE_NAME.
        """
        logger = self.logger
        # Extract parameters from both kwargs and kwargs['kwargs'] (future-proof,
        # even if unused)
        params = dict(kwargs)
        if "kwargs" in kwargs and isinstance(kwargs["kwargs"], dict):
            params.update(kwargs["kwargs"])
        # Extract context (assume .env is loaded and Context is configured)
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)
        result = {
            "workspace_name": workspace_name,
            "resource_group": resource_group,
            "subscription_id": subscription_id,
            "properties": {},
            "additional_information": [
                "For data connector details, use the `sentinel_connectors_list` tool.",
                "For analytics rules details, use the `list_analytics_rules` tool.",
            ],
        }

        try:
            client = self.get_loganalytics_client(subscription_id)
            ws = await run_in_thread(
                client.workspaces.get, resource_group, workspace_name
            )
            result["properties"] = {
                "location": ws.location,
                "sku": getattr(ws.sku, "name", None),
                "sku_description": getattr(ws.sku, "description", None),
                "last_sku_update": str(getattr(ws, "last_sku_update", "")),
                "retention_period_days": ws.retention_in_days,
                "daily_quota_gb": getattr(ws, "daily_quota_gb", None),
                "quota_reset_time": str(getattr(ws, "quota_reset_time", "")),
                "ingestion_status": getattr(ws, "ingestion_status", None),
                "public_network_access_ingestion": getattr(
                    ws, "public_network_access_for_ingestion", None
                ),
                "public_network_access_query": getattr(
                    ws, "public_network_access_for_query", None
                ),
                "created": str(getattr(ws, "created_date", "")),
                "last_modified": str(getattr(ws, "modified_date", "")),
                "features": getattr(ws, "features", {}),
            }
        except Exception as ex:
            error_msg = "Error retrieving workspace info: %s" % ex
            logger.exception("%s", error_msg)
            result["error"] = error_msg
        return result


class SentinelSourceControlsListTool(MCPToolBase):
    """
    Tool for listing all Sentinel source controls in the current workspace.
    """

    name = "sentinel_source_controls_list"
    description = "List all Sentinel source controls in the current workspace."

    async def run(self, ctx: Context, **kwargs):
        """
        List all source controls in the current Sentinel workspace.

        Parameters:
            None required. (Context is extracted from MCP or environment.)
        Returns:
            dict: {
                'source_controls': list[dict],
                'valid': bool,
                'errors': list[str],
                'error': str (optional, present only if an error occurs)
            }
        Output Fields:
            - source_controls: List of source control objects (id, name, repo, etc.)
            - valid: True if successful, False otherwise
            - errors: List of error messages (empty if none)
            - error: Error message if an error occurs (optional)
        Error cases will always include an 'error' key for testability.
        """
        logger = self.logger
        params = dict(kwargs)
        if "kwargs" in kwargs and isinstance(kwargs["kwargs"], dict):
            params.update(kwargs["kwargs"])
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)
        result = {
            "source_controls": [],
            "valid": False,
            "errors": [],
        }
        try:
            client = self.get_securityinsight_client(subscription_id)
            controls = client.source_controls.list(resource_group, workspace_name)
            controls_list = []
            for ctrl in controls:
                controls_list.append(
                    {
                        "id": getattr(ctrl, "id", None),
                        "name": getattr(ctrl, "name", None),
                        "repo_type": getattr(ctrl, "repo_type", None),
                        "repo_url": getattr(ctrl, "repo_url", None),
                        "description": getattr(ctrl, "description", None),
                        "content_types": getattr(ctrl, "content_types", None),
                        "created_time_utc": str(getattr(ctrl, "created_time_utc", "")),
                        "last_modified_time_utc": str(
                            getattr(ctrl, "last_modified_time_utc", "")
                        ),
                    }
                )
            result["source_controls"] = controls_list
            result["valid"] = True
        except Exception as ex:
            error_msg = "Error listing source controls: %s" % ex
            logger.exception("%s", error_msg)
            result["error"] = error_msg
            result["errors"].append(error_msg)
        return result


class SentinelSourceControlGetTool(MCPToolBase):
    """
    Tool for retrieving details for a specific Sentinel source control by ID.
    """

    name = "sentinel_source_control_get"
    description = "Get details for a specific Sentinel source control by ID."

    async def run(self, ctx: Context, **kwargs):
        """
        Get details for a specific source control by ID.

        Parameters:
            source_control_id (str, required): The ID of the source control to
                retrieve.
        Returns:
            dict: {
                'source_control': dict,
                'valid': bool,
                'errors': list[str],
                'error': str (optional, present only if an error occurs)
            }
        Output Fields:
            - source_control: Source control object (id, name, repo, etc.)
            - valid: True if successful, False otherwise
            - errors: List of error messages (empty if none)
            - error: Error message if an error occurs (optional)
        Error cases will always include an 'error' key for testability.
        """
        logger = self.logger
        # Extract parameters using the base class method
        source_control_id = self._extract_param(kwargs, "source_control_id")
        result = {
            "source_control": {},
            "valid": False,
            "errors": [],
        }
        if not source_control_id:
            error_msg = "Missing required parameter: source_control_id"
            logger.error("%s", error_msg)
            result["error"] = error_msg
            result["errors"].append(error_msg)
            return result
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)
        try:
            client = self.get_securityinsight_client(subscription_id)
            ctrl = client.source_controls.get(
                resource_group, workspace_name, source_control_id
            )
            result["source_control"] = {
                "id": getattr(ctrl, "id", None),
                "name": getattr(ctrl, "name", None),
                "repo_type": getattr(ctrl, "repo_type", None),
                "repo_url": getattr(ctrl, "repo_url", None),
                "description": getattr(ctrl, "description", None),
                "content_types": getattr(ctrl, "content_types", None),
                "created_time_utc": str(getattr(ctrl, "created_time_utc", "")),
                "last_modified_time_utc": str(
                    getattr(ctrl, "last_modified_time_utc", "")
                ),
            }
            result["valid"] = True
        except Exception as ex:
            error_msg = "Error retrieving source control: %s" % ex
            logger.exception("%s", error_msg)
            result["error"] = error_msg
            result["errors"].append(error_msg)
        return result


class SentinelMetadataListTool(MCPToolBase):
    """
    Tool for listing all Sentinel metadata in the current workspace.
    """

    name = "sentinel_metadata_list"
    description = "List all Sentinel metadata in the current workspace."

    async def run(self, ctx: Context, **kwargs):
        """
        List all metadata in the current Sentinel workspace.

        Parameters:
            None required. (Context is extracted from MCP or environment.)
        Returns:
            dict: {
                'metadata': list[dict],
                'valid': bool,
                'errors': list[str],
                'error': str (optional, present only if an error occurs)
            }
        Output Fields:
            - metadata: List of metadata objects (id, name, kind, etc.)
            - valid: True if successful, False otherwise
            - errors: List of error messages (empty if none)
            - error: Error message if an error occurs (optional)
        Error cases will always include an 'error' key for testability.
        """
        logger = self.logger
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)
        result = {
            "metadata": [],
            "valid": False,
            "errors": [],
        }
        try:
            client = self.get_securityinsight_client(subscription_id)
            metadata_objs = client.metadata.list(resource_group, workspace_name)
            metadata_list = []
            for meta in metadata_objs:
                metadata_list.append(
                    {
                        "id": getattr(meta, "id", None),
                        "name": getattr(meta, "name", None),
                        "kind": getattr(meta, "kind", None),
                        "content_id": getattr(meta, "content_id", None),
                        "version": getattr(meta, "version", None),
                        "parent_id": getattr(meta, "parent_id", None),
                        "author": getattr(meta, "author", None),
                        "source": getattr(meta, "source", None),
                        "support": getattr(meta, "support", None),
                        "categories": getattr(meta, "categories", None),
                        "dependencies": getattr(meta, "dependencies", None),
                        "created": str(getattr(meta, "created", "")),
                        "last_modified": str(getattr(meta, "last_modified", "")),
                    }
                )
            result["metadata"] = metadata_list
            result["valid"] = True
        except Exception as ex:
            error_msg = "Error listing metadata: %s" % ex
            logger.exception("%s", error_msg)
            result["error"] = error_msg
            result["errors"].append(error_msg)
        return result


class SentinelMetadataGetTool(MCPToolBase):
    """
    Tool for retrieving details for specific Sentinel metadata by ID.
    """

    name = "sentinel_metadata_get"
    description = "Get details for specific Sentinel metadata by ID."

    async def run(self, ctx: Context, **kwargs):
        """
        Get details for specific metadata by ID.

        Parameters:
            metadata_id (str, required): The ID of the metadata object to retrieve.
        Returns:
            dict: {
                'metadata': dict,
                'valid': bool,
                'errors': list[str],
                'error': str (optional, present only if an error occurs)
            }
        Output Fields:
            - metadata: Metadata object (id, name, kind, etc.)
            - valid: True if successful, False otherwise
            - errors: List of error messages (empty if none)
            - error: Error message if an error occurs (optional)
        Error cases will always include an 'error' key for testability.
        """
        logger = self.logger
        # Accept both 'metadata_id' and 'id' as input keys using the base class method
        metadata_id = self._extract_param(kwargs, "metadata_id") or self._extract_param(
            kwargs, "id"
        )
        logger.debug("SentinelMetadataGetTool metadata_id: %r", metadata_id)
        # If a full ARM resource ID is provided, extract the short name (last segment)
        if metadata_id and "/" in metadata_id:
            metadata_id = metadata_id.rstrip("/").split("/")[-1]
        result = {
            "metadata": {},
            "valid": False,
            "errors": [],
        }
        if not metadata_id:
            error_msg = (
                "Missing required parameter: metadata_id or id. Provide either "
                "the short name or the full ARM resource ID."
            )
            logger.error("%s", error_msg)
            result["error"] = error_msg
            result["errors"].append(error_msg)
            return result
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)
        try:
            client = self.get_securityinsight_client(subscription_id)
            meta = client.metadata.get(resource_group, workspace_name, metadata_id)

            def _serialize_model(obj):
                if hasattr(obj, "as_dict"):
                    return obj.as_dict()
                elif hasattr(obj, "__dict__"):
                    # fallback, filter out private attributes
                    return {
                        k: v for k, v in obj.__dict__.items() if not k.startswith("_")
                    }
                elif obj is None:
                    return None
                else:
                    return str(obj)

            result["metadata"] = {
                "id": getattr(meta, "id", None),
                "name": getattr(meta, "name", None),
                "kind": getattr(meta, "kind", None),
                "content_id": getattr(meta, "content_id", None),
                "version": getattr(meta, "version", None),
                "parent_id": getattr(meta, "parent_id", None),
                "author": _serialize_model(getattr(meta, "author", None)),
                "source": _serialize_model(getattr(meta, "source", None)),
                "support": _serialize_model(getattr(meta, "support", None)),
                "categories": getattr(meta, "categories", None),
                "dependencies": getattr(meta, "dependencies", None),
                "created": str(getattr(meta, "created", "")),
                "last_modified": str(getattr(meta, "last_modified", "")),
            }
            result["valid"] = True
        except Exception as ex:
            error_msg = f"Error retrieving metadata: {ex}"
            logger.exception(error_msg)
            result["error"] = error_msg
            result["errors"].append(error_msg)
        return result


class SentinelMLAnalyticsSettingsListTool(MCPToolBase):
    """Tool for listing all Sentinel ML analytics settings in the current workspace."""

    name = "sentinel_ml_analytics_settings_list"
    description = "List all Sentinel ML analytics settings in the current workspace."

    async def run(self, ctx: Context, **kwargs):
        """
        List all ML analytics settings in the current Sentinel workspace.
        Returns MCP-compliant dict with 'settings', 'valid', 'errors', and 'error'.
        """
        logger = self.logger
        result = {"settings": [], "valid": False, "errors": []}
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)
        if not (workspace_name and resource_group and subscription_id):
            error_msg = (
                "Missing required Azure context (workspace_name, resource_group, "
                "subscription_id)."
            )
            logger.error(error_msg)
            result["error"] = error_msg
            result["errors"].append(error_msg)
            return result
        try:
            client = self.get_securityinsight_client(subscription_id)
            # Use the preview API version for ML Analytics support
            ml_settings_paged = client.security_ml_analytics_settings.list(
                resource_group, workspace_name
            )
            settings = []
            for s in ml_settings_paged:
                s_dict = s.as_dict() if hasattr(s, "as_dict") else dict(s)
                settings.append(
                    {
                        "id": s_dict.get("id"),
                        "name": s_dict.get("name"),
                        "description": s_dict.get("description"),
                        "enabled": s_dict.get("enabled"),
                    }
                )
            result["settings"] = settings
            result["valid"] = True
        except Exception as ex:
            error_msg = f"Error listing ML analytics settings: {ex}"
            logger.exception(error_msg)
            result["error"] = error_msg
            result["errors"].append(error_msg)
        return result


class SentinelMLAnalyticsSettingGetTool(MCPToolBase):
    """
    Tool for retrieving a specific Sentinel ML analytics setting by name.
    """

    name = "sentinel_ml_analytics_setting_get"
    description = "Get a specific Sentinel ML analytics setting by name."

    async def run(self, ctx: Context, **kwargs):
        """
        Get a specific ML analytics setting by name.
        Parameters:
            setting_name (str, required): The name of the ML analytics setting.
        Returns MCP-compliant dict with 'setting', 'valid', 'errors', and 'error'.
        """
        logger = self.logger
        # Extract parameters using the base class method
        setting_name = self._extract_param(kwargs, "setting_name")
        result = {"setting": {}, "valid": False, "errors": []}
        if not setting_name:
            error_msg = "Missing required parameter: setting_name"
            logger.error(error_msg)
            result["error"] = error_msg
            result["errors"].append(error_msg)
            return result
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)
        if not (workspace_name and resource_group and subscription_id):
            error_msg = (
                "Missing required Azure context (workspace_name, resource_group, "
                "subscription_id)."
            )
            logger.error(error_msg)
            result["error"] = error_msg
            result["errors"].append(error_msg)
            return result
        try:
            client = self.get_securityinsight_client(subscription_id)
            s = client.security_ml_analytics_settings.get(
                resource_group, workspace_name, setting_name
            )
            s_dict = s.as_dict() if hasattr(s, "as_dict") else dict(s)
            enriched = {
                "id": s_dict.get("id"),
                "name": s_dict.get("name"),
                "kind": s_dict.get("kind"),
                "etag": s_dict.get("etag"),
                "type": s_dict.get("type"),
                "description": s_dict.get("description"),
                "display_name": s_dict.get("display_name"),
                "enabled": s_dict.get("enabled"),
                "last_modified_utc": s_dict.get("last_modified_utc"),
                "required_data_connectors": s_dict.get("required_data_connectors"),
                "tactics": s_dict.get("tactics"),
                "techniques": s_dict.get("techniques"),
                "anomaly_version": s_dict.get("anomaly_version"),
                "customizable_observations": s_dict.get("customizable_observations"),
                "frequency": s_dict.get("frequency"),
                "settings_status": s_dict.get("settings_status"),
                "is_default_settings": s_dict.get("is_default_settings"),
                "anomaly_settings_version": s_dict.get("anomaly_settings_version"),
                "settings_definition_id": s_dict.get("settings_definition_id"),
                "properties": None,
                "referenced_by_analytic_rules": [],
            }
            # Parse 'properties' if present
            props = getattr(s, "properties", None)
            if props is not None:
                if hasattr(props, "as_dict"):
                    enriched["properties"] = props.as_dict()
                elif isinstance(props, dict):
                    enriched["properties"] = props
                else:
                    enriched["properties"] = {"raw": str(props)}
            # Attempt to find analytic rules that reference this ML setting
            analytic_rules = []
            for rule in client.alert_rules.list(resource_group, workspace_name):
                rule_dict = rule.as_dict() if hasattr(rule, "as_dict") else dict(rule)
                found_ref = False
                for val in rule_dict.values():
                    if isinstance(val, str) and (
                        enriched["name"] in val or enriched["id"] in val
                    ):
                        found_ref = True
                    elif isinstance(val, dict):
                        if any(
                            enriched["name"] in str(v) or enriched["id"] in str(v)
                            for v in val.values()
                        ):
                            found_ref = True
                    elif isinstance(val, list):
                        if any(
                            enriched["name"] in str(v) or enriched["id"] in str(v)
                            for v in val
                        ):
                            found_ref = True
                if found_ref:
                    analytic_rules.append(
                        {
                            "rule_name": rule_dict.get(
                                "display_name", rule_dict.get("name")
                            ),
                            "rule_id": rule_dict.get("id"),
                            "rule_kind": rule_dict.get("kind"),
                        }
                    )
            enriched["referenced_by_analytic_rules"] = analytic_rules
            result["setting"] = enriched
            result["valid"] = True
        except Exception as ex:
            error_msg = f"Error retrieving ML analytics setting: {ex}"
            logger.exception(error_msg)
            result["error"] = error_msg
            result["errors"].append(error_msg)
        return result


def register_tools(mcp):
    """Register all Sentinel workspace-related tools with the MCP server instance."""
    SentinelWorkspaceGetTool.register(mcp)
    SentinelSourceControlsListTool.register(mcp)
    SentinelSourceControlGetTool.register(mcp)
    SentinelMetadataListTool.register(mcp)
    SentinelMetadataGetTool.register(mcp)
    SentinelMLAnalyticsSettingsListTool.register(mcp)
    SentinelMLAnalyticsSettingGetTool.register(mcp)
