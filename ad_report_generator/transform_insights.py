from typing import Any

from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import Cursor
from parse_campaign_name import parse_campaign_name


def transform_campaign(campaign: Campaign, insights: dict) -> dict:
    transformed = {}
    transformed["id"] = campaign["id"]
    transformed["name"] = campaign["name"]
    transformed["daily_budget"] = campaign.get("daily_budget", "")
    for k, v in filter_insights(insights).items():
        transformed[k] = v
    transformed["parsed_name"] = parse_campaign_name(campaign["name"])
    return transformed


def get_campaign_names(campaigns: Cursor) -> list[str]:
    return [campaign["name"] for campaign in campaigns]


def _get_interesting_action_values(campaign_insight: dict) -> list[dict]:
    interesting_actions = [
        "offsite_conversion.fb_pixel_purchase",
        "omni_purchase",
    ]
    action_values = campaign_insight.get("action_values")
    if not action_values:
        return []
    return [av for av in action_values if av["action_type"] in interesting_actions]


def _get_interesting_actions(campaign_insight: dict) -> list[dict]:
    interesting_actions = [
        "offsite_conversion.fb_pixel_purchase",
        "omni_purchase",
        "purchase",
    ]
    actions = campaign_insight.get("actions")
    if not actions:
        return []
    return [action for action in actions if action["action_type"] in interesting_actions]


def filter_insights(campaign_insights: dict) -> dict:
    campaign_insights["actions"] = _get_interesting_actions(campaign_insights)
    campaign_insights["action_values"] = _get_interesting_action_values(campaign_insights)
    return campaign_insights


def _get_nested_field_by_key(lst: list, key: str) -> Any:
    return next((item["value"] for item in lst if item["action_type"] == key), None)
