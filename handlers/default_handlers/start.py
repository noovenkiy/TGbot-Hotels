from telebot.types import Message
from states.user_states import UserState
from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    bot.send_message(message.chat.id, f"Приветствую, {message.from_user.full_name}! Данный бот служит "
                          f"для просмотра информации об отелях с сайта Hotels.com")
    bot.send_message(message.chat.id, f"Вызов справки: /help")

    bot.delete_state(message.from_user.id, message.chat.id)
    bot.set_state(message.from_user.id, UserState.done, message.chat.id)
