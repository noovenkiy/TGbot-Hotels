from telebot.types import Message, CallbackQuery
from states.user_states import UserState
from keyboards.reply import city_choice_keyboard
from utils.api_hotels import get_destination
from handlers.custom_handlers.menu import main_menu_st1
from loader import bot


@bot.message_handler(commands=['city'])
def city_com(message: Message) -> None:
    bot.set_state(message.from_user.id, UserState.choice_city, message.chat.id)
    bot.send_message(message.chat.id, "Введите город для поиска")

@bot.callback_query_handler(func=lambda call: call.data == '/city')
def city_inl(call: CallbackQuery) -> None:
    bot.answer_callback_query(call.id)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=None)
    bot.set_state(call.from_user.id, UserState.choice_city, call.message.chat.id)
    bot.send_message(call.message.chat.id, 'Введите город для поиска')


@bot.message_handler(state=UserState.choice_city)
def city_rep(message: Message) -> None:
    city_options(message, message.text)


def city_options(message: Message, city: str) -> None:
    user_id = message.from_user.id
    chat_id = message.chat.id

    cities = get_destination(city)

    if cities is None:
        bot.send_message(chat_id, 'Данные не получены. Повторите попытку позже.')
    elif cities:
        bot.set_state(user_id, UserState.city_received, chat_id)
        with bot.retrieve_data(user_id, chat_id) as data:
            data['city'] = cities
        bot.send_message(chat_id, 'Уточните поиск', reply_markup=city_choice_keyboard(cities))
    else:
        bot.send_message(chat_id, f'По запросу "{city}" ничего не найдено.\n'
                                  f'Попробуйте еще раз.\n'
                                  f'Введите город для поиска >>>')


@bot.message_handler(state=UserState.city_received)
def city_received(message: Message) -> None:
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, message.chat.id) as data:
        cities = data['city']

    if message.text in cities:
        with bot.retrieve_data(user_id, message.chat.id) as data:
            data['city_id'] = cities[message.text]
            data['city'] = message.text

        bot.set_state(user_id, UserState.menu, message.chat.id)
        main_menu_st1(message.chat.id, message.from_user.id)
    else:
        bot.send_message(message.chat.id, 'Уточните поиск', reply_markup=city_choice_keyboard(cities))