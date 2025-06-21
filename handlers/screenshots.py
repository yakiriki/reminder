from aiogram import Router, types
from db import upload_file, add_screenshot, get_reminders_by_user, confirm_reminder

router = Router()

@router.message(lambda m: m.photo)
async def handle_photo(message: types.Message):
    largest = message.photo[-1]
    file = await message.bot.get_file(largest.file_id)
    file_bytes = await message.bot.download_file(file.file_path)
    filename = f"{message.from_user.id}_{largest.file_unique_id}.png"
    public_url = upload_file(file_bytes.read(), filename)
    if public_url:
        add_screenshot(message.from_user.id, public_url)
        await message.answer(f"✅ Скриншот сохранён!\n[Посмотреть]({public_url})", parse_mode="Markdown")
    else:
        await message.answer("Ошибка загрузки скриншота.")

@router.message(lambda m: m.document and m.document.mime_type and m.document.mime_type.startswith("image/"))
async def handle_image_doc(message: types.Message):
    file = await message.bot.get_file(message.document.file_id)
    file_bytes = await message.bot.download_file(file.file_path)
    filename = f"{message.from_user.id}_{message.document.file_unique_id}.png"
    public_url = upload_file(file_bytes.read(), filename)
    if public_url:
        add_screenshot(message.from_user.id, public_url)
        await message.answer(f"✅ Скриншот сохранён!\n[Посмотреть]({public_url})", parse_mode="Markdown")
    else:
        await message.answer("Ошибка загрузки скриншота.")

@router.message()
async def any_message(message: types.Message):
    reminders = get_reminders_by_user(message.from_user.id)
    for rem in reminders:
        if not rem.get("confirmed", False):
            confirm_reminder(rem["id"])
            await message.answer(f"✅ Напоминание '{rem.get('name', '(без имени)')}' подтверждено!")
