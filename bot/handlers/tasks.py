from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from bot.database.db import Database

db = Database()


class AddTask(StatesGroup):
    waiting_for_title = State()


# /add
async def add_task_command(message: Message, state: FSMContext):
    await message.answer("✏️ Напиши текст задачи:")
    await state.set_state(AddTask.waiting_for_title)


# кнопка ➕
async def add_task_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("✏️ Напиши текст задачи:")
    await state.set_state(AddTask.waiting_for_title)
    await callback.answer()


# текст задачи
async def save_task(message: Message, state: FSMContext):
    db.add_task(message.from_user.id, message.text)
    await message.answer("✅ Задача добавлена!")
    await state.clear()
