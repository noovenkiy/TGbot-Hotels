from loader import bot
from states.cur_states import OrderImformation
from telebot.types import Message

@bot.message_handler(commands=['low'])
def low(message: Message) -> None:
    bot.send_message(message.chat.id, 'Введена команда low')