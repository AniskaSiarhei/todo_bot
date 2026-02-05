from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Добавить задачу", callback_data="add_task"),
        ],
        [
            InlineKeyboardButton(text="📋 Активные задачи", callback_data="list_tasks"),
            InlineKeyboardButton(text="✅ Выполненные", callback_data="completed_tasks"),
        ]
    ])

def task_actions(task_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✔️", callback_data=f"done:{task_id}"),
            InlineKeyboardButton(text="❌", callback_data=f"delete:{task_id}")
        ]
    ])

def completed_tasks_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🗑️ Удалить выполненные", callback_data="delete_completed_tasks")
        ],
        [
            InlineKeyboardButton(text="⬅️ В меню", callback_data="main_menu")
        ]
    ])
