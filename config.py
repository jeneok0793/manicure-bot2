import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
TIMEZONE = os.getenv("TIMEZONE", "Europe/Chisinau")

SHEET_NAMES = {
    "clients": "clients",
    "slots": "slots",
    "admins": "admins"
}
