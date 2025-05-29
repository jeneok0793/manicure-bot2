import gspread
from google.oauth2.service_account import Credentials
from config import GOOGLE_SHEET_ID

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_FILE = "/etc/secrets/service_account.json"

credentials = Credentials.from_service_account_file(SERVICE_FILE, scopes=SCOPES)
client = gspread.authorize(credentials)

def get_spreadsheet_by_id():
    return client.open_by_key(GOOGLE_SHEET_ID)

def get_worksheet(spreadsheet, sheet_name):
    return spreadsheet.worksheet(sheet_name)

def get_all_records(sheet_name):
    sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet(sheet_name)
    return sheet.get_all_records()

def find_record(sheet_name, column_name, value):
    sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet(sheet_name)
    records = sheet.get_all_records()
    headers = sheet.row_values(1)
    try:
        col_index = headers.index(column_name)
    except ValueError:
        return None
    for i, row in enumerate(records):
        if str(row.get(column_name)) == str(value):
            return row
    return None

def get_column_values(sheet_name, column_name):
    sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet(sheet_name)
    headers = sheet.row_values(1)
    try:
        col_index = headers.index(column_name)
    except ValueError:
        return []
    column_data = sheet.col_values(col_index + 1)
    return column_data[1:]

def add_record(sheet_name, record):
    sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet(sheet_name)
    sheet.append_row([record.get(col, "") for col in sheet.row_values(1)])

def update_record(sheet_name, column_name, value, update_data):
    sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet(sheet_name)
    records = sheet.get_all_records()
    headers = sheet.row_values(1)
    try:
        col_index = headers.index(column_name)
    except ValueError:
        return
    for i, row in enumerate(records):
        if str(row.get(column_name)) == str(value):
            for key, new_value in update_data.items():
                if key in headers:
                    sheet.update_cell(i + 2, headers.index(key) + 1, new_value)
            return

def format_date_for_client(date_str):
    from datetime import datetime
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d.%m.%Y")
    except:
        return date_str
