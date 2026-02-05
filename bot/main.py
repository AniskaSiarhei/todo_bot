import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

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
    completed_tasks_callback, delete_completed_tasks_callback, main_menu_callback, restore_task_callback
)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # ===== MESSAGE HANDLERS =====
    dp.message.register(start_handler, Command("start"))
    dp.message.register(add_task_command, Command("add"))
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
        main_menu_callback,
        lambda c: c.data == "main_menu"
    )


    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())