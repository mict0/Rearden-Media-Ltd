# FB ad report generator


### Installation
Python 3.7+
Install the dependencies 
```sh
pip install -r requirements.txt
```
Environment variables
```sh
export access_token="fb_access_token"
export account_id="account_id"
```
### main.py
campaign_insights will return list of all campaign details for all add accounts, transformed and ready for sending in google doc
#### config.py 
Has filters for filtering campaigns and campaign insights
#### helpers.py
Uses facebook_business library to fetch the data from FB GrapQL
#### transform_insights.py
Handles transformations and preparations for sending data into Google Sheet
#### date_helper.py
Class that will return date in the right format for specified period
#### parse_camapign_name.py
Searches for the keywords in campaign name and returns dict with parsed data

### Google helper
Setting up Google API:
[Google API Python Quickstart](https://developers.google.com/sheets/api/quickstart/python)

Required stuff for connecting Python and Google API:

Project in [Google Cloud Platform](https://console.cloud.google.com/home/dashboard) needs to be created and sheets.googleapis.com service enabled.

IAM role should be created and the email for that user should be granted permission to acces Sheet, by sharing it from Google Sheet
- send share(invite) to the newly created IAM email that looks something like this user-xxx@project-name.iam.gserviceaccount.com

Fetch keys.json from [here](https://developers.google.com/workspace/guides/create-credentials)
```
SERVICE_ACCOUNT_FILE - keys.json file with credentials
SPREADSHEET_ID - id from google sheet url
```

Usage:
client_name **must** match the name in spreadsheet
```python
data = [["row1_data", "row2_data"..."row_n_data"]]
update_sheet_for_client("client_name", data)
```



### Suggestions and thoughts on what's next

- pick up data from campaing_insights and parse right columns into right field using _prepare_data_for_google_
- once that's done you should have almost everything prepared

- Idea on production realisation:
    - this should be a AWS Lambda function that's triggered using CRON job
    (since it should be running and updating data on specific days)


