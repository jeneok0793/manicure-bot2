import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
client = gspread.authorize(credentials)

# Открытие таблицы по ID
sheet = client.open_by_key("1Sk3XGVrTgiWy9vQ-Acnog1LscsFZoU5CO5RHqxL8oLs")

clients_sheet = sheet.worksheet("clients")
slots_sheet = sheet.worksheet("slots")
templates_sheet = sheet.worksheet("templates")

def get_available_slots():
    slots = slots_sheet.get_all_records()
    return [s for s in slots if s["статус"] == "свободно"]

def book_slot(user_id, name, phone, date, time, service, price, is_free):
    records = slots_sheet.get_all_records()
    for i, record in enumerate(records, start=2):
        if record["дата"] == date and record["время"] == time and record["статус"] == "свободно":
            slots_sheet.update(f"I{i}", "занято")
            clients_sheet.append_row([user_id, name, phone, date, time, service, price, "активно", is_free])
            return True
    return False

def get_user_bookings(user_id):
    records = clients_sheet.get_all_records()
    return [r for r in records if str(r["Telegram ID"]) == str(user_id) and r["статус"] == "активно"]

def cancel_booking_by_row(row_number):
    clients_sheet.update(f"H{row_number}", "отменено")
    slot_date = clients_sheet.cell(row_number, 4).value
    slot_time = clients_sheet.cell(row_number, 5).value
    slot_records = slots_sheet.get_all_records()
    for i, record in enumerate(slot_records, start=2):
        if record["дата"] == slot_date and record["время"] == slot_time:
            slots_sheet.update(f"I{i}", "свободно")
            break

async def init_google_sheets():
    pass
