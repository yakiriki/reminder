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
    print("/report_day сработал")
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
    print("/report_week сработал")
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
    print("/report_month сработал")
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
    print("/report_use сработал")
    try:
        screens = get_screenshots(user_id=message.from_user.id)
        await message.answer(format_report(screens), parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

@router.message(Command("report_user"))
async def report_user(message: types.Message):
    print("/report_user сработал")
    parts = message.text.strip().split()
    if len(parts) == 1:
        await message.answer("Используйте: /report_user <user_id> <YYYY-MM-DD> <YYYY-MM-DD>\nПример: /report_user 123456789 2025-06-01 2025-06-21")
        return
    if len(parts) == 4:
        try:
            _, user_id, date_from, date_to = parts
            screens = get_screenshots(user_id=int(user_id), date_from=date_from, date_to=date_to)
            await message.answer(format_report(screens), parse_mode="Markdown")
        except Exception as e:
            await message.answer(f"Ошибка: {e}\nФормат: /report_user <user_id> <YYYY-MM-DD> <YYYY-MM-DD>")
    else:
        await message.answer("Неверное количество аргументов.\nФормат: /report_user <user_id> <YYYY-MM-DD> <YYYY-MM-DD>")
