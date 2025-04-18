# states/api_request.py
# 🔹 Состояния FSM.
#
from aiogram.fsm.state import State, StatesGroup


class ApiRequestState(StatesGroup):
    waiting_for_contact = State()
