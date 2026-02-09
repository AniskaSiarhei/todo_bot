from aiogram.fsm.state import State, StatesGroup


class AddTaskState(StatesGroup):
    waiting_for_text = State()


class EditTaskState(StatesGroup):
    waiting_for_text = State()
