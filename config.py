from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_LINK = os.getenv("CHANNEL_LINK")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")