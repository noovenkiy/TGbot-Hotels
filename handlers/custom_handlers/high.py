from loader import bot
from states.OrderImformation import OrderImformation
from telebot.types import Message

@bot.message_handler(commands=['high'])
def high(message: Message) -> None:
    bot.send_message(message.chat.id, 'Введена команда high')