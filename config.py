import os
from dotenv import load_dotenv

load_dotenv()  # Загружает .env

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env")
