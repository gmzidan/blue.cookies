# Telegram → Google Sheets Bot

Bot Telegram sederhana untuk menyimpan pesan otomatis ke Google Sheet.

## 🚀 Cara pakai

1. Buat bot lewat @BotFather, catat TELEGRAM_BOT_TOKEN.
2. Buat Google Sheet baru, ambil SPREADSHEET_ID dari URL.
3. Buat Service Account + aktifkan Google Sheets API.
4. Copy isi `credentials.json` ke variabel environment GOOGLE_CREDS_JSON.
5. Deploy ke Render / Railway.

## ⚙️ Environment Variables
- `TELEGRAM_BOT_TOKEN` → token bot dari BotFather
- `SPREADSHEET_ID` → ID spreadsheet dari URL
- `GOOGLE_CREDS_JSON` → isi lengkap credentials.json (format JSON string)

## 📦 Install local
```bash
pip install -r requirements.txt
python bot_polling.py
