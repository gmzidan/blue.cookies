# bot_polling.py

import os
import time
import requests
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# --- Konfigurasi ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
GOOGLE_CREDS_JSON = os.environ.get("GOOGLE_CREDS_JSON")  # isi credentials.json dalam bentuk string

# Setup Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]

# parsing JSON dari env (karena kita tidak pakai file credentials.json langsung)
import json
creds_dict = json.loads(GOOGLE_CREDS_JSON)
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
gc = gspread.authorize(creds)
sheet = gc.open_by_key(SPREADSHEET_ID).sheet1  # ambil sheet pertama

# --- Fungsi ambil pesan dari Telegram ---
def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    params = {"timeout": 30, "offset": offset}
    r = requests.get(url, params=params, timeout=35)
    r.raise_for_status()
    return r.json()

# --- Fungsi simpan pesan ke Sheet ---
def save_message(msg):
    user = msg.get("from", {})
    text = msg.get("text", "")
    ts = datetime.utcfromtimestamp(msg.get("date")).strftime("%Y-%m-%d %H:%M:%S")

    row = [
        ts,
        user.get("id"),
        user.get("username", ""),
        text
    ]

    sheet.append_row(row, value_input_option="RAW")
    print("Tersimpan:", row)

# --- Main loop polling ---
def main():
    print("Bot started (polling)...")
    offset = None
    while True:
        try:
            updates = get_updates(offset)
            for upd in updates.get("result", []):
                offset = upd["update_id"] + 1
                if "message" in upd:
                    save_message(upd["message"])
        except Exception as e:
            print("Error:", e)
            time.sleep(5)

if __name__ == "__main__":
    main()
