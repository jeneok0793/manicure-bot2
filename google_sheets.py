import gspread
from google.oauth2.service_account import Credentials
from config import GOOGLE_SHEET_ID

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "service_account.json"

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
client = gspread.authorize(credentials)

def get_spreadsheet_by_id():
    return client.open_by_key(GOOGLE_SHEET_ID)

def get_worksheet(spreadsheet, sheet_name):
    return spreadsheet.worksheet(sheet_name)

def get_all_records(sheet_name):
    sheet = get_worksheet(get_spreadsheet_by_id(), sheet_name)
    return sheet.get_all_records()

def get_column_values(sheet_name, column_name):
    records = get_all_records(sheet_name)
    return [str(r[column_name]) for r in records if column_name in r]

def find_record(sheet_name, column_name, value):
    records = get_all_records(sheet_name)
    for record in records:
        if str(record.get(column_name)) == str(value):
            return record
    return None

def add_record(sheet_name, data_dict):
    sheet = get_worksheet(get_spreadsheet_by_id(), sheet_name)
    sheet.append_row([data_dict.get(col, "") for col in sheet.row_values(1)])

def update_record(sheet_name, key_column, key_value, updated_fields):
    sheet = get_worksheet(get_spreadsheet_by_id(), sheet_name)
    all_values = sheet.get_all_values()
    headers = all_values[0]
    for i, row in enumerate(all_values[1:], start=2):
        if row[headers.index(key_column)] == str(key_value):
            for field, value in updated_fields.items():
                if field in headers:
                    col = headers.index(field)
                    sheet.update_cell(i, col + 1, value)
            return

def format_date_for_client(date_str):
    year, month, day = date_str.split("-")
    return f"{day}.{month}.{year}"
