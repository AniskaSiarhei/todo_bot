from aiogram.types import Message

from bot.keyboards.inline import main_menu


async def start_handler(message: Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Я помогу тебе управлять задачами:\n"
        "➕ добавлять\n"
        "📋 просматривать\n"
        "✔️ выполнять\n"
        "❌ удалять\n\n"
        "Выбери действие 👇",
        reply_markup=main_menu()
    )
