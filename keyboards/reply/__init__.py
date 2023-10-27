from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Выбрать город посещения")
    btn2 = KeyboardButton("История запросов")
    keyboard.add(btn1, btn2)
    return keyboard

def city_choice(cities: dict) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, one_time_keyboard=True, row_width=1)
    keyboard.add(*[KeyboardButton(city) for city in cities])
    return keyboard