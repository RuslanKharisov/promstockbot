import datetime
import gspread
from google.oauth2.service_account import Credentials
from config import GOOGLE_SHEET_ID

scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1

def append_to_sheet(user_id, username, text):
    sheet.append_row([
        str(user_id),
        username or "",
        text,
        datetime.datetime.now().isoformat()
    ])

