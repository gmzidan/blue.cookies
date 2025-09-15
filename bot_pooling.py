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
def handle_message(update, context):
    text = update.message.text
    username = update.message.from_user.username or "unknown"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    parts = text.split(" ", 2)  # pisah jadi max 3 bagian
    if len(parts) < 2:
        update.message.reply_text("Format salah! Gunakan: pendapatan 5000 keterangan")
        return

    tipe = parts[0].lower()
    if tipe not in ["pendapatan", "pengeluaran"]:
        update.message.reply_text("Tipe harus 'pendapatan' atau 'pengeluaran'")
        return

    jumlah = parts[1]
    keterangan = parts[2] if len(parts) > 2 else ""

    # susun row sesuai tabel
    row = [timestamp, tipe.capitalize(), jumlah, keterangan, username]

    try:
        sheet.append_row(row)
        update.message.reply_text("✅ Data berhasil disimpan!")
    except Exception as e:
        update.message.reply_text("❌ Gagal menyimpan ke Google Sheets")
        print("Error:", e)
