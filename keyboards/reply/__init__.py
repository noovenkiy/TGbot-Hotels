from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def city_choice_keyboard(cities: dict) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, one_time_keyboard=True, row_width=1)
    keyboard.add(*[KeyboardButton(city) for city in cities])
    return keyboard
