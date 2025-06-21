from aiogram import Router, types
from datetime import datetime, timedelta
from db import get_screenshots
from aiogram.filters import Command

router = Router()

def format_report(screens):
    if not screens:
        return "Нет скриншотов за выбранный период."
    txt = "Скриншоты:\n"
    for item in screens:
        txt += f"- {item['added_at'][:19]}: [ссылка]({item['file_url']})\n"
    return txt

@router.message(Command("report_day"))
async def report_day(message: types.Message):
    try:
        now = datetime.utcnow()
        date_from = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        date_to = now.isoformat()
        screens = get_screenshots(user_id=message.from_user.id, date_from=date_from, date_to=date_to)
        await message.answer(format_report(screens), parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

@router.message(Command("report_week"))
async def report_week(message: types.Message):
    try:
        now = datetime.utcnow()
        date_from = (now - timedelta(days=7)).isoformat()
        date_to = now.isoformat()
        screens = get_screenshots(user_id=message.from_user.id, date_from=date_from, date_to=date_to)
        await message.answer(format_report(screens), parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

@router.message(Command("report_month"))
async def report_month(message: types.Message):
    try:
        now = datetime.utcnow()
        date_from = (now - timedelta(days=30)).isoformat()
        date_to = now.isoformat()
        screens = get_screenshots(user_id=message.from_user.id, date_from=date_from, date_to=date_to)
        await message.answer(format_report(screens), parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

@router.message(Command("report_use"))
async def report_use(message: types.Message):
    try:
        screens = get_screenshots(user_id=message.from_user.id)
        await message.answer(format_report(screens), parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

@router.message(Command("report_user"))
async def report_user(message: types.Message):
    await message.answer("Используйте: /report_user <user_id> <YYYY-MM-DD> <YYYY-MM-DD>\nПример: /report_user 123456789 2025-06-01 2025-06-21")

@router.message(lambda m: m.text and m.text.startswith("/report_user ") and len(m.text.split()) == 4)
async def report_user_args(message: types.Message):
    try:
        _, user_id, date_from, date_to = message.text.split()
        screens = get_screenshots(user_id=int(user_id), date_from=date_from, date_to=date_to)
        await message.answer(format_report(screens), parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"Ошибка: {e}\nФормат: /report_user <user_id> <YYYY-MM-DD> <YYYY-MM-DD>")
