# google_sheets.py

import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
client = gspread.authorize(credentials)
sheet = client.open_by_key("16gIFFCTsBHxFaRI6uNAoQCehMey2IbGddHlcY3XxICY")

clients_sheet = sheet.worksheet("clients")
slots_sheet = sheet.worksheet("slots")
templates_sheet = sheet.worksheet("templates")

def get_available_slots():
    return [row for row in slots_sheet.get_all_values()[1:] if row[6] == ""]

def book_slot(user_id, name, phone, date, time, service, price, is_free):
    clients_sheet.append_row([user_id, name, phone, date, time, service, price, "запись", is_free])
    cell = slots_sheet.find(f"{date} {time}")
    slots_sheet.update_cell(cell.row, 7, user_id)

def get_user_bookings(user_id):
    return [row for row in clients_sheet.get_all_values()[1:] if row[0] == str(user_id) and row[7] == "запись"]

def cancel_booking_by_row(row_number):
    clients_sheet.update_cell(row_number, 8, "отменено")

def add_free_client_entry(user_id, name, phone, date, time, service):
    book_slot(user_id, name, phone, date, time, service, "0", "да")
