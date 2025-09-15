import os
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram.ext import Updater, MessageHandler, Filters

# ===== GOOGLE SHEETS SETUP =====
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

# credentials.json harus ada di Replit
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Ganti dengan nama sheet kamu
SHEET_NAME = "Laporan Keuangan"
sheet = client.open(SHEET_NAME).sheet1

# ===== BOT TELEGRAM SETUP =====
TOKEN = os.getenv("BOT_TOKEN")  # simpan token di Secrets Replit
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

# ===== HANDLE PESAN =====
def handle_message(update, context):
    text = update.message.text.strip()
    username = update.message.from_user.username or "unknown"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    parts = text.split(" ", 2)  # pisah max 3 bagian
    if len(parts) < 2:
        update.message.reply_text("⚠️ Format salah!\nGunakan: pendapatan 5000 keterangan")
        return

    tipe = parts[0].lower()
    if tipe not in ["pendapatan", "pengeluaran"]:
        update.message.reply_text("⚠️ Tipe harus 'pendapatan' atau 'pengeluaran'")
        return

    jumlah = parts[1]
    keterangan = parts[2] if len(parts) > 2 else ""

    # rapikan isi row
    row = [timestamp, tipe.capitalize(), jumlah, keterangan, username]

    try:
        sheet.append_row(row)
        update.message.reply_text("✅ Data berhasil disimpan ke Google Sheets!")
    except Exception as e:
        update.message.reply_text("❌ Gagal menyimpan ke Google Sheets.")
        print("Error:", e)

# ===== REGISTER HANDLER =====
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# ===== START BOT =====
print("🤖 Bot is running...")
updater.start_polling()
updater.idle()
