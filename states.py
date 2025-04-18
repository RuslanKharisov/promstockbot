# states.py
from aiogram.fsm.state import State, StatesGroup


class ApiRequestState(StatesGroup):
    awaiting_contact = State()
