import telebot
from telebot.types import Message
from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
    bot.send_message(message.chat.id, 'Приветствую вас!\nЯ буду повторять все сообщения за вами.')

@bot.message_handler()
def reply(message: Message) -> None:
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling()


