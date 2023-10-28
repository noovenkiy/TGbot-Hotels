from loader import bot
from states.user_states import UserState
from telebot.types import Message
from keyboards.reply import city_choice_keyboard, city_received_keyboard
from keyboards.inline import calendar_keyboard
from utils.api_hotels import get_destination
from datetime import datetime, date

@bot.message_handler(state=UserState.choice_city)
def choice_city(message: Message):
    city_option(message, message.text)

def city_option(message: Message, city: str) -> None:
    user_id = message.from_user.id
    chat_id = message.chat.id

    cities = get_destination(city)

    if cities is None:
        bot.send_message(chat_id, 'Данные не получены. Повторите попытку позже.')
    elif cities:
        bot.set_state(user_id, UserState.city_received, chat_id)
        with bot.retrieve_data(user_id, chat_id) as data:
            data['city'] = cities
        bot.send_message(chat_id, 'Уточните нужный город', reply_markup=city_choice_keyboard(cities))
    else:
        bot.send_message(chat_id, f'По запросу "{city}" ничего не найдено.\n'
                                  f'Попробуйте еще раз.\n'
                                  f'Введите город для поиска')

@bot.message_handler(state=UserState.city_received)
def city_received(message: Message) -> None:
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, message.chat.id) as data:
        cities = data['city']

    if message.text in cities:

        with bot.retrieve_data(user_id, message.chat.id) as data:
            data['city_id'] = cities[message.text]
            data['city'] = message.text

        bot.set_state(message.from_user.id, UserState.choice_action, message.chat.id)
        bot.send_message(message.chat.id, f"Выбранный город - {message.text}", reply_markup=city_received_keyboard())

    else:
        bot.send_message(message.chat.id, "Уточните поиск", reply_markup=city_choice_keyboard(cities))

@bot.message_handler(state=UserState.choice_action)
def city_received(message: Message) -> None:
    if message.text == "Назад к выбору города":
        bot.set_state(message.from_user.id, UserState.choice_city, message.chat.id)
        bot.send_message(message.chat.id, "Укажите город для поиска")
    elif message.text == "Выбрать дату заезда":
        bot.set_state(message.from_user.id, UserState.choice_date, message.chat.id)
    else:
        bot.send_message(message.chat.id, "Выберите один из вариантов",
                         reply_markup=city_received_keyboard())