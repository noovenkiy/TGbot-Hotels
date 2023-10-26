from telebot.handler_backends import State, StatesGroup

class OrderImformation(StatesGroup):
    country = State()
    num_of_ppl = State()
    date = State()


