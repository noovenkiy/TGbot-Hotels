from telebot.handler_backends import State, StatesGroup

class UserState(StatesGroup):
    history = State()
    choice_city = State()
    city_received = State()
    check_in = State()
    check_out = State()
