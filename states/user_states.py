from telebot.handler_backends import State, StatesGroup

class UserState(StatesGroup):
    menu = State()
    choice_city = State()
    city_received = State()
    choice_date = State()
    date_received = State()
    #choice_composition = State() : Количество взрослых и детей (и их возраст)
    done = State()
