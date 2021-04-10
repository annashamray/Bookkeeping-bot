import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SHEETS_NAME = os.getenv("SHEETS_NAME")
