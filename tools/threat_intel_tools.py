"""
FILE: tools/threat_intel_tools.py
DESCRIPTION:
    Microsoft Sentinel Threat Intelligence tools.

This module provides MCP-compliant tools for listing, retrieving, and collecting metrics
for Microsoft Sentinel Threat Intelligence indicators using direct REST API calls.
"""

from mcp.server.fastmcp import Context, FastMCP
from tools.base import MCPToolBase
from utilities.task_manager import run_in_thread


class SentinelThreatIntelligenceIndicatorsListTool(MCPToolBase):
    """
    Tool to list all Sentinel Threat Intelligence indicators.

    Returns:
        dict: {
            'indicators': list,  # List of indicators as returned by the API
            'count': int,        # Number of indicators returned
            'valid': bool,       # True if successful
            'error': str (optional)
        }
    """

    name = "sentinel_ti_indicators_list"
    description = "List all Sentinel threat intelligence indicators"

    async def run(self, ctx: Context, **kwargs):
        """
        List all Sentinel Threat Intelligence indicators in the workspace.

        Args:
            ctx (Context): The MCP tool context.
            **kwargs: Not used.

        Returns:
            dict: Results as described in the class docstring.
        """
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)
        valid = self.validate_azure_context(
            True, workspace_name, resource_group, subscription_id, self.logger
        )
        if not valid:
            return {"error": "Missing required Azure context", "valid": False}
        try:
            url = (
                f"https://management.azure.com/subscriptions/{subscription_id}/"
                f"resourceGroups/{resource_group}/providers/Microsoft.OperationalInsights/"
                f"workspaces/{workspace_name}/providers/Microsoft.SecurityInsights/"
                f"threatIntelligence/main/indicators?api-version=2024-01-01-preview"
            )
            response = await self.call_api(ctx, "GET", url, name="list_ti_indicators")
            indicators = response.get("value", [])
            result = []
            for indicator in indicators:
                info = {
                    "id": indicator.get("id"),
                    "name": indicator.get("name"),
                    "type": indicator.get("type"),
                }
                props = indicator.get("properties", {})
                info["displayName"] = props.get("displayName")
                info["patternType"] = props.get("patternType")
                info["pattern"] = props.get("pattern")
                info["source"] = props.get("source")
                info["created"] = props.get("createdTimeUtc")
                info["confidence"] = props.get("confidence")
                info["threatTypes"] = props.get("threatTypes")
                info["validFrom"] = props.get("validFrom")
                info["validUntil"] = props.get("validUntil")
                info["description"] = props.get("description")
                result.append(info)
            return {"indicators": result, "count": len(result), "valid": True}
        except Exception as e:
            self.logger.error("Error retrieving threat intelligence indicators: %s", e)
            return {
                "error": "Error retrieving threat intelligence indicators: %s" % e,
                "valid": False,
            }


class SentinelIPGeodataGetTool(MCPToolBase):
    """
    Tool to get geolocation data for an IP address.

    Returns:
        dict: {
            'geodata': dict,   # Geolocation data as returned by the API
            'valid': bool,     # True if successful
            'error': str (optional)
        }
    """

    name = "sentinel_ip_geodata_get"
    description = "Get geolocation data for an IP address"

    async def run(self, ctx: Context, **kwargs):
        """
        Get geolocation data for an IP address.

        Args:
            ctx (Context): The MCP tool context.
            **kwargs: IP address as 'ip' parameter.

        Returns:
            dict: Results as described in the class docstring.
        """

        # Extract parameters
        # Extract ip parameter using the centralized parameter extraction from MCPToolBase
        ip = self._extract_param(kwargs, "ip")

        if not ip:
            return {"error": "ip parameter is required", "valid": False}

        # Get Azure context
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)

        # Get security insights client
        client = None
        try:
            client = self.get_securityinsight_client(subscription_id)
        except Exception as e:
            self.logger.error("Error initializing Azure SecurityInsights client: %s", e)
            return {
                "error": (
                    f"Azure SecurityInsights client initialization failed: {str(e)}"
                ),
                "valid": False,
            }

        if client is None:
            return {
                "error": "Azure SecurityInsights client is not initialized",
                "valid": False,
            }

        # Validate Azure context
        valid = self.validate_azure_context(
            client is not None,
            workspace_name,
            resource_group,
            subscription_id,
            self.logger,
        )
        if not valid:
            return {
                "error": "Missing required Azure context or SDK components",
                "valid": False,
            }

        try:
            # Get geolocation data for the IP address
            # Based on SDK testing, ip_geodata.get() doesn't accept workspace_name
            geodata = await run_in_thread(
                client.ip_geodata.get,
                resource_group_name=resource_group,
                ip_address=ip,
            )

            # Process geodata result
            # Return the full geodata object
            geodata_dict = {}
            if hasattr(geodata, "as_dict"):
                geodata_dict = geodata.as_dict()
            else:
                # If as_dict() is not available, try to convert to dict directly
                geodata_dict = dict(geodata) if geodata else {}

            # Ensure we have at least the IP in the response
            if not geodata_dict or not geodata_dict.get("ip"):
                geodata_dict["ip"] = ip

            return {
                "geodata": geodata_dict,
                "valid": True,
            }
        except Exception as e:
            self.logger.error("Error retrieving IP geodata for %s: %s", ip, e)
            return {
                "error": f"Error retrieving IP geodata for {ip}: {str(e)}",
                "valid": False,
            }


class SentinelDomainWhoisGetTool(MCPToolBase):
    """
    Tool to get WHOIS information for a domain.

    Returns:
        dict: {
            'whois': dict,     # WHOIS data as returned by the API
            'valid': bool,     # True if successful
            'error': str (optional)
        }
    """

    name = "sentinel_domain_whois_get"
    description = "Get WHOIS information for a domain"

    async def run(self, ctx: Context, **kwargs):
        """
        Get WHOIS information for a domain.

        Args:
            ctx (Context): The MCP tool context.
            **kwargs: Domain as 'domain' parameter.

        Returns:
            dict: Results as described in the class docstring.
        """

        # Extract parameters
        domain = None
        if "domain" in kwargs:
            domain = kwargs["domain"]
        elif "kwargs" in kwargs and isinstance(kwargs["kwargs"], dict):
            domain = kwargs["kwargs"].get("domain")

        if not domain:
            return {"error": "domain parameter is required", "valid": False}

        # Get Azure context
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)

        # Get security insights client
        client = None
        try:
            client = self.get_securityinsight_client(subscription_id)
        except Exception as e:
            self.logger.error("Error initializing Azure SecurityInsights client: %s", e)
            return {
                "error": (
                    f"Azure SecurityInsights client initialization failed: {str(e)}"
                ),
                "valid": False,
            }

        if client is None:
            return {
                "error": "Azure SecurityInsights client is not initialized",
                "valid": False,
            }

        # Validate Azure context
        valid = self.validate_azure_context(
            client is not None,
            workspace_name,
            resource_group,
            subscription_id,
            self.logger,
        )
        if not valid:
            return {
                "error": "Missing required Azure context or SDK components",
                "valid": False,
            }

        try:
            # Get WHOIS data for the domain
            # Based on SDK testing, domain_whois.get() doesn't accept workspace_name
            whois_data = await run_in_thread(
                client.domain_whois.get,
                resource_group_name=resource_group,
                domain=domain,
            )

            # Process WHOIS data result
            # Return the full WHOIS data object
            whois_dict = {}
            if hasattr(whois_data, "as_dict"):
                whois_dict = whois_data.as_dict()
            else:
                # If as_dict() is not available, try to convert to dict directly
                whois_dict = dict(whois_data) if whois_data else {}

            # Ensure we have at least the domain in the response
            if not whois_dict or not whois_dict.get("domain"):
                whois_dict["domain"] = domain

            return {
                "whois": whois_dict,
                "valid": True,
            }
        except Exception as e:
            self.logger.error("Error retrieving WHOIS data for %s: %s", domain, e)
            return {
                "error": f"Error retrieving WHOIS data for {domain}: {str(e)}",
                "valid": False,
            }


class SentinelThreatIntelligenceIndicatorGetTool(MCPToolBase):
    """
    Tool to get a specific Sentinel Threat Intelligence indicator.

    Returns:
        dict: {
            'indicator': dict,  # Indicator details as returned by the API
            'valid': bool,      # True if successful
            'error': str (optional)
        }
    """

    name = "sentinel_ti_indicator_get"
    description = "Get a specific Sentinel threat intelligence indicator"

    async def run(self, ctx: Context, **kwargs):
        """
        Get a specific Sentinel Threat Intelligence indicator.

        Args:
            ctx (Context): The MCP tool context.
            **kwargs: Indicator name as 'indicator_name' parameter.

        Returns:
            dict: Results as described in the class docstring.
        """
        indicator_name = self._extract_param(kwargs, "indicator_name")
        if not indicator_name:
            return {"error": "indicator_name parameter is required", "valid": False}
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)
        valid = self.validate_azure_context(
            True, workspace_name, resource_group, subscription_id, self.logger
        )
        if not valid:
            return {"error": "Missing required Azure context", "valid": False}
        try:
            url = (
                f"https://management.azure.com/subscriptions/{subscription_id}/"
                f"resourceGroups/{resource_group}/providers/Microsoft.OperationalInsights/"
                f"workspaces/{workspace_name}/providers/Microsoft.SecurityInsights/"
                f"threatIntelligence/main/indicators/{indicator_name}?"
                f"api-version=2024-01-01-preview"
            )
            indicator = await self.call_api(ctx, "GET", url, name="get_ti_indicator")
            if not indicator:
                return {
                    "error": "Threat intelligence indicator '%s' not found"
                    % indicator_name,
                    "valid": False,
                }
            props = indicator.get("properties", {})
            details = {
                "id": indicator.get("id"),
                "name": indicator.get("name"),
                "type": indicator.get("type"),
                "displayName": props.get("displayName"),
                "patternType": props.get("patternType"),
                "pattern": props.get("pattern"),
                "source": props.get("source"),
                "created": props.get("createdTimeUtc"),
                "confidence": props.get("confidence"),
                "threatTypes": props.get("threatTypes"),
                "validFrom": props.get("validFrom"),
                "validUntil": props.get("validUntil"),
                "description": props.get("description"),
                "killChainPhases": props.get("killChainPhases"),
                "labels": props.get("labels"),
            }
            return {"indicator": details, "valid": True}
        except Exception as e:
            self.logger.error(
                "Error retrieving threat intelligence indicator %s: %s",
                indicator_name,
                e,
            )
            return {
                "error": "Error retrieving threat intelligence indicator %s: %s"
                % (indicator_name, e),
                "valid": False,
            }


class SentinelThreatIntelligenceIndicatorMetricsCollectTool(MCPToolBase):
    """
    Tool to collect metrics for Sentinel Threat Intelligence indicators.

    Returns:
        dict: {
            'metrics': dict,   # Metrics details as returned by the API
            'valid': bool,     # True if successful
            'error': str (optional)
        }
    """

    name = "sentinel_ti_indicator_metrics_collect"
    description = "Collect metrics for Sentinel threat intelligence indicators"

    async def run(self, ctx: Context, **kwargs):
        """
        Collect metrics for Sentinel Threat Intelligence indicators in the workspace.

        Args:
            ctx (Context): The MCP tool context.
            **kwargs: Not used.

        Returns:
            dict: Results as described in the class docstring.
        """
        workspace_name, resource_group, subscription_id = self.get_azure_context(ctx)
        valid = self.validate_azure_context(
            True, workspace_name, resource_group, subscription_id, self.logger
        )
        if not valid:
            return {"error": "Missing required Azure context", "valid": False}
        try:
            url = (
                f"https://management.azure.com/subscriptions/{subscription_id}/"
                f"resourceGroups/{resource_group}/providers/Microsoft.OperationalInsights/"
                f"workspaces/{workspace_name}/providers/Microsoft.SecurityInsights/"
                f"threatIntelligence/main/metrics?api-version=2024-01-01-preview"
            )
            metrics = await self.call_api(
                ctx, "GET", url, name="list_ti_indicator_metrics"
            )
            return {"metrics": metrics, "valid": True}
        except Exception as e:
            self.logger.error("Error collecting threat intelligence metrics: %s", e)
            return {
                "error": "Error collecting threat intelligence metrics: %s" % e,
                "valid": False,
            }


def register_tools(mcp: FastMCP):
    """
    Register all Sentinel Threat Intelligence tools with the given MCP instance.

    Args:
        mcp (FastMCP): The MCP instance to register tools with.
    """
    SentinelThreatIntelligenceIndicatorGetTool.register(mcp)
    SentinelThreatIntelligenceIndicatorMetricsCollectTool.register(mcp)
    SentinelIPGeodataGetTool.register(mcp)
    SentinelDomainWhoisGetTool.register(mcp)
