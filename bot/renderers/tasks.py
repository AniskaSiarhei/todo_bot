from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from bot.database.db import Database
from bot.keyboards.inline import task_actions, completed_task_actions
from bot.utils.time_utils import is_expired

db = Database()


class TasksRenderer:

    @staticmethod
    async def show_active(message: Message, user_id: int):
        """
        Показать активные задачи
        """

        tasks = db.get_active_tasks(user_id)

        if not tasks:
            await message.answer("📭 У тебя нет активных задач")
            return

        for task_id, title, deadline in tasks:

            expired = is_expired(deadline)

            # Формируем текст
            if expired:
                text = f"🔴 {title} (просрочено)"
            elif deadline:
                text = f"🟡 {title} — до {deadline}"
            else:
                text = f"🟢 {title}"

            await message.answer(
                text,
                reply_markup=task_actions(task_id)
            )

    @staticmethod
    async def show_completed(message: Message, user_id: int):
        """
        Показать выполненные задачи
        """

        tasks = db.get_completed_tasks(user_id)

        if not tasks:
            await message.answer("📭 Выполненных задач пока нет")
            return

        for task_id, title in tasks:
            await message.answer(
                f"✅ {title}",
                reply_markup=completed_task_actions(task_id)
            )

    @staticmethod
    async def task_restored(message: Message):

        try:
            await message.edit_text("↩️ Задача восстановлена")
            await message.edit_reply_markup(None)

        except TelegramBadRequest:
            pass

    @staticmethod
    async def task_deleted(message: Message):

        try:
            await message.edit_text("🗑 Задача удалена")
            await message.edit_reply_markup(None)

        except TelegramBadRequest:
            pass

    @staticmethod
    async def task_done(message: Message):

        try:
            await message.edit_text("✅ Задача выполнена")
            await message.edit_reply_markup(None)

        except TelegramBadRequest:
            # Сообщение уже такое — игнорируем
            pass
