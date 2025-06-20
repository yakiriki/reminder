from aiogram import Router, types

router = Router()

from aiogram.filters import Command

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    text = (
        "👋 Привет! Это бот для напоминаний и отправки скринов.\n\n"
        "Доступные команды:\n"
        "/info — Справка по командам\n"
        "/reminder_add — Добавить напоминание\n"
        "/reminder_edit — Изменить напоминание\n"
        "/reminder_delete — Удалить напоминание\n"
        "/report_day — Отчёт за день\n"
        "/report_week — Отчёт за неделю\n"
        "/report_month — Отчёт за месяц\n"
        "/report_user — Отчёт по диапазону дат\n"
        "/report_use — Отчёт за всё время\n"
        "/debug — Статистика\n"
        "/adduser — Добавить пользователя\n"
        "/removeuser — Удалить пользователя\n"
        "/listusers — Список пользователей\n"
    )
    await message.answer(text)
