from aiogram.types import Message


async def start_handler(message: Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Я помогу тебе управлять задачами:\n"
        "➕ /add — добавить\n"
        "📋 /list — активные\n"
        "✅ /completed — выполненные\n\n"
        "Меню доступно возле 📎"
    )
