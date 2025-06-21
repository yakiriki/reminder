from aiogram import Router, types

router = Router()

@router.errors()
async def error_handler(event, exception):
    # Общий обработчик ошибок
    return True
