from loader import bot
from states.user_states import UserState
from telebot.types import Message
from keyboards.reply import city_choice
from utils.api_hotels import get_destination

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
        bot.send_message(chat_id, 'Уточните нужный город', reply_markup=city_choice(cities))
    else:
        bot.send_message(chat_id, f'По запросу "{city}" ничего не найдено.\n'
                                  f'Попробуйте еще раз.\n'
                                  f'Введите город для поиска')

