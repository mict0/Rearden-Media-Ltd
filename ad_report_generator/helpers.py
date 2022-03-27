import os

from config import ACTIVE_CAMPAIGN_FILTER
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adaccountuser import AdAccountUser as AdUser
from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import Cursor, FacebookAdsApi

# from facebook_business.adobjects.adsinsights import AdsInsights

ACCESS_TOKEN = os.environ.get("access_token")
ACCOUNT_ID = os.environ.get("account_id")

FacebookAdsApi.init(access_token=ACCESS_TOKEN)
me = AdUser(fbid=ACCOUNT_ID)


def get_ad_accounts(ad_user: AdUser) -> list[str]:
    """
    Returns list of all AdAccounts
    """
    return [
        account["id"]
        for account in list(ad_user.get_ad_accounts())
        if account["id"] == "act_457228929100368"
    ]


def get_campaigns_for_account(account: str, start_date: str, end_date: str) -> Cursor:
    """
    Fetches all campaigns for specified account
    """
    fields = ["name", "id", "daily_budget"]
    params = {
        "time_range": {"since": start_date, "until": end_date},
        "filtering": [ACTIVE_CAMPAIGN_FILTER],
        "level": "campaign",
    }
    campaigns = AdAccount(account).get_campaigns(fields=fields, params=params)
    return campaigns


def get_campaign_insights(campaign: Campaign, start_date: str, end_date: str) -> dict:
    """
    Fetches insights for specified campaign
    """
    fields = [
        "spend",
        "impressions",
        "cpm",
        "cpc",
        "clicks",
        "actions",
        "action_values",
    ]
    params = {
        "level": "campaign",
        "time_range": {"since": start_date, "until": end_date},
    }
    insights = campaign.get_insights(fields=fields, params=params)
    return dict(insights[0])
