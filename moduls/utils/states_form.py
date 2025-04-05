from aiogram.fsm.state import StatesGroup, State

class StepsTimeHand(StatesGroup):
    GET_ID = State()
    GET_TIME = State()
    CHECK_DATA = State()
    GET_ONLY_ID = State()