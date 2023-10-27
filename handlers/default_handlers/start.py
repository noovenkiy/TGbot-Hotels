from telebot.types import Message
from states.user_states import UserState
from loader import bot
from keyboards.reply import menu


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    bot.send_message(message.chat.id, f"Приветствую, {message.from_user.full_name}! Данный бот служит "
                          f"для просмотра информации об отелях с сайта Hotels.com", reply_markup=menu())
    bot.send_message(message.chat.id, f"Вызов справки: /help")

    bot.delete_state(message.from_user.id, message.chat.id)
    bot.set_state(message.from_user.id, UserState.menu, message.chat.id)

@bot.message_handler(content_types=['text'])
def choice(message: Message) -> None:
    if message.text == "Выбрать город посещения":
        bot.send_message(message.chat.id, "Пожалуйста, введите город, который вы хотели бы посетить.")
        bot.set_state(message.from_user.id, UserState.choice_city, message.chat.id)
    elif message.text == "История запросов":
        bot.send_message(message.chat.id, "Вот история ваших запросов:")