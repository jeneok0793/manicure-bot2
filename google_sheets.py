import json
import gspread
from google.oauth2.service_account import Credentials
import os

# Путь к секретному JSON-файлу от сервисного аккаунта
SERVICE_ACCOUNT_FILE = "/etc/secrets/service_account.json"

# ID таблицы из Google Sheets
SPREADSHEET_ID = "16gIFFCTsBHxFaRI6uNAoQCehMey2IbGddHlcY3XxICY"

# Названия листов
SHEET_NAMES = {
    "clients": "clients",
    "slots": "slots",
    "admins": "admins",
}

# Авторизация
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(credentials)

# Получить таблицу
def get_spreadsheet_by_id():
    return client.open_by_key(SPREADSHEET_ID)

# Получить лист
def get_worksheet(spreadsheet, sheet_name):
    return spreadsheet.worksheet(sheet_name)

# Получить все записи из листа
def get_all_records(sheet_name):
    spreadsheet = get_spreadsheet_by_id()
    worksheet = get_worksheet(spreadsheet, sheet_name)
    return worksheet.get_all_records()

# Добавить запись
def add_record(sheet_name, data):
    spreadsheet = get_spreadsheet_by_id()
    worksheet = get_worksheet(spreadsheet, sheet_name)
    worksheet.append_row(list(data.values()))

# Найти запись по ключу
def find_record(sheet_name, key_column, key_value):
    records = get_all_records(sheet_name)
    for record in records:
        if str(record.get(key_column)) == str(key_value):
            return record
    return None

# Обновить запись
def update_record(sheet_name, key_column, key_value, new_data):
    spreadsheet = get_spreadsheet_by_id()
    worksheet = get_worksheet(spreadsheet, sheet_name)
    all_data = worksheet.get_all_values()
    headers = all_data[0]
    for idx, row in enumerate(all ​:contentReference[oaicite:0]{index=0}​
