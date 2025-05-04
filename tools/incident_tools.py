"""
Incident Tools for Microsoft Sentinel MCP Server.

This module provides tools for listing and retrieving security incidents in
Microsoft Sentinel. Implements MCPToolBase-compliant async tool classes for
integration with the MCP server.
"""

import json
from datetime import timedelta

# NOTE: Azure client initialization for all MCP tools is centralized in MCPToolBase (tools/base.py).
# All tools must use self.get_securityinsight_client, self.get_logs_client_and_workspace, etc.,
# instead of duplicating credential/client logic.

from mcp.server.fastmcp import Context, FastMCP
from tools.base import MCPToolBase
from utilities.task_manager import run_in_thread


class SentinelIncidentListTool(MCPToolBase):
    """
    Tool for listing security incidents in Microsoft Sentinel.

    Returns a list of recent incidents with summary fields.

    Supports filtering by severity and status.
    """

    name = "sentinel_incident_list"
    description = "List security incidents in Microsoft Sentinel"

    async def run(self, ctx: Context, **kwargs):
        """
        List recent security incidents in Microsoft Sentinel.

        Args:
            ctx (Context): MCP context object.
            **kwargs: Optional filters (limit, severity, status).

        Returns:
            dict: Contains 'incidents' (list), 'valid' (bool),
            'errors' (list), and optional 'message'.
        """
        logger = self.logger

        # Using centralized parameter extraction from MCPToolBase
        limit = self._extract_param(kwargs, "limit", 10)
        severity = self._extract_param(kwargs, "severity", None)
        status = self._extract_param(kwargs, "status", None)

        try:
            logs_client, workspace_id = self.get_logs_client_and_workspace(ctx)
        except Exception as e:
            logger.error("Error initializing Azure logs client: %s", e)
            return {"error": "Azure Logs client initialization failed"}
        if logs_client is None or workspace_id is None:
            return {"error": "Azure Logs client or workspace_id is not initialized"}

        try:
            query = """
            SecurityIncident
            | order by TimeGenerated desc
            """
            if severity:
                query += f"\n| where Severity =~ '{severity}'"
            if status:
                query += f"\n| where Status =~ '{status}'"
            query += f"\n| take {limit}"
            query += """
            | project
                IncidentNumber,
                Title,
                Severity,
                Status,
                CreatedTime=TimeGenerated,
                LastModifiedTime,
                IncidentUrl
            """
            response = await run_in_thread(
                logs_client.query_workspace,
                workspace_id=workspace_id,
                query=query,
                timespan=timedelta(days=30),
                name="get_recent_incidents",
            )
            if response and response.tables and len(response.tables[0].rows) > 0:
                incidents = []
                for row in response.tables[0].rows:
                    incident = {
                        "IncidentNumber": row[0],
                        "Title": row[1],
                        "Severity": row[2],
                        "Status": row[3],
                        "CreatedTime": row[4],
                        "LastModifiedTime": row[5],
                        "IncidentUrl": row[6] if len(row) > 6 else None,
                    }
                    incidents.append(incident)
                return {"incidents": incidents, "valid": True, "errors": []}

            filters = []
            if severity:
                filters.append(f"severity={severity}")
            if status:
                filters.append(f"status={status}")
            filter_text = ""
            if filters:
                filter_text = f" with filters ({', '.join(filters)})"
            logger.info("No incidents found%s in the last 30 days.", filter_text)
            return {
                "incidents": [],
                "valid": True,
                "errors": [],
                "message": f"No incidents found{filter_text} in the last 30 days.",
            }
        except Exception as e:
            logger.error("Error retrieving incidents: %s", e)
            return {
                "incidents": [],
                "valid": False,
                "errors": ["Error retrieving incidents"],
            }


class SentinelIncidentDetailsTool(MCPToolBase):
    """
    Tool for retrieving detailed information about a specific Sentinel incident.

    Returns incident details and related alerts if available.
    """

    name = "sentinel_incident_get"
    description = "Get detailed information about a specific Sentinel incident"

    async def run(self, ctx: Context, **kwargs):
        """
        Get detailed information about a specific Sentinel incident.

        Args:
            ctx (Context): MCP context object.
            **kwargs: Must include 'incident_number'.

        Returns:
            dict: Contains 'incident' (dict),
            'related_alerts' (list), 'valid' (bool), 'errors' (list).
        """
        logger = self.logger

        # Using centralized parameter extraction from MCPToolBase
        incident_number = self._extract_param(kwargs, "incident_number")
        if incident_number is None:
            return {
                "incident": None,
                "related_alerts": [],
                "valid": False,
                "errors": ["incident_number is required"],
            }

        try:
            logs_client, workspace_id = self.get_logs_client_and_workspace(ctx)
        except Exception as e:
            logger.error("Error initializing Azure logs client: %s", e)
            return {"error": "Azure Logs client initialization failed"}
        if logs_client is None or workspace_id is None:
            return {"error": "Azure Logs client or workspace_id is not initialized"}

        try:
            details_query = f"""
            SecurityIncident
            | where IncidentNumber == '{incident_number}'
            | extend AlertsCount = iif(isnull(AlertIds), 0, array_length(AlertIds))
            | extend BookmarksCount = iif(isnull(BookmarkIds), 0,
                array_length(BookmarkIds))
            | extend CommentsCount = iif(isnull(Comments), 0, array_length(Comments))
            """
            details_response = await run_in_thread(
                logs_client.query_workspace,
                workspace_id=workspace_id,
                query=details_query,
                timespan=timedelta(days=90),
                name=f"get_incident_details_{incident_number}",
            )
            if (
                not details_response
                or not details_response.tables
                or not details_response.tables[0].rows
            ):
                return {
                    "incident": None,
                    "related_alerts": [],
                    "valid": True,
                    "errors": [
                        f"No incident found for incident number: {incident_number}"
                    ],
                }
            row = details_response.tables[0].rows[0]
            columns = [
                col.name if hasattr(col, "name") else col
                for col in details_response.tables[0].columns
            ]
            incident_details = {col: row[idx] for idx, col in enumerate(columns)}
            alert_ids = incident_details.get("AlertIds")
            if isinstance(alert_ids, str):
                try:
                    alert_ids = json.loads(alert_ids)
                except Exception:
                    alert_ids = []
            result = {
                "incident": incident_details,
                "related_alerts": [],
                "valid": True,
                "errors": [],
            }
            if alert_ids and isinstance(alert_ids, list) and len(alert_ids) > 0:
                alert_id_list = ",".join([f"'{aid}'" for aid in alert_ids if aid])
                alerts_query = f"""
                SecurityAlert
                | where TimeGenerated > ago(90d)
                | where SystemAlertId in ({alert_id_list})
                | project
                    TimeGenerated,
                    AlertName,
                    AlertSeverity,
                    Description,
                    Status,
                    Entities
                | sort by TimeGenerated desc
                | take 5
                """
                alerts_response = await run_in_thread(
                    logs_client.query_workspace,
                    workspace_id=workspace_id,
                    query=alerts_query,
                    timespan=timedelta(days=90),
                    name=f"get_incident_alerts_{incident_number}",
                )
                if (
                    alerts_response
                    and alerts_response.tables
                    and alerts_response.tables[0].rows
                ):
                    for alert_row in alerts_response.tables[0].rows:
                        alert_time = alert_row[0]
                        alert_name = alert_row[1]
                        alert_severity = alert_row[2]
                        alert_description = (
                            alert_row[3] if alert_row[3] else "No description"
                        )
                        alert_status = alert_row[4]
                        alert_entities = alert_row[5]
                        result["related_alerts"].append(
                            {
                                "Time": alert_time,
                                "Name": alert_name,
                                "Severity": alert_severity,
                                "Status": alert_status,
                                "Description": alert_description,
                                "Entities": alert_entities,
                            }
                        )
            else:
                # No alert IDs associated with this incident
                result["related_alerts"] = []
            return result
        except Exception as e:
            logger.error("Error retrieving incident details: %s", e)
            return {
                "incident": None,
                "related_alerts": [],
                "valid": False,
                "errors": ["Error retrieving incident details"],
            }


def register_tools(mcp: FastMCP):
    """
    Register incident tools with the MCP server.

    Args:
        mcp (FastMCP): The MCP server instance.
    """
    SentinelIncidentListTool.register(mcp)
    SentinelIncidentDetailsTool.register(mcp)
