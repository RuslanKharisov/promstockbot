import gspread
from google.oauth2.service_account import Credentials

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(creds)

# Укажи ID твоей таблицы
GOOGLE_SHEET_ID = "1aVJp-81j-crDAuxcnrmx4qqMYJL14EgWz9IGD1ElsIA"

sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1

# Пробуем записать строку
sheet.append_row(["🔧 Test", "✅ Success", "Hello from bot!", "2025-04-17"])
print("✅ Запись прошла успешно!")
