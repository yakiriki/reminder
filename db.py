import datetime
from supabase import create_client, Client
from config import Config

supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY, async_=True)

# USERS

async def get_user(user_id):
    res = await supabase.table("users").select("*").eq("user_id", user_id).execute()
    return res.data[0] if res.data else None

async def add_user(user_id, username, is_admin=False):
    res = await supabase.table("users").insert({
        "user_id": user_id,
        "username": username,
        "is_admin": is_admin
    }).execute()
    return res

async def remove_user(user_id):
    res = await supabase.table("users").delete().eq("user_id", user_id).execute()
    return res

async def list_users():
    res = await supabase.table("users").select("*").execute()
    return res.data

# REMINDERS

async def create_reminder(user_id, type, time, date=None, days_of_week=None, interval_min=1, active=True, name=None):
    res = await supabase.table("reminders").insert({
        "user_id": user_id,
        "type": type,
        "time": time,
        "date": date,
        "days_of_week": days_of_week,
        "interval_min": interval_min,
        "active": active,
        "name": name,
        "confirmed": False
    }).execute()
    return res

async def get_reminders(user_id=None):
    q = supabase.table("reminders").select("*")
    if user_id:
        q = q.eq("user_id", user_id)
    res = await q.execute()
    return res.data

async def get_reminders_by_user(user_id):
    res = await supabase.table("reminders").select("*").eq("user_id", user_id).eq("active", True).execute()
    return res.data if res.data else []

async def update_reminder(reminder_id, **fields):
    res = await supabase.table("reminders").update(fields).eq("id", reminder_id).execute()
    return res

async def delete_reminder(reminder_id):
    res = await supabase.table("reminders").delete().eq("id", reminder_id).execute()
    return res

async def confirm_reminder(reminder_id):
    # Отметить напоминание как подтверждённое
    res = await supabase.table("reminders").update({"confirmed": True}).eq("id", reminder_id).execute()
    return res

# SCREENSHOTS

async def add_screenshot(user_id, file_url):
    res = await supabase.table("screenshots").insert({
        "user_id": user_id,
        "file_url": file_url,
        "added_at": datetime.datetime.utcnow().isoformat()
    }).execute()
    return res

async def get_screenshots(user_id=None, date_from=None, date_to=None):
    q = supabase.table("screenshots").select("*")
    if user_id:
        q = q.eq("user_id", user_id)
    if date_from:
        q = q.gte("added_at", date_from)
    if date_to:
        q = q.lte("added_at", date_to)
    q = q.order("added_at", desc=False)
    res = await q.execute()
    return res.data

# REMINDER RESPONSES

async def add_reminder_response(reminder_id, user_id, screenshot_id=None):
    res = await supabase.table("reminder_responses").insert({
        "reminder_id": reminder_id,
        "user_id": user_id,
        "screenshot_id": screenshot_id,
        "replied_at": datetime.datetime.utcnow().isoformat()
    }).execute()
    return res

async def get_stats():
    screenshots = await supabase.table("screenshots").select("id").execute()
    reminders = await supabase.table("reminders").select("id").execute()
    responses = await supabase.table("reminder_responses").select("id").execute()
    return {
        "screenshots": len(screenshots.data),
        "reminders": len(reminders.data),
        "responses": len(responses.data),
    }

# STORAGE

async def upload_file(file_bytes, filename):
    storage = supabase.storage()
    bucket = storage.from_(Config.SUPABASE_BUCKET)
    path = f"{datetime.datetime.utcnow().strftime('%Y/%m/%d')}/{filename}"
    res = await bucket.upload(path, file_bytes, {"content-type": "image/png"})
    # Проверяем статус ответа
    if res and getattr(res, "status_code", None) in (200, 201):
        public_url = bucket.get_public_url(path)
        return public_url
    return None
