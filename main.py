import httpx
import gotrue
import supabase
import asyncio
import logging
import os

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from config import Config
from filters import WhitelistMiddleware
from scheduler import reminder_scheduler

from handlers import start, info, reminder, screenshots, report, admin, errors

print("HTTPX VERSION:", httpx.__version__)
print("GOTRUE VERSION:", gotrue.__version__)
print("SUPABASE VERSION:", supabase.__version__)

API_TOKEN = Config.BOT_TOKEN
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "change-this-secret")
WEB_SERVER_HOST = Config.APP_HOST
WEB_SERVER_PORT = int(os.getenv("PORT", Config.APP_PORT))

async def on_startup(bot: Bot):
    hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
    if not hostname and Config.WEBHOOK_URL:
        webhook_url = f"{Config.WEBHOOK_URL}{WEBHOOK_PATH}"
    elif hostname:
        webhook_url = f"https://{hostname}{WEBHOOK_PATH}"
    else:
        raise RuntimeError("WEBHOOK_URL or RENDER_EXTERNAL_HOSTNAME is not set!")
    await bot.set_webhook(webhook_url, secret_token=WEBHOOK_SECRET)
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
    print(f"Webhook set to {webhook_url}")

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=API_TOKEN)
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

    asyncio.create_task(reminder_scheduler(bot))

    app = web.Application()
    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    ).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    app.on_startup.append(lambda app: on_startup(bot))
    app.on_shutdown.append(lambda app: on_shutdown(bot))

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, WEB_SERVER_HOST, WEB_SERVER_PORT)
    await site.start()
    print(f"Server started on {WEB_SERVER_HOST}:{WEB_SERVER_PORT}")

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
