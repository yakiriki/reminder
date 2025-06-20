from aiogram import Router, types
from datetime import datetime, timedelta
from app.db import get_screenshots

router = Router()

def format_report(screens):
    if not screens:
        return "Нет скриншотов за выбранный период."
    txt = "Скриншоты:\n"
    for item in screens:
        txt += f"- {item['added_at'][:19]}: [ссылка]({item['file_url']})\n"
    return txt

@router.message(commands=["report_day"])
async def report_day(message: types.Message):
    now = datetime.utcnow()
    date_from = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    date_to = now.isoformat()
    screens = get_screenshots(user_id=message.from_user.id, date_from=date_from, date_to=date_to)
    await message.answer(format_report(screens), parse_mode="Markdown")

@router.message(commands=["report_week"])
async def report_week(message: types.Message):
    now = datetime.utcnow()
    date_from = (now - timedelta(days=7)).isoformat()
    date_to = now.isoformat()
    screens = get_screenshots(user_id=message.from_user.id, date_from=date_from, date_to=date_to)
    await message.answer(format_report(screens), parse_mode="Markdown")

@router.message(commands=["report_month"])
async def report_month(message: types.Message):
    now = datetime.utcnow()
    date_from = (now - timedelta(days=30)).isoformat()
    date_to = now.isoformat()
    screens = get_screenshots(user_id=message.from_user.id, date_from=date_from, date_to=date_to)
    await message.answer(format_report(screens), parse_mode="Markdown")

@router.message(commands=["report_use"])
async def report_use(message: types.Message):
    screens = get_screenshots(user_id=message.from_user.id)
    await message.answer(format_report(screens), parse_mode="Markdown")