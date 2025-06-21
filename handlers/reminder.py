from aiogram import Router, types
from aiogram.filters import Command
from db import create_reminder, delete_reminder

router = Router()

@router.message(lambda m: m.text and m.text.startswith("/reminder_add "))
async def handle_reminder_add(message: types.Message):
    try:
        args = message.text.strip().split(maxsplit=3)
        if len(args) < 4:
            raise ValueError("Недостаточно аргументов.")
        _, typ, time_val, param = args
        user_id = message.from_user.id

        if typ.lower() == "weekly":
            days_of_week = [d.strip() for d in param.split(',')]
            create_reminder(
                user_id=user_id,
                type=typ,
                time=f"{time_val}:00",
                days_of_week=days_of_week
            )
            await message.answer("✅ Еженедельное напоминание добавлено!")
        elif typ.lower() == "date":
            create_reminder(
                user_id=user_id,
                type=typ,
                time=f"{time_val}:00",
                date=param
            )
            await message.answer("✅ Разовое напоминание по дате добавлено!")
        else:
            await message.answer(
                "Неизвестный тип напоминания. Используйте:\n"
                "- weekly — по дням недели\n"
                "- date — по конкретной дате"
            )
    except Exception as e:
        await message.answer(f"Ошибка: {e}\nПример: /reminder_add weekly 10:00 0,2,4")

@router.message(Command("reminder_add"))
async def reminder_add_help(message: types.Message):
    await message.answer(
        "Добавить напоминание:\n"
        "Формат: /reminder_add <тип> <время(HH:MM)> <дни недели через запятую (0=Пн,..6=Вс)> или дата(YYYY-MM-DD)\n"
        "Типы:\n"
        "- weekly — по дням недели (например: 0,2,4)\n"
        "- date — по конкретной дате (например: 2025-06-21)\n"
        "Примеры:\n"
        "- /reminder_add weekly 10:00 1,3,5\n"
        "- /reminder_add date 14:15 2025-06-21"
    )

@router.message(Command("reminder_delete"))
async def reminder_delete_help(message: types.Message):
    await message.answer(
        "Удалить напоминание:\n"
        "Формат: /reminder_delete <id>\n"
        "Пример: /reminder_delete 2"
    )

@router.message(lambda m: m.text and m.text.startswith("/reminder_delete "))
async def handle_reminder_delete(message: types.Message):
    try:
        _, rem_id = message.text.strip().split(maxsplit=1)
        delete_reminder(int(rem_id))
        await message.answer("✅ Напоминание удалено!")
    except Exception as e:
        await message.answer(f"Ошибка: {e}\nПример: /reminder_delete 2")

@router.message(Command("reminder_edit"))
async def reminder_edit(message: types.Message):
    await message.answer("Редактирование напоминаний не реализовано (удалите через /reminder_delete и добавьте заново через /reminder_add).")
