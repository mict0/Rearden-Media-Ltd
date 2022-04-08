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


def prepare_data_for_google(campaign_insights):
    # once everything is fetched it should be stored here
    # and sent as data in google helper
    # those are columns in google sheet and data should be stored accordingly
    # use campaign_insights to get right data in right place
    prepared_data = {}
    prepared_data["week_number"] = ""
    prepared_data["offer"] = ""
    prepared_data["cpa_type"] = ""
    prepared_data["be_cpa"] = ""
    prepared_data["purchases_cold"] = ""
    prepared_data["amount_spent_cold"] = ""
    prepared_data["tracked_cpa_cold"] = ""
    prepared_data["current_daily_budget_ret"] = ""
    prepared_data["profitability_ret"] = ""
    prepared_data["profitability_cold"] = ""
    prepared_data["profitability_total"] = ""
    prepared_data["amount_spent_total"] = ""
    prepared_data["current_daily_budget_total"] = ""
    prepared_data["average_daily_budget_total"] = ""
    prepared_data["fb_only_traffic_channel"] = ""
    prepared_data["backend_revenue"] = ""
    prepared_data["gross_margin"] = ""
    prepared_data["backend_profits"] = ""
    return [[v for v in prepared_data.values()]]
