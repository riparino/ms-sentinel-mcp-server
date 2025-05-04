# Azure Sentinel Workspace Details

**Workspace Name:** `{{ workspace_name }}`
**Resource Group:** `{{ resource_group }}`  
**Subscription:** `{{ subscription_id }}`  
**Location:** `{{ direct_info.location }}`  
**SKU:** `{{ direct_info.sku }}`
{% if direct_info.sku_description %}  _Description:_ {{ direct_info.sku_description }}{% endif %}
{% if direct_info.last_sku_update %}  _Last SKU Update:_ {{ direct_info.last_sku_update }}{% endif %}
**Retention (days):** `{{ direct_info.retention_period_days }}`  
**Daily Quota (GB):** `{{ direct_info.daily_quota_gb }}`  
**Quota Reset Time:** `{{ direct_info.quota_reset_time }}`  
**Ingestion Status:** `{{ direct_info.ingestion_status }}`  
**Public Network Access (Ingestion):** `{{ direct_info.public_network_access_ingestion }}`  
**Public Network Access (Query):** `{{ direct_info.public_network_access_query }}`  
**Created:** `{{ direct_info.created }}`  
**Last Modified:** `{{ direct_info.last_modified }}`  

{% if direct_info.features %}
## Workspace Features
{% if direct_info.features.additional_properties %}
{% for k, v in direct_info.features.additional_properties.items() %}- **{{ k }}:** `{{ v }}`
{% endfor %}
{% endif %}
{% for k, v in direct_info.features.items() %}{% if k != "additional_properties" %}- **{{ k }}:** `{{ v }}`
{% endif %}{% endfor %}
{% endif %}

{% if additional_information %}
## Additional Information
{% for line in additional_information %}- {{ line }}
{% endfor %}
{% endif %}
