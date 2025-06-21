from supabase import create_client, Client
from config import Config
import datetime

supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

# USERS

def get_user(user_id):
    data = supabase.table("users").select("*").eq("user_id", user_id).execute()
    return data.data[0] if data.data else None

def add_user(user_id, username, is_admin=False):
    return supabase.table("users").insert({
        "user_id": user_id,
        "username": username,
        "is_admin": is_admin
    }).execute()

def remove_user(user_id):
    return supabase.table("users").delete().eq("user_id", user_id).execute()

def list_users():
    return supabase.table("users").select("*").execute().data

# REMINDERS

def create_reminder(user_id, type, time, date=None, days_of_week=None, interval_min=1, active=True, name=None):
    return supabase.table("reminders").insert({
        "user_id": user_id,
        "type": type,
        "time": time,
        "date": date,
        "days_of_week": days_of_week,
        "interval_min": interval_min,
        "active": active,
        "name": name,             # поддержка имени
        "confirmed": False        # при создании всегда False
    }).execute()

def get_reminders(user_id=None):
    q = supabase.table("reminders").select("*")
    if user_id:
        q = q.eq("user_id", user_id)
    return q.execute().data

def get_reminders_by_user(user_id):
    data = supabase.table("reminders").select("*").eq("user_id", user_id).eq("active", True).execute()
    return data.data if data.data else []

def update_reminder(reminder_id, **fields):
    return supabase.table("reminders").update(fields).eq("id", reminder_id).execute()

def delete_reminder(reminder_id):
    return supabase.table("reminders").delete().eq("id", reminder_id).execute()

def confirm_reminder(reminder_id):
    # Отметить напоминание как подтверждённое
    supabase.table("reminders").update({"confirmed": True}).eq("id", reminder_id).execute()

# SCREENSHOTS

def add_screenshot(user_id, file_url):
    return supabase.table("screenshots").insert({
        "user_id": user_id,
        "file_url": file_url,
        "added_at": datetime.datetime.utcnow().isoformat()
    }).execute()

def get_screenshots(user_id=None, date_from=None, date_to=None):
    q = supabase.table("screenshots").select("*")
    if user_id:
        q = q.eq("user_id", user_id)
    if date_from:
        q = q.gte("added_at", date_from)
    if date_to:
        q = q.lte("added_at", date_to)
    q = q.order("added_at", desc=False)
    return q.execute().data

# REMINDER RESPONSES

def add_reminder_response(reminder_id, user_id, screenshot_id=None):
    return supabase.table("reminder_responses").insert({
        "reminder_id": reminder_id,
        "user_id": user_id,
        "screenshot_id": screenshot_id,
        "replied_at": datetime.datetime.utcnow().isoformat()
    }).execute()

def get_stats():
    screenshots = supabase.table("screenshots").select("id").execute().data
    reminders = supabase.table("reminders").select("id").execute().data
    responses = supabase.table("reminder_responses").select("id").execute().data
    return {
        "screenshots": len(screenshots),
        "reminders": len(reminders),
        "responses": len(responses),
    }

# STORAGE

def upload_file(file_bytes, filename):
    storage = supabase.storage()
    bucket = storage.from_(Config.SUPABASE_BUCKET)
    # filename should be unique (add datetime/user etc)
    path = f"{datetime.datetime.utcnow().strftime('%Y/%m/%d')}/{filename}"
    res = bucket.upload(path, file_bytes, {"content-type": "image/png"})
    if res and res.status_code in (200, 201):
        public_url = bucket.get_public_url(path)
        return public_url
    return None
