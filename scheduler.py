import asyncio
from datetime import datetime, timedelta
from aiogram import Bot
from db import get_reminders, update_reminder
from config import Config

async def reminder_scheduler(bot: Bot):
    while True:
        from datetime import datetime
        print(f"[DEBUG] Время сервера: {datetime.now()}")
        now = datetime.utcnow()
        reminders = get_reminders()
        for rem in reminders:
            # Вычисление условий срабатывания (пример — можно доработать)
            if not rem["active"]:
                continue
            # Проверяем тип напоминания
            # type: "weekly", "date"
            if rem["type"] == "weekly":
                if str(now.weekday()) not in (rem["days_of_week"] or []):
                    continue
            if rem["type"] == "date":
                if str(now.date()) != str(rem.get("date")):
                    continue
            # Проверяем время
            rem_time = datetime.strptime(rem["time"], "%H:%M:%S").time()
            if rem_time.hour == now.hour and rem_time.minute == now.minute:
                # Отправляем напоминание
                try:
                    await bot.send_message(rem["user_id"], "⏰ Напоминание! Не забудьте отправить скриншот.")
                except Exception:
                    pass
                # Обрабатывать интервалы/повторы можно расширить тут
        await asyncio.sleep(60)
