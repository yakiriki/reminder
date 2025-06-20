from aiogram import Router, types
from app.db import create_reminder, get_reminders, update_reminder, delete_reminder
from aiogram.filters import Command

router = Router()

@router.message(Command("reminder_add"))
async def reminder_add(message: types.Message):
    # Пример простого добавления еженедельного напоминания
    # В реальной версии лучше реализовать FSM для опроса пользователя!
    await message.answer(
        "Добавить напоминание:\n"
        "Формат: /reminder_add <тип> <время(HH:MM)> <дни недели через запятую (0=Пн,..6=Вс)>\n"
        "Пример: /reminder_add weekly 10:00 0,2,4"
    )
    # Подключить FSM для диалога и сохранения напоминания

@router.message(Command("reminder_edit"))
async def reminder_edit(message: types.Message):
    await message.answer("Редактирование напоминаний не реализовано (добавьте через /reminder_delete и /reminder_add).")

@router.message(Command("reminder_delete"))
async def reminder_delete_cmd(message: types.Message):
    await message.answer(
        "Удалить напоминание:\n"
        "Формат: /reminder_delete <id>\n"
        "Пример: /reminder_delete 2"
    )
    # Тут можно реализовать удаление по id напоминания

@router.message(lambda m: m.text and m.text.startswith("/reminder_add "))
async def handle_reminder_add(message: types.Message):
    try:
        _, typ, time_val, days_str = message.text.strip().split(maxsplit=3)
        days_of_week = [d.strip() for d in days_str.split(',')]
        create_reminder(
            user_id=message.from_user.id,
            type=typ,
            time=f"{time_val}:00",
            days_of_week=days_of_week
        )
        await message.answer("✅ Напоминание добавлено!")
    except Exception as e:
        await message.answer(f"Ошибка: {e}\nПример: /reminder_add weekly 10:00 0,2,4")

@router.message(lambda m: m.text and m.text.startswith("/reminder_delete "))
async def handle_reminder_delete(message: types.Message):
    try:
        _, rem_id = message.text.strip().split(maxsplit=1)
        delete_reminder(int(rem_id))
        await message.answer("✅ Напоминание удалено!")
    except Exception as e:
        await message.answer(f"Ошибка: {e}\nПример: /reminder_delete 2")