from telebot.types import Message, CallbackQuery
from states.user_states import UserState
from keyboards.inline import main_menu_st1_keyboard, main_menu_st2_keyboard
from loader import bot


@bot.message_handler(commands=['menu'])
def menu_com(message: Message) -> None:
    main_menu_st1(message)


@bot.message_handler(func=lambda message: message.text == "Меню")
def menu_repl(message: Message) -> None:
    main_menu_st1(message)


@bot.callback_query_handler(func=lambda call: call.data == 'back')
def back_to_st1(call: CallbackQuery) -> None:
    chat_id = call.message.chat.id
    user_id = call.message.from_user.id

    if isinstance(call, CallbackQuery):
        bot.edit_message_reply_markup(chat_id, call.message.id, reply_markup=main_menu_st1_keyboard())
    else:
        with bot.retrieve_data(user_id, chat_id) as data:
            city = data.get('city', "Не выбран")
            check_in = data.get('check_in', "Не выбрана")
            check_out = data.get('check_out', "Не выбрана")
            if not isinstance(check_in, str) and not isinstance(check_out, str):
                amount_days = (data['check_out'] - data['check_in']).days
            else:
                amount_days = 0
        bot.send_message(chat_id, f"Выбранный город:\t{city}\n"
                                  f"Дата заезда:\t{check_in}\n"
                                  f"Дата отъезда:\t{check_out}\n"
                                  f"Всего дней:\t{amount_days}", reply_markup=main_menu_st1_keyboard())


def main_menu_st1(message: Message) -> None:
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        city = data.get('city', "Не выбран")
        check_in = data.get('check_in', "Не выбрана")
        check_out = data.get('check_out', "Не выбрана")
        if not isinstance(check_in, str) and not isinstance(check_out, str):
            amount_days = (data['check_out'] - data['check_in']).days
        else:
            amount_days = 0

    bot.send_message(chat_id, f"Выбранный город:\t{city}\n"
                              f"Дата заезда:\t{check_in}\n"
                              f"Дата отъезда:\t{check_out}\n"
                              f"Всего дней:\t{amount_days}", reply_markup=main_menu_st1_keyboard())


@bot.callback_query_handler(func=lambda call: call.data == 'next')
def main_menu_st2(call: CallbackQuery) -> None:
    chat_id = call.message.chat.id
    user_id = call.message.from_user.id

    if isinstance(call, CallbackQuery):
        bot.edit_message_reply_markup(chat_id, call.message.id, reply_markup=main_menu_st2_keyboard())
    else:
        with bot.retrieve_data(user_id, chat_id) as data:
            city = data.get('city', "Не выбран")
            check_in = data.get('check_in', "Не выбрана")
            check_out = data.get('check_out', "Не выбрана")
            if not isinstance(check_in, str) and not isinstance(check_out, str):
                amount_days = (data['check_out'] - data['check_in']).days
            else:
                amount_days = 0
        bot.send_message(chat_id, f"Выбранный город:\t{city}\n"
                                  f"Дата заезда:\t{check_in}\n"
                                  f"Дата отъезда:\t{check_out}\n"
                                  f"Всего дней:\t{amount_days}", reply_markup=main_menu_st2_keyboard())

