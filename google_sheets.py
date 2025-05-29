import gspread
from google.oauth2.service_account import Credentials
from config import GOOGLE_SHEET_ID
import datetime

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'service_account.json'

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

client = gspread.authorize(credentials)

def get_spreadsheet_by_id():
    return client.open_by_key(GOOGLE_SHEET_ID)

def get_worksheet(spreadsheet, sheet_name):
    return spreadsheet.worksheet(sheet_name)

def get_column_values(sheet_name, column_name):
    spreadsheet = get_spreadsheet_by_id()
    worksheet = get_worksheet(spreadsheet, sheet_name)
    records = worksheet.get_all_records()
    return [str(r.get(column_name, "")).strip() for r in records if column_name in r]

def get_all_records(sheet_name):
    spreadsheet = get_spreadsheet_by_id()
    worksheet = get_worksheet(spreadsheet, sheet_name)
    return worksheet.get_all_records()

def find_record(sheet_name, key_column, key_value):
    spreadsheet = get_spreadsheet_by_id()
    worksheet = get_worksheet(spreadsheet, sheet_name)
    records = worksheet.get_all_records()
    for record in records:
        if str(record.get(key_column)).strip() == str(key_value).strip():
            return record
    return None

def add_record(sheet_name, record):
    spreadsheet = get_spreadsheet_by_id()
    worksheet = get_worksheet(spreadsheet, sheet_name)
    worksheet.append_row([record.get(col, "") for col in worksheet.row_values(1)])

def update_record(sheet_name, key_column, key_value, new_data):
    spreadsheet = get_spreadsheet_by_id()
    worksheet = get_worksheet(spreadsheet, sheet_name)
    records = worksheet.get_all_records()
    headers = worksheet.row_values(1)

    for i, record in enumerate(records):
        if str(record.get(key_column)).strip() == str(key_value).strip():
            row_index = i + 2
            for col, val in new_data.items():
                if col in headers:
                    col_index = headers.index(col) + 1
                    worksheet.update_cell(row_index, col_index, val)
            return True
    return False

def format_date_for_client(date_str):
    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        return date_str
