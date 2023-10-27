from loader import bot
from states.user_states import UserState
from telebot.types import Message

@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    bot.send_message(message.chat.id, 'Введена команда history')