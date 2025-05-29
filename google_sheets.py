import gspread
import json
import os
from google.oauth2.service_account import Credentials

# Чтение ключа из секрета Render
SERVICE_ACCOUNT_FILE = "/etc/secrets/service_account.json"

with open(SERVICE_ACCOUNT_FILE, "r") as f:
    data = json.load(f)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(data, scopes=SCOPES)

client = gspread.authorize(credentials)

# ID таблицы из переменной окружения
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
sheet = client.open_by_key(GOOGLE_SHEET_ID)

def get_worksheet(sheet, sheet_name):
    """Возвращает лист по имени"""
    return sheet.worksheet(sheet_name)

def get_all_records(sheet_name):
    """Получает все записи с листа"""
    return get_worksheet(sheet, sheet_name).get_all_records()

def get_column_values(sheet_name, column_name):
    """Получает все значения из указанного столбца"""
    worksheet = get_worksheet(sheet, sheet_name)
    data = worksheet.get_all_records()
    return [row[column_name] for row in data if column_name in row]

def find_record(sheet_name, key_column, key_value):
    """Ищет запись по значению в ключевом столбце"""
    data = get_all_records(sheet_name)
    for row in data:
        if str(row.get(key_column)) == str(key_value):
            return row
    return None

def add_record(sheet_name, record_dict):
    """Добавляет запись"""
    worksheet = get_worksheet(sheet, sheet_name)
    worksheet.append_row([record_dict.get(col, "") for col in worksheet.row_values(1)])

def update_record(sheet_name, key_column, key_value, new_data_dict):
    """Обновляет строку, в которой ключевое значение совпадает"""
    worksheet = get_worksheet(sheet, sheet_name)
    data = worksheet.get_all_records()
    headers = worksheet.row_values(1)

    for idx, row in enumerate(data):
        if str(row.get(key_column)) == str(key_value):
            row_index = idx + 2  # +1 за заголовок, +1 за смещение
            for col, value in new_data_dict.items():
                if col in headers:
                    col_index = headers.index(col) + 1
                    worksheet.update_cell(row_index, col_index, value)
            break

def format_date_for_client(date_str):
    """Форматирует YYYY-MM-DD в ДД.ММ"""
    try:
        parts = date_str.split("-")
        return f"{parts[2]}.{parts[1]}"
    except Exception:
        return date_str

def get_spreadsheet_by_id():
    """Возвращает объект Google Spreadsheet"""
    return client.open_by_key(GOOGLE_SHEET_ID)
