from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from bot.database.db import Database
from bot.keyboards.inline import (task_actions,
                                  main_menu,
                                  completed_tasks_menu, completed_task_actions)
from bot.renderers.tasks import TasksRenderer

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
    )
    await state.clear()


async def list_tasks_callback(callback: CallbackQuery):
    await TasksRenderer.show_active(
        callback.message,
        callback.from_user.id
    )

    await callback.answer()


async def completed_tasks_callback(callback: CallbackQuery):
    await TasksRenderer.show_completed(
        callback.message,
        callback.from_user.id
    )

    await callback.answer()


# Обработчик ✔️ «выполнено
async def mark_done_callback(callback: CallbackQuery):
    task_id = int(callback.data.split(":")[1])

    db.mark_done(task_id, callback.from_user.id)

    await TasksRenderer.task_done(callback.message)
    await callback.answer("✅ Готово")


async def restore_task_callback(callback: CallbackQuery):
    task_id = int(callback.data.split(":")[1])

    db.restore_task(task_id, callback.from_user.id)

    await TasksRenderer.task_restored(callback.message)

    await callback.answer("↩️ Восстановлено")


# Обработчик ❌ «удалить»
async def delete_task_callback(callback: CallbackQuery):
    task_id = int(callback.data.split(":")[1])

    db.delete_task(task_id, callback.from_user.id)

    await TasksRenderer.task_deleted(callback.message)
    await callback.answer("🗑 Удалено")


async def delete_completed_tasks_callback(callback: CallbackQuery):
    db.delete_completed_tasks(callback.from_user.id)

    await callback.message.edit_text("🧹 Выполненные задачи удалены")
    await callback.answer()


# /list
async def list_tasks_command(message: Message):
    tasks = db.get_active_tasks(message.from_user.id)

    if not tasks:
        await message.answer(
            "🎉 У тебя нет активных задач!",
        )
        return

    await message.answer("📋 *Активные задачи:*", parse_mode="Markdown")

    for task_id, title in tasks:
        await message.answer(
            f"⬜ {title}",
            reply_markup=task_actions(task_id)
        )


# /completed
async def completed_tasks_command(message: Message):
    tasks = db.get_completed_tasks(message.from_user.id)

    if not tasks:
        await message.answer("📭 Выполненных задач пока нет")
        return

    await message.answer("✅ *Выполненные задачи:*", parse_mode="Markdown")

    for task_id, title in tasks:
        await message.answer(
            f"✅ {title}",
            reply_markup=completed_task_actions(task_id)
        )

    await message.answer(
        "Можно удалить выполненные задачи 👇",
        reply_markup=completed_tasks_menu()
    )


# /menu
async def menu_command(message: Message):
    await message.answer(
        "🏠 Главное меню",
        reply_markup=main_menu()
    )
