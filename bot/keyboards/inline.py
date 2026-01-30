from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Добавить задачу", callback_data="add_task"),
            InlineKeyboardButton(text="📋 Список задач", callback_data="list_tasks")
        ]
    ])
