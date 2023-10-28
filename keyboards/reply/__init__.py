from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = KeyboardButton("Выбрать город посещения")
    btn2 = KeyboardButton("История запросов")
    keyboard.add(btn1, btn2)
    return keyboard

def city_choice_keyboard(cities: dict) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, one_time_keyboard=True, row_width=1)
    keyboard.add(*[KeyboardButton(city) for city in cities])
    return keyboard

def city_received_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, one_time_keyboard=True, row_width=2)
    btn1 = KeyboardButton("Выбрать дату заезда")
    btn2 = KeyboardButton("Назад к выбору города")
    keyboard.add(btn1, btn2)
    return keyboard

def date_received_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, one_time_keyboard=True, row_width=2)
    btn1 = KeyboardButton("Изменить город")
    btn2 = KeyboardButton("Изменить даты")
    btn3 = KeyboardButton("Показать результаты")
    keyboard.add(btn1, btn2, btn3)
    return keyboard