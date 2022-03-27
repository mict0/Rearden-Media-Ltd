from date_helper import DateHelper
from helpers import extract_campaign_insights_for_account, get_ad_accounts, me

dh = DateHelper(month=True)
start_date, end_date = dh.get_start_date(), dh.get_end_date()
print(f"Extracting campaign data for timerange: {start_date} {end_date}")


ad_accounts = get_ad_accounts(me)
campaign_insights = [
    extract_campaign_insights_for_account(account, start_date, end_date)
    for account in ad_accounts
]
