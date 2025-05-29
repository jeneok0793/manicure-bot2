import os
import gspread
from google.oauth2.service_account import Credentials

# Чтение JSON из переменной окружения (обычный JSON, без base64)
import json
service_account_info = json.loads(os.getenv("SERVICE_ACCOUNT_JSON"))

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
client = gspread.authorize(credentials)

# Открываем таблицу по ID
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
sheet = client.open_by_key(GOOGLE_SHEET_ID)

# Листы
clients_sheet = sheet.worksheet("clients")
slots_sheet = sheet.worksheet("slots")
templates_sheet = sheet.worksheet("templates")

# Функции
def get_available_slots():
    slots = slots_sheet.get_all_records()
    available = [slot for slot in slots if slot["свободно?"] == "да"]
    return available

def book_slot(user_id, name, phone, date, time, service, price, free=False):
    slots = slots_sheet.get_all_records()
    for i, slot in enumerate(slots, start=2):
        if slot["дата"] == date and slot["время"] == time:
            slots_sheet.update_cell(i, 4, "нет")
            clients_sheet.append_row([user_id, name, phone, date, time, service, price, "запись", "да" if free else "нет"])
            return True
    return False

def get_user_bookings(user_id):
    bookings = clients_sheet.get_all_records()
    return [b for b in bookings if str(b["Telegram ID"]) == str(user_id) and b["статус"] == "запись"]

def cancel_booking_by_row(row_index):
    clients_sheet.update_cell(row_index, 8, "отменено")

def add_free_client_entry(user_id, name, phone, date, time, service):
    clients_sheet.append_row([user_id, name, phone, date, time, service, "0", "запись", "да"])
