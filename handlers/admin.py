from aiogram import Router, types
from db import add_user, remove_user, list_users, get_stats
from config import Config
from aiogram.filters import Command

router = Router()

@router.message(Command("adduser"))
async def add_user_cmd(message: types.Message):
    if message.from_user.id != Config.ADMIN_USER_ID:
        await message.answer("Только админ может добавлять пользователей.")
        return
    try:
        await message.answer("Отправьте user_id нового пользователя (или пересланное сообщение от пользователя).")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

@router.message(Command("removeuser"))
async def remove_user_cmd(message: types.Message):
    if message.from_user.id != Config.ADMIN_USER_ID:
        await message.answer("Только админ может удалять пользователей.")
        return
    await message.answer("Отправьте user_id пользователя для удаления.")

@router.message(lambda m: m.reply_to_message and m.from_user.id == Config.ADMIN_USER_ID)
async def handle_add_remove(message: types.Message):
    try:
        user_id = message.reply_to_message.from_user.id
        username = message.reply_to_message.from_user.username or "unknown"
        if message.text.startswith("/adduser"):
            await add_user(user_id, username)
            await message.answer("Пользователь добавлен!")
        elif message.text.startswith("/removeuser"):
            await remove_user(user_id)
            await message.answer("Пользователь удалён!")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

@router.message(Command("listusers"))
async def list_users_cmd(message: types.Message):
    users = await list_users()
    if not users:
        await message.answer("Нет разрешённых пользователей.")
        return
    txt = "Разрешённые пользователи:\n"
    for u in users:
        txt += f"- {u['user_id']} ({u['username']}) {'[admin]' if u['is_admin'] else ''}\n"
    await message.answer(txt)

@router.message(Command("debug"))
async def debug_cmd(message: types.Message):
    stats = await get_stats()
    await message.answer(
        f"Статистика:\n"
        f"- Сохранено скриншотов: {stats['screenshots']}\n"
        f"- Напоминаний: {stats['reminders']}\n"
        f"- Ответов на напоминания: {stats['responses']}"
    )
