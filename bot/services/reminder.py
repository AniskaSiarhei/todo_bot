import asyncio
import logging
from datetime import datetime

from bot.database.db import Database


db = Database()


async def deadline_watcher(bot):
    """
    Проверяет дедлайны каждые 60 секунд
    """

    logging.info("⏰ Deadline watcher запущен")

    while True:

        now = datetime.now()

        tasks = db.get_tasks_with_deadline()

        for task_id, user_id, title, deadline in tasks:

            if not deadline:
                continue

            deadline_dt = datetime.fromisoformat(deadline)

            # Если срок наступил или прошёл
            if deadline_dt <= now:

                try:
                    await bot.send_message(
                        user_id,
                        f"⏰ Срок задачи истёк!\n\n📌 {title}"
                    )

                    # Чтобы не спамил — убираем deadline
                    # db.set_deadline(task_id, user_id, None)

                except Exception as e:
                    logging.error(f"Notify error: {e}")

        await asyncio.sleep(60)
