from aiogram.fsm.state import StatesGroup, State

class StepsTimeHand(StatesGroup):
    GET_ID = State()
    GET_TIME = State()
    CHECK_DATA = State()
    GET_ONLY_ID = State()


class StepsTimeAuto(StatesGroup):
    GET_ID = State()
    GET_START = State()
    GET_FINISH = State()
    CONFIRM_KB = State()
    TIME_MENU = State()


class Help(StatesGroup):
    GET_HELP = State()
    SEND_HELP_ADMIN = State()

class SendProtocol(StatesGroup):
    SEND_PROTOCOL = State()