from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from bot.database.db import Database
from bot.keyboards.inline import task_actions, main_menu, completed_tasks_menu

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
    title = message.text.strip()

    if not title:
        await message.answer("⚠️ Задача не может быть пустой. Напиши текст:")
        return

    db.add_task(message.from_user.id, title)

    await message.answer(
        "✅ Задача добавлена!",
        reply_markup=main_menu()
    )
    await state.clear()


async def list_tasks_callback(callback: CallbackQuery):
    tasks = db.get_active_tasks(callback.from_user.id)

    if not tasks:
        await callback.message.answer(
            "🎉 У тебя нет активных задач!",
            reply_markup=main_menu()
        )
        await callback.answer()
        return

    await callback.message.answer("📋 *Активные задачи:*", parse_mode="Markdown")

    for task_id, title in tasks:
        await callback.message.answer(
            f"⬜ {title}",
            reply_markup=task_actions(task_id)
        )

    await callback.message.answer(
        "Что делаем дальше? 👇",
        reply_markup=main_menu()
    )

    await callback.answer()


# Обработчик ✔️ «выполнено
async def mark_done_callback(callback: CallbackQuery):
    task_id = int(callback.data.split(":")[1])

    db.mark_done(task_id, callback.from_user.id)

    await callback.message.edit_text("✅ Задача выполнена и перенесена")
    await callback.message.answer(
        "Отлично 💪 Она теперь в разделе «Выполненные»",
        reply_markup=main_menu()
    )
    await callback.answer()


# Обработчик ❌ «удалить»
async def delete_task_callback(callback: CallbackQuery):
    task_id = int(callback.data.split(":")[1])

    db.delete_task(task_id, callback.from_user.id)

    await callback.message.edit_text("❌ Задача удалена")
    await callback.message.answer(
        "Задачу убрали 🧹 Что дальше?",
        reply_markup=main_menu()
    )
    await callback.answer()


async def completed_tasks_callback(callback: CallbackQuery):
    tasks = db.get_completed_tasks(callback.from_user.id)

    if not tasks:
        await callback.message.answer(
            "📭 Выполненных задач пока нет",
            reply_markup=main_menu()
        )
        await callback.answer()
        return

    await callback.message.answer("✅ *Выполненные задачи:*", parse_mode="Markdown")

    for task_id, title in tasks:
        await callback.message.answer(
            f"✅ {title}",
            reply_markup=task_actions(task_id)
        )

    await callback.message.answer(
        "Можно удалить выполненные задачи 👇",
        reply_markup=completed_tasks_menu()
    )

    await callback.answer()


async def delete_completed_tasks_callback(callback: CallbackQuery):
    db.delete_completed_tasks(callback.from_user.id)

    await callback.message.edit_text("🧹 Выполненные задачи удалены")
    await callback.message.answer(
        "Готово! Что дальше? 👇",
        reply_markup=main_menu()
    )
    await callback.answer()

async def restore_task_callback(callback: CallbackQuery):
    task_id = int(callback.data.split(":")[1])

    db.restore_task(task_id, callback.from_user.id)

    await callback.message.edit_text("↩️ Задача восстановлена")
    await callback.message.answer(
        "Она снова в активных задачах 👍",
        reply_markup=main_menu()
    )
    await callback.answer()

async def main_menu_callback(callback: CallbackQuery):
    await callback.message.answer(
        "Выбери действие 👇",
        reply_markup=main_menu()
    )
    await callback.answer()