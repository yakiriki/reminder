from aiogram import Router, types

router = Router()

@router.message(commands=["info"])
async def cmd_info(message: types.Message):
    text = (
        "Справка по командам:\n"
        "/reminder_add — Добавить напоминание (по дням недели/датам/времени)\n"
        "/reminder_edit — Изменить напоминание\n"
        "/reminder_delete — Удалить напоминание\n"
        "/report_day — Отчёт по скринам за день\n"
        "/report_week — Отчёт за неделю\n"
        "/report_month — Отчёт за месяц\n"
        "/report_user — Отчёт по выбранному диапазону дат\n"
        "/report_use — Отчёт за всё время\n"
        "/debug — Показать статистику\n"
        "/adduser — Добавить пользователя (только для админа)\n"
        "/removeuser — Удалить пользователя (только для админа)\n"
        "/listusers — Показать разрешённых пользователей\n"
    )
    await message.answer(text)