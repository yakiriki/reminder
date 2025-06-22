from aiogram import BaseMiddleware
from aiogram.types import Message
from db import get_user, add_user
from config import Config

class WhitelistMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = event.from_user.id if hasattr(event, "from_user") else None
        if not user_id:
            return await handler(event, data)
        user = get_user(user_id)
        # Первый запуск — только админ
        if user_id == Config.ADMIN_USER_ID:
            if not user:
                get_user(user_id) or add_user(user_id, event.from_user.username, True)
            return await handler(event, data)
        # Остальные только если есть в базе
        if not user:
            await event.answer("Доступ запрещён. Обратитесь к администратору.")
            return None      # <--- ЯВНОЕ ЗАВЕРШЕНИЕ CHAIN
        return await handler(event, data)
