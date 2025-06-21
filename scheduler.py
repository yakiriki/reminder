import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
from db import get_reminders, update_reminder

KYIV_TZ = ZoneInfo("Europe/Kyiv")

async def reminder_scheduler(bot):
    print("[REMINDER_SCHEDULER] стартовал!")
    while True:
        now = datetime.now(KYIV_TZ)
        reminders = get_reminders()
        for rem in reminders:
            if not rem.get("active", True) or rem.get("confirmed", False):
                continue

            msg = f"⏰ Напоминание: {rem.get('name', '(без имени)')}\nНе забудьте отправить скриншот."

            # WEEKLY
            if rem["type"] == "weekly":
                days = [int(d) for d in rem.get("days_of_week", [])]
                rem_time = datetime.strptime(rem["time"], "%H:%M:%S").time()
                if now.weekday() in days and rem_time.hour == now.hour and rem_time.minute == now.minute:
                    try:
                        await bot.send_message(rem["user_id"], msg)
                    except Exception as e:
                        print(f"Ошибка при отправке напоминания: {e}")

            # DATE (one-time, но повторяет, пока не подтвердите)
            if rem["type"] == "date":
                if str(now.date()) == str(rem.get("date")):
                    rem_time = datetime.strptime(rem["time"], "%H:%M:%S").time()
                    if rem_time.hour == now.hour and rem_time.minute == now.minute:
                        try:
                            await bot.send_message(rem["user_id"], msg)
                        except Exception as e:
                            print(f"Ошибка при отправке напоминания: {e}")
        await asyncio.sleep(60)
