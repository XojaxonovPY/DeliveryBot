from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    lang=State()
    quantity=State()