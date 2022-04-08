import os

from config import HAS_IMPRESSIONS_FILTER
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adaccountuser import AdAccountUser as AdUser
from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import Cursor, FacebookAdsApi
from transform_insights import transform_campaign

ACCESS_TOKEN = os.environ.get("access_token")
ACCOUNT_ID = os.environ.get("account_id")

FacebookAdsApi.init(access_token=ACCESS_TOKEN)
me = AdUser(fbid=ACCOUNT_ID)


def get_ad_accounts(ad_user: AdUser) -> list[str]:
    """
    Returns list of all AdAccounts
    """
    return [account["id"] for account in list(ad_user.get_ad_accounts())]


def get_campaigns_for_account(account: str, start_date: str, end_date: str) -> Cursor:
    """
    Fetches all campaigns for specified account
    """
    fields = ["name", "id", "daily_budget"]
    params = {
        "time_range": {"since": start_date, "until": end_date},
        "filtering": [HAS_IMPRESSIONS_FILTER],
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


def extract_campaign_insights_for_account(account, start_date, end_date):
    extracted_campaigns = []
    campaigns = get_campaigns_for_account(account, start_date, end_date)
    for campaign in campaigns:
        campaign_insights = get_campaign_insights(campaign, start_date, end_date)
        transformed_campaign = transform_campaign(campaign, campaign_insights)
        extracted_campaigns.append(transformed_campaign)
    return extracted_campaigns
