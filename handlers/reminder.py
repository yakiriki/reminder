from aiogram import Router, types
from aiogram.filters import Command
from db import create_reminder, delete_reminder, update_reminder, get_reminders_by_user

router = Router()

@router.message(Command("reminder_add"))
async def reminder_add_help(message: types.Message):
    if len(message.text.strip().split()) == 1:
        await message.answer(
            "Добавить напоминание:\n"
            "Формат:\n"
            "/reminder_add weekly <HH:MM> <дни недели через запятую (0=Пн,..6=Вс)> <имя>\n"
            "/reminder_add date <HH:MM> <YYYY-MM-DD> <имя>\n"
            "Примеры:\n"
            "/reminder_add weekly 10:00 1,3,5 Утренняя проверка\n"
            "/reminder_add date 14:15 2025-06-21 День рождения"
        )
        return

@router.message(lambda m: m.text and m.text.startswith("/reminder_add ") and len(m.text.strip().split()) >= 5)
async def handle_reminder_add(message: types.Message):
    try:
        args = message.text.strip().split(maxsplit=4)
        _, typ, time_val, param, name = args
        user_id = message.from_user.id

        # поддержка имен с пробелами
        name = name.strip()

        if typ.lower() == "weekly":
            days_of_week = [d.strip() for d in param.split(',')]
            create_reminder(
                user_id=user_id,
                type=typ,
                time=f"{time_val}:00" if len(time_val) == 5 else time_val,
                days_of_week=days_of_week,
                name=name,
            )
            await message.answer("✅ Еженедельное напоминание добавлено!\nПосмотреть ID можно через /reminder_list")
        elif typ.lower() == "date":
            create_reminder(
                user_id=user_id,
                type=typ,
                time=f"{time_val}:00" if len(time_val) == 5 else time_val,
                date=param,
                name=name,
            )
            await message.answer("✅ Разовое напоминание по дате добавлено!\nПосмотреть ID можно через /reminder_list")
        else:
            await message.answer(
                "Неизвестный тип напоминания. Используйте:\n"
                "- weekly — по дням недели\n"
                "- date — по конкретной дате"
            )
    except Exception as e:
        await message.answer(f"Ошибка: {e}\nПример:\n/reminder_add weekly 10:00 0,2,4 Имя_напоминания")

@router.message(Command("reminder_list"))
async def reminder_list(message: types.Message):
    reminders = get_reminders_by_user(message.from_user.id)
    if not reminders:
        await message.answer("У вас нет активных напоминаний.")
        return
    text = "Ваши напоминания:\n"
    for rem in reminders:
        text += (
            f"ID: {rem['id']}, Имя: {rem.get('name', '(без имени)')}, "
            f"Тип: {rem['type']}, Время: {rem['time']}"
        )
        if rem["type"] == "weekly":
            text += f", Дни: {','.join(rem.get('days_of_week', []))}"
        if rem["type"] == "date":
            text += f", Дата: {rem.get('date')}"
        text += f", Подтверждено: {'Да' if rem.get('confirmed') else 'Нет'}\n"
    await message.answer(text)

@router.message(lambda m: m.text and m.text.startswith("/reminder_delete ") and len(m.text.strip().split()) == 2)
async def handle_reminder_delete(message: types.Message):
    try:
        _, rem_id = message.text.strip().split(maxsplit=1)
        delete_reminder(int(rem_id))
        await message.answer("✅ Напоминание удалено!")
    except Exception as e:
        await message.answer(f"Ошибка: {e}\nПример: /reminder_delete 2")

@router.message(Command("reminder_delete"))
async def reminder_delete_help(message: types.Message):
    await message.answer(
        "Удалить напоминание:\n"
        "Формат: /reminder_delete <id>\n"
        "ID смотрите через /reminder_list\n"
        "Пример: /reminder_delete 2"
    )

@router.message(lambda m: m.text and m.text.startswith("/reminder_edit ") and len(m.text.strip().split()) >= 4)
async def handle_reminder_edit(message: types.Message):
    try:
        _, rem_id, field, value = message.text.strip().split(maxsplit=3)
        allowed_fields = {"name", "time", "date", "type", "days_of_week"}
        if field not in allowed_fields:
            await message.answer(f"Можно менять только: {', '.join(allowed_fields)}")
            return
        if field == "days_of_week":
            value = value.split(",")
        update_reminder(int(rem_id), **{field: value})
        await message.answer("✅ Напоминание обновлено!")
    except Exception as e:
        await message.answer(f"Ошибка: {e}\nПример: /reminder_edit 2 name Новый_текст")

@router.message(Command("reminder_edit"))
async def reminder_edit_help(message: types.Message):
    await message.answer(
        "Изменить напоминание:\n"
        "Формат: /reminder_edit <id> <поле> <значение>\n"
        "Поля: name, time, date, type, days_of_week\n"
        "Пример: /reminder_edit 2 name Новое_имя"
    )
