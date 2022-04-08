from __future__ import print_function

from google.oauth2 import service_account
from googleapiclient.discovery import build
from openpyxl.utils.cell import get_column_letter

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "keys.json"  # download .json file from Google Cloud
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
SPREADSHEET_ID = ""  # id from Google Sheet URL
service = build("sheets", "v4", credentials=creds)


def append_data_to_sheet(data, column_range, spreadsheet_id):
    body = {"values": data, "majorDimension": "COLUMNS"}
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=column_range,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()


def get_all_sheets(spreadsheet):
    return [
        {
            "index": sheet["properties"]["index"],
            "title": sheet["properties"]["title"],
            "last_column": get_last_column(spreadsheet, sheet["properties"]["index"]),
        }
        for sheet in spreadsheet["sheets"]
        if sheet.get("properties") and sheet["properties"].get("index")
    ]


def get_last_column(spreadsheet, sheet_index):
    """
    Returns letter(s) for first available column to append the data to
    """
    try:
        last_column = max(
            [
                len(sheet["values"]) if sheet else 0
                for sheet in spreadsheet["sheets"][sheet_index]["data"][0]["rowData"]
            ]
        )
    except Exception as e:
        print(f"There is no data for {sheet_index}, error: {str(e)}")
        last_column = 0
    return get_column_letter(last_column + 1)


def get_range(parsed_sheet):
    title = parsed_sheet["title"]
    last_column = parsed_sheet["last_column"]
    column_range = f"{title}!{last_column}:{last_column}"
    return column_range


def get_client_from_list(client, all_sheets):
    return next(sheet for sheet in all_sheets if sheet["title"] == client)


def update_sheet_for_client(client, data):
    spreadsheet = (
        service.spreadsheets()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            fields="sheets(data/rowData/values/userEnteredValue,properties(index,sheetId,title))",
        )
        .execute()
    )

    all_sheets = get_all_sheets(spreadsheet)
    client_sheet = get_client_from_list(client, all_sheets)
    column_range = get_range(client_sheet)
    append_data_to_sheet(data, column_range, SPREADSHEET_ID)
