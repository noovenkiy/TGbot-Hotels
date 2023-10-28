from telebot.handler_backends import State, StatesGroup

class UserState(StatesGroup):
    menu = State()
    history = State()
    choice_city = State()
    city_received = State()
    choice_date = State()
    check_in = State()
    check_out = State()
    choice_action = State()
    #choice_composition = State() : Количество взрослых и детей (и их возраст)
    done = State()
