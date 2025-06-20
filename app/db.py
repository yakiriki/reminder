import asyncpg
from app.config import Config
import datetime
import aiohttp
import base64

# ----- DB UTILS -----

async def get_db():
    return await asyncpg.create_pool(Config.SUPABASE_DB_URL)

# ----- USERS -----

async def get_user(pool, user_id):
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM users WHERE user_id=$1", user_id)
        return dict(row) if row else None

async def add_user(pool, user_id, username, is_admin=False):
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO users (user_id, username, is_admin) VALUES ($1, $2, $3) ON CONFLICT (user_id) DO NOTHING",
            user_id, username, is_admin
        )

async def remove_user(pool, user_id):
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM users WHERE user_id=$1", user_id)

async def list_users(pool):
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM users ORDER BY user_id")
        return [dict(row) for row in rows]

# ----- REMINDERS -----

async def create_reminder(pool, user_id, typ, time, date=None, days_of_week=None, interval_min=1, active=True):
    async with pool.acquire() as conn:
        await conn.execute(
            """INSERT INTO reminders (user_id, type, time, date, days_of_week, interval_min, active)
               VALUES ($1, $2, $3, $4, $5, $6, $7)""",
            user_id, typ, time, date, days_of_week, interval_min, active
        )

async def get_reminders(pool, user_id=None):
    async with pool.acquire() as conn:
        if user_id:
            rows = await conn.fetch("SELECT * FROM reminders WHERE user_id=$1", user_id)
        else:
            rows = await conn.fetch("SELECT * FROM reminders")
        return [dict(row) for row in rows]

async def update_reminder(pool, reminder_id, **fields):
    keys, values = zip(*fields.items())
    set_str = ', '.join([f"{k}=${i+2}" for i, k in enumerate(keys)])
    sql = f"UPDATE reminders SET {set_str} WHERE id=$1"
    async with pool.acquire() as conn:
        await conn.execute(sql, reminder_id, *values)

async def delete_reminder(pool, reminder_id):
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM reminders WHERE id=$1", reminder_id)

# ----- SCREENSHOTS -----

async def add_screenshot(pool, user_id, file_url):
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO screenshots (user_id, file_url, added_at) VALUES ($1, $2, $3)",
            user_id, file_url, datetime.datetime.utcnow()
        )

async def get_screenshots(pool, user_id=None, date_from=None, date_to=None):
    async with pool.acquire() as conn:
        sql = "SELECT * FROM screenshots WHERE 1=1"
        params = []
        if user_id:
            sql += " AND user_id=$" + str(len(params) + 1)
            params.append(user_id)
        if date_from:
            sql += " AND added_at>=$" + str(len(params) + 1)
            params.append(date_from)
        if date_to:
            sql += " AND added_at<=$" + str(len(params) + 1)
            params.append(date_to)
        sql += " ORDER BY added_at"
        rows = await conn.fetch(sql, *params)
        return [dict(row) for row in rows]

# ----- REMINDER RESPONSES -----

async def add_reminder_response(pool, reminder_id, user_id, screenshot_id=None):
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO reminder_responses (reminder_id, user_id, screenshot_id, replied_at) VALUES ($1, $2, $3, $4)",
            reminder_id, user_id, screenshot_id, datetime.datetime.utcnow()
        )

async def get_stats(pool):
    async with pool.acquire() as conn:
        screenshots = await conn.fetchval("SELECT COUNT(*) FROM screenshots")
        reminders = await conn.fetchval("SELECT COUNT(*) FROM reminders")
        responses = await conn.fetchval("SELECT COUNT(*) FROM reminder_responses")
        return {
            "screenshots": screenshots,
            "reminders": reminders,
            "responses": responses
        }

# ----- SUPABASE STORAGE -----

async def upload_file(file_bytes, filename):
    url = f"{Config.SUPABASE_URL}/storage/v1/object/{Config.SUPABASE_BUCKET}/{filename}"
    headers = {
        "apikey": Config.SUPABASE_KEY,
        "Authorization": f"Bearer {Config.SUPABASE_KEY}",
        "Content-Type": "application/octet-stream"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=file_bytes) as resp:
            if resp.status in (200, 201):
                return f"{Config.SUPABASE_URL}/storage/v1/object/public/{Config.SUPABASE_BUCKET}/{filename}"
            else:
                return None
