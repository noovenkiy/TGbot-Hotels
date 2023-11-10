from loader import bot
from handlers.custom_handlers.menu import main_menu_st1
from telebot.types import CallbackQuery, Message
from states.user_states import UserState
from keyboards.inline import calendar_keyboard
from datetime import datetime, date


@bot.message_handler(commands=['date'])
def get_date_com(message: Message) -> None:
    bot.set_state(message.from_user.id, UserState.check_in, message.chat.id)
    bot.send_message(message.chat.id, 'Дата заезда',
                     reply_markup=calendar_keyboard(date.today().year, date.today().month))


@bot.callback_query_handler(func=lambda call: call.data == '/date')
def get_date(call: CallbackQuery) -> None:
    bot.answer_callback_query(call.id)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=None)
    bot.set_state(call.from_user.id, UserState.check_in, call.message.chat.id)
    bot.send_message(call.message.chat.id, 'Дата заезда',
                     reply_markup=calendar_keyboard(date.today().year, date.today().month))


@bot.callback_query_handler(func=lambda call: call.data.startswith('date:'))
def check_date(call: CallbackQuery) -> None:
    date_current = datetime.strptime(call.data, 'date:%Y-%m-%d').date()
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    if bot.get_state(user_id, chat_id) == UserState.check_in.name:
        if date_current < date.today():
            bot.answer_callback_query(call.id, 'Дата меньше текущей', show_alert=True)
        else:
            with bot.retrieve_data(user_id, chat_id) as data:
                data['check_in'] = date_current
            bot.answer_callback_query(call.id, f'Дата заезда: {date_current}\nВыберите дату отъезда.', show_alert=True)
            bot.set_state(user_id, UserState.check_out, chat_id)
            bot.edit_message_text(f'Дата заезда: {date_current}\nДата отъезда >>>', call.message.chat.id, call.message.id,
                                  reply_markup=calendar_keyboard(date_current.year, date_current.month))
    elif bot.get_state(user_id, chat_id) == UserState.check_out.name:
        with bot.retrieve_data(user_id, chat_id) as data:
            date_check_in = data['check_in']
        if date_check_in >= date_current:
            bot.answer_callback_query(call.id, 'Дата выезда раньше заезда!', show_alert=True)
        else:
            with bot.retrieve_data(user_id, chat_id) as data:
                data['check_out'] = date_current
            bot.answer_callback_query(call.id, f'Дата выезда: {date_current}\n'
                                               f'Дней проживания: {(date_current - date_check_in).days}',
                                      show_alert=True)
            bot.set_state(user_id, UserState.menu, chat_id)
            bot.edit_message_text('Даты выбраны', call.message.chat.id, call.message.id)
            main_menu_st1(chat_id, user_id)
    else:
        bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('month:'))
def change_month(call: CallbackQuery) -> None:
    bot.answer_callback_query(call.id)
    if bot.get_state(call.from_user.id, call.message.chat.id) in [UserState.check_in.name, UserState.check_out.name]:
        year, month = map(int, call.data.replace('month:', '').split())
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=calendar_keyboard(year, month))


@bot.callback_query_handler(func=lambda call: call.data == 'empty')
def empty(call: CallbackQuery) -> None:
    bot.answer_callback_query(call.id)