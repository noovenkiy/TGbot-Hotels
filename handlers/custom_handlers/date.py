from loader import bot
from telebot.types import CallbackQuery, Message
from keyboards.inline import calendar_keyboard
from keyboards.reply import date_received_keyboard
from states.user_states import UserState
from datetime import datetime, date

@bot.message_handler(state=UserState.choice_date)
def choice_date(message: Message) -> None:
    bot.set_state(message.from_user.id, UserState.check_in, message.chat.id)
    bot.send_message(message.chat.id, "Выберите дату заезда",
                     reply_markup=calendar_keyboard(date.today().year, date.today().month))

@bot.message_handler(state=UserState.check_in)
def date_in(call: CallbackQuery) -> None:
    bot.answer_callback_query(call.id)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=None)


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
            bot.edit_message_text(f'Дата заезда: {date_current}\nДата отъезда', call.message.chat.id, call.message.id,
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
            bot.edit_message_text('Даты выбраны', call.message.chat.id, call.message.id)
            with bot.retrieve_data(user_id, chat_id) as data:
                bot.send_message(call.message.chat.id,
                                 f"Выбранный город:\t{data['city']}\n"
                                 f"Дата заезда:\t{data['check_in']}\n"
                                 f"Дата отъезда:\t{data['check_out']}",
                                 reply_markup=date_received_keyboard())
    else:
        bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda message: message.text == "Изменить город")
def change_city(message: Message) -> None:
    bot.set_state(message.from_user.id, UserState.choice_city, message.chat.id)
    bot.send_message(message.chat.id, "Введите новый город")


@bot.message_handler(func=lambda message: message.text == "Изменить даты")
def change_date(message: Message) -> None:
    bot.set_state(message.from_user.id, UserState.choice_date, message.chat.id)


@bot.message_handler(func=lambda message: message.text == "Показать результаты")
def result(message: Message) -> None:
    bot.set_state(message.from_user.id, UserState.done, message.chat.id)
    bot.send_message(message.chat.id, "Здесь будут результаты поиска",
                     reply_markup=date_received_keyboard())


@bot.callback_query_handler(func=lambda call: call.data.startswith('month:'))
def change_month(call: CallbackQuery) -> None:
    bot.answer_callback_query(call.id)
    if bot.get_state(call.from_user.id, call.message.chat.id) in [UserState.check_in.name, UserState.check_out.name]:
        year, month = map(int, call.data.replace('month:', '').split())
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=calendar_keyboard(year, month))


@bot.callback_query_handler(func=lambda call: call.data == 'empty')
def empty(call: CallbackQuery) -> None:
    bot.answer_callback_query(call.id)