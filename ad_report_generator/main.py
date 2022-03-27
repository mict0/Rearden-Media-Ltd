from pprint import pprint

from date_helper import DateHelper
from helpers import get_ad_accounts, get_campaign_insights, get_campaigns_for_account, me
from transform_insights import transform_campaign

dh = DateHelper(month=True)
start_date, end_date = dh.get_start_date(), dh.get_end_date()
print(f"Extracting campaign data for timerange: {start_date} {end_date}")

ad_accounts = get_ad_accounts(me)
for acc in ad_accounts:
    campaigns = get_campaigns_for_account(acc, start_date, end_date)
    for campaign in campaigns:
        if (
            campaign["name"]
            == "EM 1.57 WW_EX_LPPC Consolidation BO AV_1 3 copies 2 captivating variants #sd1"
        ):
            campaign_insights = get_campaign_insights(campaign, start_date, end_date)
            transformed_campaign = transform_campaign(campaign, campaign_insights)
            pprint(transformed_campaign)
            break
