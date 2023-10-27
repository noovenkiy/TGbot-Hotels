from loader import bot
from states.user_states import OrderImformation
from telebot.types import Message

@bot.message_handler(commands=['custom'])
def custom(message: Message) -> None:
    bot.send_message(message.chat.id, 'Введена команда custom')