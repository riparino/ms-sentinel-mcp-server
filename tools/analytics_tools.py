"""
Analytics Tools for Microsoft Sentinel MCP Server (MCPToolBase-compliant).

This module implements MCP-compliant tools for listing, retrieving, and summarizing
Microsoft Sentinel analytics rules and templates. All classes inherit from MCPToolBase.

Tools include:
- sentinel_analytics_rule_list
- sentinel_analytics_rule_get
- sentinel_analytics_rule_templates_list
- sentinel_analytics_rule_template_get
- sentinel_analytics_rules_count_by_tactic
- sentinel_analytics_rule_templates_count_by_tactic
- sentinel_analytics_rules_count_by_technique
- sentinel_analytics_rule_templates_count_by_technique

All Azure workspace/resource identifiers are anonymized in documentation.
"""

from typing import Dict

from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
from mcp.server.fastmcp import Context

from tools.base import MCPToolBase


class SentinelAnalyticsRuleListTool(MCPToolBase):
    """
    Tool to list all Microsoft Sentinel analytics rules with key fields.

    Returns a list of dictionaries, each containing rule summary fields or error
    details.
    """

    name = "sentinel_analytics_rule_list"
    description = "List all analytics rules with key fields"

    async def run(self, ctx: Context, **kwargs):
        """
        List all analytics rules with key fields.

        Supports both MCP server and direct (test) invocation.

        Args:
            ctx (Context): MCP context object.
            **kwargs: Additional keyword arguments (unused).

        Returns:
            list[dict]: List of rule summaries or error details.
        """
        logger = self.logger
        workspace, resource_group, subscription_id = self.get_azure_context(ctx)
        if not (workspace and resource_group and subscription_id):
            logger.error("Missing Azure Sentinel context for analytics rule listing.")
            return [{"error": "Missing Azure Sentinel context."}]
        rule_summaries = []
        errors = []
        try:
            client = self.get_securityinsight_client(subscription_id)
            rules = client.alert_rules.list(
                resource_group_name=resource_group,
                workspace_name=workspace,
            )
        except (HttpResponseError, ResourceNotFoundError) as e:
            logger.error("Azure SDK error listing analytics rules: %s", e)
            return [{"error": f"Azure SDK error: {str(e)}"}]
        except Exception as e:
            logger.error("Unexpected error listing analytics rules: %s", e)
            return [{"error": f"Unexpected error: {str(e)}"}]

        logged_first = False
        for rule in rules:
            try:
                if not hasattr(rule, "name") or not hasattr(rule, "id"):
                    raise ValueError("Rule object missing required attributes")
                name = getattr(rule, "name", None)
                id_ = getattr(rule, "id", None)
                kind = getattr(rule, "kind", None)
                display_name = getattr(rule, "display_name", None) or getattr(
                    rule, "displayName", None
                )
                severity = getattr(rule, "severity", None)
                enabled = getattr(rule, "enabled", None)
                summary = {
                    "id": id_,
                    "name": name,
                    "kind": kind,
                    "displayName": display_name,
                    "severity": severity,
                    "enabled": enabled,
                }
                rule_summaries.append(summary)
                if not logged_first:
                    logger.debug("First rule object: %s", rule)
                    logger.debug(
                        "First rule as_dict: %s",
                        getattr(rule, "as_dict", lambda: None)(),
                    )
                    logged_first = True
            except Exception as rule_exc:
                logger.warning("Failed to process rule: %s", rule_exc)
                errors.append(str(rule_exc))
                continue
        if errors:
            rule_summaries.append(
                {
                    "warning": f"{len(errors)} rules could not be processed",
                    "details": errors,
                }
            )
        logger.info(
            "Retrieved %d analytics rule summaries (with %d errors).",
            len(rule_summaries),
            len(errors),
        )
        return rule_summaries


class SentinelAnalyticsRuleGetTool(MCPToolBase):
    name = "sentinel_analytics_rule_get"
    description = "Get details for a specific analytics rule"

    async def run(self, ctx: Context, rule_name: str = None, **kwargs):
        """
        Get details for a specific analytics rule.
        Supports both MCP server and direct (test) invocation.
        Returns a dict with summary fields and full rule details, or error details.
        """
        logger = self.logger
        # Robust parameter extraction: support both direct and nested kwargs
        if rule_name is None:
            rule_name = self._extract_param(kwargs, "rule_name")
        workspace, resource_group, subscription_id = self.get_azure_context(ctx)
        if not (workspace and resource_group and subscription_id):
            logger.error("Missing Azure Sentinel context for analytics rule retrieval.")
            return {"error": "Missing Azure Sentinel context."}
        if not rule_name:
            logger.error("No rule_name provided for analytics rule retrieval.")
            return {"error": "No rule_name provided."}
        try:
            client = self.get_securityinsight_client(subscription_id)
            rule = client.alert_rules.get(
                resource_group_name=resource_group,
                workspace_name=workspace,
                rule_id=rule_name,
            )
            if hasattr(rule, "as_dict"):
                rule_dict = rule.as_dict()
            else:
                rule_dict = dict(rule)
            display_name = rule_dict.get("display_name") or rule_dict.get("displayName")
            severity = rule_dict.get("severity")
            enabled = rule_dict.get("enabled")
            summary = {
                "id": rule_dict.get("id"),
                "name": rule_dict.get("name"),
                "kind": rule_dict.get("kind"),
                "displayName": display_name,
                "severity": severity,
                "enabled": enabled,
            }
            summary["_full"] = rule_dict
            return summary
        except ResourceNotFoundError as e:
            logger.error("Analytics rule not found: %s", e)
            return {"error": "Analytics rule not found", "details": str(e)}
        except HttpResponseError as e:
            logger.error("HTTP error retrieving analytics rule: %s", e)
            return {"error": "HTTP error", "details": str(e)}
        except Exception as e:
            logger.error(
                "Unexpected error retrieving analytics rule '%s': %s", rule_name, e
            )
            return {"error": "Unexpected error", "details": str(e)}


class SentinelAnalyticsRuleTemplatesListTool(MCPToolBase):
    """
    List all Sentinel analytics rule templates in the current workspace.
    Returns a list of template summaries or error details.
    """

    name = "sentinel_analytics_rule_templates_list"
    description = "List all Sentinel analytics rule templates"

    async def run(self, ctx: Context, **kwargs):
        """
        List all analytics rule templates in the current Sentinel workspace.
        Returns a list of dicts, each containing template summary fields, or
        error details.

        Parameters:
            ctx (Context): MCP context object.
            **kwargs: No parameters required.

        Returns:
            list[dict]: List of template summaries or error dicts.
        """
        logger = self.logger
        workspace, resource_group, subscription_id = self.get_azure_context(ctx)
        if not (workspace and resource_group and subscription_id):
            logger.error(
                "Missing Azure Sentinel context for analytics rule templates list."
            )
            return [{"error": "Missing Azure Sentinel context."}]
        try:
            client = self.get_securityinsight_client(subscription_id)
            templates = client.alert_rule_templates.list(resource_group, workspace)
        except Exception as e:
            logger.error("Error listing analytics rule templates: %s", e)
            # pylint: disable=consider-using-f-string
            return [{"error": f"Error listing analytics rule templates: {str(e)}"}]
        results = []
        for template in templates:
            try:
                template_dict = (
                    template.as_dict()
                    if hasattr(template, "as_dict")
                    else dict(template)
                )
                summary = {
                    "id": template_dict.get("id"),
                    "name": template_dict.get("name"),
                    "displayName": template_dict.get("display_name")
                    or template_dict.get("displayName"),
                    "description": template_dict.get("description"),
                    "kind": template_dict.get("kind"),
                }
                results.append(summary)
            except Exception as e:
                logger.warning("Error processing template: %s", e)
                results.append({"error": f"Error processing template: {str(e)}"})
        return results


class SentinelAnalyticsRuleTemplateGetTool(MCPToolBase):
    """
    Get details for a specific Sentinel analytics rule template by ID.
    Returns a dict with summary fields and full template details, or error details.
    """

    name = "sentinel_analytics_rule_template_get"
    description = "Get a specific Sentinel analytics rule template"

    async def run(self, ctx: Context, **kwargs):
        """
        Get details for a specific analytics rule template by ID.
        Parameters:
            ctx (Context): MCP context object.
            template_id (str): The ID of the analytics rule template to retrieve.
            **kwargs: Accepts template_id as direct key or via kwargs["kwargs"].
        Returns:
            dict: Template summary and details, or error dict.
        """
        logger = self.logger
        # Extract template_id using the centralized parameter extraction from MCPToolBase
        template_id = self._extract_param(kwargs, "template_id")
        if not template_id:
            logger.error(
                "No template_id provided for analytics rule template retrieval."
            )
            return {"error": "No template_id provided."}
        # Extract Azure context
        workspace, resource_group, subscription_id = self.get_azure_context(ctx)
        if not (workspace and resource_group and subscription_id):
            logger.error(
                "Missing Azure Sentinel context for analytics rule template retrieval."
            )
            return {"error": "Missing Azure Sentinel context."}
        # Get client
        client = self.get_securityinsight_client(subscription_id)
        try:
            template = client.alert_rule_templates.get(
                resource_group, workspace, template_id
            )
            template_dict = (
                template.as_dict() if hasattr(template, "as_dict") else dict(template)
            )
            summary = {
                "id": template_dict.get("id"),
                "name": template_dict.get("name"),
                "displayName": template_dict.get("display_name")
                or template_dict.get("displayName"),
                "description": template_dict.get("description"),
                "kind": template_dict.get("kind"),
            }
            summary["_full"] = template_dict
            return summary
        except Exception as e:
            logger.error("Error retrieving analytics rule template: %s", e)
            # pylint: disable=consider-using-f-string
            return {"error": f"Error retrieving analytics rule template: {str(e)}"}


# --- Utility: Extract tags, tactics, techniques from analytics rules/templates ---
def extract_tags_tactics_techniques_from_dict(obj):
    """
      Extract tags, tactics, and techniques from an analytics rule/template dict.

    Args:
        obj (dict): Analytics rule or template dictionary.

    Returns:
        tuple: (tags, tactics, techniques)
            tags (list[dict]): All tags as {name, value} pairs.
            tactics (list[str]): List of tactics (from tags or legacy fields).
            techniques (list[str]): List of techniques (from tags or legacy fields).

    Extraction precedence:
        - Tactics/techniques: Prefer tags with name 'tactics'/'techniques'
          (case-insensitive, split on comma). Fallback to legacy fields.
        - Tags: All tags as {name, value} pairs (robust to SDK object, dict, or string).
    """
    tags = []
    tactics = []
    techniques = []
    raw_tags = obj.get("tags")
    if raw_tags:
        for tag in raw_tags:
            tag_name = None
            tag_value = None
            if isinstance(tag, dict):
                tag_name = tag.get("name") or tag.get("Name")
                tag_value = tag.get("value") or tag.get("Value")
            elif hasattr(tag, "name") and hasattr(tag, "value"):
                tag_name = getattr(tag, "name", None)
                tag_value = getattr(tag, "value", None)
            elif isinstance(tag, str):
                tag_name = tag
                tag_value = None
            else:
                try:
                    tag_name = str(tag)
                except Exception:
                    continue
            if tag_name is not None:
                tags.append({"name": tag_name, "value": tag_value})
    for tag in tags:
        if tag["name"] and isinstance(tag["name"], str):
            if tag["name"].lower() == "tactics" and tag["value"]:
                tactics += [t.strip() for t in tag["value"].split(",") if t.strip()]
            elif tag["name"].lower() == "techniques" and tag["value"]:
                techniques += [t.strip() for t in tag["value"].split(",") if t.strip()]
    legacy_tactics = obj.get("tactics")
    if legacy_tactics:
        tactics += [
            t.strip() for t in legacy_tactics if isinstance(t, str) and t.strip()
        ]
    legacy_techniques = obj.get("techniques")
    if legacy_techniques:
        techniques += [
            t.strip() for t in legacy_techniques if isinstance(t, str) and t.strip()
        ]
    tactics = list(dict.fromkeys([t for t in tactics if t]))
    techniques = list(dict.fromkeys([t for t in techniques if t]))
    return tags, tactics, techniques


class SentinelAnalyticsRulesCountByTacticTool(MCPToolBase):
    """
    Count Sentinel analytics rules by tactic.
    Extracts tactics from each rule and returns a mapping of tactic to count and
    rule summaries.
    """

    name = "sentinel_analytics_rules_count_by_tactic"
    description = "Count Sentinel analytics rules by tactic."

    async def run(self, ctx: Context, **kwargs) -> Dict:
        """
        Count analytics rules by tactic.
        Returns a dict: {tactic: {count: int, rules: [{id, display_name}]}}
        """
        logger = self.logger
        workspace, resource_group, subscription_id = self.get_azure_context(ctx)
        if not (workspace and resource_group and subscription_id):
            logger.error("Missing Azure Sentinel context for analytics rule listing.")
            return {"error": "Missing Azure Sentinel context."}
        client = self.get_securityinsight_client(subscription_id)
        tactic_map = {}
        try:
            rules = client.alert_rules.list(
                resource_group_name=resource_group,
                workspace_name=workspace,
            )
            for rule in rules:
                rule_dict = rule.as_dict() if hasattr(rule, "as_dict") else dict(rule)
                # pylint: disable=unused-variable
                tags, tactics, _ = extract_tags_tactics_techniques_from_dict(rule_dict)
                display_name = (
                    rule_dict.get("display_name")
                    or rule_dict.get("displayName")
                    or rule_dict.get("name")
                )
                for tactic in tactics or ["Unknown"]:
                    tkey = tactic.lower() or "unknown"
                    if tkey not in tactic_map:
                        tactic_map[tkey] = {"count": 0, "rules": []}
                    tactic_map[tkey]["count"] += 1
                    tactic_map[tkey]["rules"].append(
                        {
                            "id": rule_dict.get("id"),
                            "display_name": display_name,
                        }
                    )
            return {
                "valid": True,
                "error": None,
                "results": tactic_map,
                "errors": [],
            }
        except Exception as e:
            logger.error("Error in %s: %s", self.__class__.__name__, str(e))
            return {
                "valid": False,
                "error": str(e),
                "results": None,
                "errors": [str(e)],
            }


class SentinelAnalyticsRuleTemplatesCountByTacticTool(MCPToolBase):
    """
    Count Sentinel analytics rule templates by tactic.
    Extracts tactics from each template and returns a mapping of tactic to count
    and template summaries.
    """

    name = "sentinel_analytics_rule_templates_count_by_tactic"
    description = "Count Sentinel analytics rule templates by tactic."

    async def run(self, ctx: Context, **kwargs) -> Dict:
        """
        Count analytics rule templates by tactic.
        Returns a dict: {tactic: {count: int, templates: [{id, display_name}]}}
        """
        logger = self.logger
        # Extract Azure context
        workspace, resource_group, subscription_id = self.get_azure_context(ctx)
        client = self.get_securityinsight_client(subscription_id)
        tactic_map = {}
        try:
            templates = client.alert_rule_templates.list(resource_group, workspace)
            for template in templates:
                template_dict = (
                    template.as_dict()
                    if hasattr(template, "as_dict")
                    else dict(template)
                )
                # pylint: disable=unused-variable
                tags, tactics, _ = extract_tags_tactics_techniques_from_dict(
                    template_dict
                )
                display_name = (
                    template_dict.get("display_name")
                    or template_dict.get("displayName")
                    or template_dict.get("name")
                )
                for tactic in tactics or ["Unknown"]:
                    tkey = tactic.lower() or "unknown"
                    if tkey not in tactic_map:
                        tactic_map[tkey] = {"count": 0, "templates": []}
                    tactic_map[tkey]["count"] += 1
                    tactic_map[tkey]["templates"].append(
                        {
                            "id": template_dict.get("id"),
                            "display_name": display_name,
                        }
                    )
            return {
                "valid": True,
                "error": None,
                "results": tactic_map,
                "errors": [],
            }
        except Exception as e:
            logger.error("Error in %s: %s", self.__class__.__name__, str(e))
            return {
                "valid": False,
                "error": str(e),
                "results": None,
                "errors": [str(e)],
            }


class SentinelAnalyticsRulesCountByTechniqueTool(MCPToolBase):
    """
    Count Sentinel analytics rules by MITRE technique.
    Extracts techniques from each rule and returns a mapping of technique to count
    and rule summaries.
    """

    name = "sentinel_analytics_rules_count_by_technique"
    description = "Count Sentinel analytics rules by MITRE technique."

    async def run(self, ctx: Context, **kwargs) -> Dict:
        """
        Count analytics rules by technique.
        Returns a dict: {technique: {count: int, rules: [{id, display_name}]}}
        """
        logger = self.logger
        workspace, resource_group, subscription_id = self.get_azure_context(ctx)
        client = self.get_securityinsight_client(subscription_id)
        technique_map = {}
        try:
            rules = client.alert_rules.list(
                resource_group_name=resource_group,
                workspace_name=workspace,
            )
            for rule in rules:
                rule_dict = rule.as_dict() if hasattr(rule, "as_dict") else dict(rule)
                _, _, techniques = extract_tags_tactics_techniques_from_dict(rule_dict)
                display_name = (
                    rule_dict.get("display_name")
                    or rule_dict.get("displayName")
                    or rule_dict.get("name")
                )
                for technique in techniques or ["Unknown"]:
                    tkey = technique.lower() or "unknown"
                    if tkey not in technique_map:
                        technique_map[tkey] = {"count": 0, "rules": []}
                    technique_map[tkey]["count"] += 1
                    technique_map[tkey]["rules"].append(
                        {
                            "id": rule_dict.get("id"),
                            "display_name": display_name,
                        }
                    )
            return {
                "valid": True,
                "error": None,
                "results": technique_map,
                "errors": [],
            }
        except Exception as e:
            logger.error("Error in %s: %s", self.__class__.__name__, str(e))
            return {
                "valid": False,
                "error": str(e),
                "results": None,
                "errors": [str(e)],
            }


class SentinelAnalyticsRuleTemplatesCountByTechniqueTool(MCPToolBase):
    """
    Count Sentinel analytics rule templates by MITRE technique.
    Extracts techniques from each template and returns a mapping of technique to
    count and template summaries.
    """

    name = "sentinel_analytics_rule_templates_count_by_technique"
    description = "Count Sentinel analytics rule templates by MITRE technique."

    async def run(self, ctx: Context, **kwargs):
        """
        Count analytics rule templates by technique.
        Returns a dict: {technique: {count: int, templates: [{id, display_name}]}}
        """
        logger = self.logger
        workspace, resource_group, subscription_id = self.get_azure_context(ctx)
        client = self.get_securityinsight_client(subscription_id)
        technique_map = {}
        try:
            templates = client.alert_rule_templates.list(resource_group, workspace)
            for template in templates:
                template_dict = (
                    template.as_dict()
                    if hasattr(template, "as_dict")
                    else dict(template)
                )
                _, _, techniques = extract_tags_tactics_techniques_from_dict(
                    template_dict
                )
                display_name = (
                    template_dict.get("display_name")
                    or template_dict.get("displayName")
                    or template_dict.get("name")
                )
                for technique in techniques or ["Unknown"]:
                    tkey = technique.lower() or "unknown"
                    if tkey not in technique_map:
                        technique_map[tkey] = {"count": 0, "templates": []}
                    technique_map[tkey]["count"] += 1
                    technique_map[tkey]["templates"].append(
                        {
                            "id": template_dict.get("id"),
                            "display_name": display_name,
                        }
                    )
            return {
                "valid": True,
                "error": None,
                "results": technique_map,
                "errors": [],
            }
        except Exception as e:
            logger.error("Error in %s: %s", self.__class__.__name__, str(e))
            return {
                "valid": False,
                "error": str(e),
                "results": None,
                "errors": [str(e)],
            }


def register_tools(mcp):
    """
    Register all analytics tools with the given MCP server instance.

    Args:
        mcp: The MCP server instance to register tools with.
    """
    SentinelAnalyticsRuleListTool.register(mcp)
    SentinelAnalyticsRuleGetTool.register(mcp)
    SentinelAnalyticsRuleTemplatesListTool.register(mcp)
    SentinelAnalyticsRuleTemplateGetTool.register(mcp)
    SentinelAnalyticsRulesCountByTacticTool.register(mcp)
    SentinelAnalyticsRuleTemplatesCountByTacticTool.register(mcp)
    SentinelAnalyticsRulesCountByTechniqueTool.register(mcp)
    SentinelAnalyticsRuleTemplatesCountByTechniqueTool.register(mcp)
