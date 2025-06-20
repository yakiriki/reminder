import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "screenshots")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0"))
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT = int(os.getenv("APP_PORT", "8080"))