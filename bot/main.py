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
    AddTask
)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.register(start_handler, Command("start"))
    dp.message.register(add_task_command, Command("add"))
    dp.message.register(save_task, AddTask.waiting_for_title)

    dp.callback_query.register(add_task_callback, lambda c: c.data == "add_task")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
