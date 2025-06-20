import httpx
import gotrue
import supabase
print("HTTPX VERSION:", httpx.__version__)
print("GOTRUE VERSION:", gotrue.__version__)
print("SUPABASE VERSION:", supabase.__version__)
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from config import Config
from filters import WhitelistMiddleware
from scheduler import reminder_scheduler

from handlers import start, info, reminder, screenshots, report, admin, errors

async def on_startup(bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/info", description="Описание команд"),
        BotCommand(command="/reminder_add", description="Добавить напоминание"),
        BotCommand(command="/reminder_edit", description="Изменить напоминание"),
        BotCommand(command="/reminder_delete", description="Удалить напоминание"),
        BotCommand(command="/report_day", description="Отчёт по скринам за день"),
        BotCommand(command="/report_week", description="Отчёт за неделю"),
        BotCommand(command="/report_month", description="Отчёт за месяц"),
        BotCommand(command="/report_user", description="Отчёт по диапазону дат"),
        BotCommand(command="/report_use", description="Отчёт за всё время"),
        BotCommand(command="/debug", description="Статистика"),
        BotCommand(command="/adduser", description="Добавить пользователя"),
        BotCommand(command="/removeuser", description="Удалить пользователя"),
        BotCommand(command="/listusers", description="Список пользователей"),
    ]
    await bot.set_my_commands(commands)

async def main():
    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware(WhitelistMiddleware())
    
    dp.include_routers(
        start.router,
        info.router,
        reminder.router,
        screenshots.router,
        report.router,
        admin.router,
        errors.router,
    )

    # Запуск планировщика напоминаний
    asyncio.create_task(reminder_scheduler(bot))

    # Запуск через webhook если задан
    if Config.WEBHOOK_URL:
        await bot.set_webhook(Config.WEBHOOK_URL)
        await dp.start_polling(bot)
    else:
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
