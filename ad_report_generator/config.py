ACTIVE_CAMPAIGN_FILTER = {
    "field": "delivery_info",
    "operator": "IN",
    "value": ["active"],
}
ACTIVE_OR_SCHEDULED_CAMPAIGN_FILTER = {
    "field": "delivery_info",
    "operator": "IN",
    "value": ["active", "scheduled"],
}
HAS_IMPRESSIONS_FILTER = {
    "field": "impressions",
    "operator": "GREATER_THAN",
    "value": "0",
}
