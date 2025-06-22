import asyncio
from datetime import datetime, date
from zoneinfo import ZoneInfo
from db import get_reminders

KYIV_TZ = ZoneInfo("Europe/Kyiv")

async def reminder_scheduler(bot):
    print("[REMINDER_SCHEDULER] стартовал!")
    while True:
        now = datetime.now(KYIV_TZ)
        reminders = get_reminders()
        for rem in reminders:
            if not rem.get("active", True) or rem.get("confirmed", False):
                continue

            msg = f"⏰ Напоминание: {rem.get('name', 'Без имени')}\nНе забудьте отправить скриншот."

            if rem["type"] == "weekly":
                days = [int(d) for d in rem.get("days_of_week", [])]
                rem_time = datetime.strptime(rem["time"], "%H:%M:%S").time()
                # если сегодня нужный день, и время уже наступило — шлём каждую минуту до подтверждения
                if now.weekday() in days:
                    rem_dt = now.replace(hour=rem_time.hour, minute=rem_time.minute, second=0, microsecond=0)
                    if now >= rem_dt:
                        try:
                            await bot.send_message(rem["user_id"], msg)
                        except Exception as e:
                            print(f"Ошибка при отправке напоминания: {e}")

            if rem["type"] == "date":
                # если дата совпадает и время уже наступило — шлём каждую минуту до подтверждения
                rem_date = rem.get("date")
                if str(now.date()) == str(rem_date):
                    rem_time = datetime.strptime(rem["time"], "%H:%M:%S").time()
                    rem_dt = datetime.combine(now.date(), rem_time, tzinfo=KYIV_TZ)
                    if now >= rem_dt:
                        try:
                            await bot.send_message(rem["user_id"], msg)
                        except Exception as e:
                            print(f"Ошибка при отправке напоминания: {e}")

        await asyncio.sleep(60)
