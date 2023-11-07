from telebot.types import Message
from states.user_states import UserState
from loader import bot
from handlers.custom_handlers.menu import main_menu_st1


@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.send_message(chat_id, f"Приветствую, {message.from_user.first_name}")
    bot.send_message(chat_id, "Для вызова справки /help")
    bot.send_message(chat_id, "Здесь можно посмотреть информацию от отелях с сайта Hotels.com")

    bot.delete_state(user_id, chat_id)
    bot.set_state(user_id, UserState.menu, chat_id)

    main_menu_st1(message.chat.id, message.from_user.id)
