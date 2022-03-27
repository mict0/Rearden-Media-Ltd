from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import Cursor


def transform_campaign(campaign: Campaign, insights: dict) -> dict:
    transformed = {}
    transformed["id"] = campaign["id"]
    transformed["name"] = campaign["name"]
    transformed["daily_budget"] = campaign["daily_budget"]
    transformed["insights"] = filter_insights(insights)
    return transformed


def get_campaign_names(campaigns: Cursor) -> list[str]:
    return [campaign["name"] for campaign in campaigns]


def _get_interesting_action_values(campaign_insight: dict) -> list[dict]:
    interesting_actions = [
        "offsite_conversion.fb_pixel_purchase",
        "omni_purchase",
    ]
    action_values = campaign_insight["action_values"]
    if not action_values:
        return []
    return [av for av in action_values if av["action_type"] in interesting_actions]


def _get_interesting_actions(campaign_insight: dict) -> list[dict]:
    interesting_actions = [
        "offsite_conversion.fb_pixel_purchase",
        "omni_purchase",
        "purchase",
    ]
    actions = campaign_insight["actions"]
    if not actions:
        return []
    return [action for action in actions if action["action_type"] in interesting_actions]


def filter_insights(campaign_insights: dict) -> dict:
    campaign_insights["actions"] = _get_interesting_actions(campaign_insights)
    campaign_insights["action_values"] = _get_interesting_action_values(campaign_insights)
    return campaign_insights
