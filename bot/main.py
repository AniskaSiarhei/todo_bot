import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
import logging

from bot.config import BOT_TOKEN
from bot.handlers.start import start_handler
from bot.handlers.tasks import (
    add_task_command,
    add_task_callback,
    save_task,
    AddTask,
    list_tasks_callback,
    mark_done_callback,
    delete_task_callback,
    completed_tasks_callback, delete_completed_tasks_callback,
    # main_menu_callback,
    restore_task_callback,
    list_tasks_command, completed_tasks_command, menu_command, edit_task_callback, save_edited_task,
    cancel_edit_callback, deadline_callback, save_deadline, db
)
from bot.states.task import EditTaskState, DeadlineState

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    logging.info("🤖 Бот успешно запущен!")

    # ===== MESSAGE HANDLERS =====
    dp.message.register(start_handler, Command("start"))
    dp.message.register(add_task_command, Command("add"))
    dp.message.register(list_tasks_command, Command("list"))
    dp.message.register(completed_tasks_command, Command("completed"))
    dp.message.register(menu_command, Command("menu"))

    dp.message.register(save_task, AddTask.waiting_for_title)

    # ===== CALLBACK HANDLERS =====
    dp.callback_query.register(
        add_task_callback,
        lambda c: c.data == "add_task"
    )

    dp.callback_query.register(
        list_tasks_callback,
        lambda c: c.data == "list_tasks"
    )

    dp.callback_query.register(
        mark_done_callback,
        lambda c: c.data.startswith("done:")
    )

    dp.callback_query.register(
        delete_task_callback,
        lambda c: c.data.startswith("delete:")
    )

    dp.callback_query.register(
        completed_tasks_callback,
        lambda c: c.data == "completed_tasks"
    )


    dp.callback_query.register(
        delete_completed_tasks_callback,
        lambda c: c.data == "delete_completed_tasks"
    )

    dp.callback_query.register(
        restore_task_callback,
        lambda c: c.data.startswith("restore:")
    )

    dp.callback_query.register(
        edit_task_callback,
        lambda c: c.data.startswith("edit:")
    )

    dp.message.register(
        save_edited_task,
        EditTaskState.waiting_for_text
    )

    dp.callback_query.register(
        cancel_edit_callback,
        lambda c: c.data == "cancel_edit"
    )

    dp.callback_query.register(
        deadline_callback,
        lambda c: c.data.startswith("deadline:")
    )

    dp.message.register(
        save_deadline,
        DeadlineState.waiting_for_date
    )

    await dp.start_polling(bot)

async def deadline_checker(bot: Bot):

    while True:

        tasks = db.get_tasks_with_deadline()

        now = datetime.now()

        for task_id, user_id, title, deadline in tasks:

            dt = datetime.fromisoformat(deadline)

            if dt <= now:

                await bot.send_message(
                    user_id,
                    f"⏰ Напоминание!\n\n{title}"
                )

                # Убираем deadline чтобы не спамить
                db.set_deadline(task_id, user_id, None)

        await asyncio.sleep(30)  # каждые 30 сек


if __name__ == "__main__":
    asyncio.run(main())