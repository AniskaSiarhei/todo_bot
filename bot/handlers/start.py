from aiogram.types import Message
from aiogram.filters import CommandStart

from bot.keyboards.inline import main_menu


async def start_handler(message: Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Я бот для управления задачами.\n"
        "Выбирай действие 👇",
        reply_markup=main_menu()
    )
