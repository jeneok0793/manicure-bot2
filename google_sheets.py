import json
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "/etc/secrets/SERVICE_ACCOUNT_JSON"

with open(SERVICE_ACCOUNT_FILE, "r") as f:
    data = json.load(f)
    credentials = Credentials.from_service_account_info(data, scopes=SCOPES)

client = gspread.authorize(credentials)
sheet = client.open_by_key("16gIFFCTsBHxFaRI6uNAoQCehMey2IbGddHlcY3XxICY")
clients_sheet = sheet.worksheet("clients")
slots_sheet = sheet.worksheet("slots")
templates_sheet = sheet.worksheet("templates")
