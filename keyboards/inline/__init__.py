from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import calendar
from datetime import date, timedelta

def calendar_keyboard(year: int, month: int) -> InlineKeyboardMarkup:
    EMTPY_FIELD = 'empty'
    format_date = '%Y-%m-%d'

    keyboard = InlineKeyboardMarkup(row_width=7)
    keyboard.add(InlineKeyboardButton(text=date(year=year, month=month, day=1).strftime('%b %Y'),
                                      callback_data=EMTPY_FIELD))
    keyboard.add(*[InlineKeyboardButton(text=day, callback_data=EMTPY_FIELD)
                   for day in ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']])

    for week in calendar.Calendar().monthdayscalendar(year=year, month=month):
        week_buttons = []
        for day in week:
            if day != 0:
                day_name = str(day)
                week_buttons.append(InlineKeyboardButton(
                    text=day_name, callback_data='date:' + date(year, month, day).strftime(format_date)))
            else:
                day_name = ' '
                week_buttons.append(InlineKeyboardButton(text=day_name, callback_data=EMTPY_FIELD))
        keyboard.add(*week_buttons)

    form = '%Y %m'

    cur = date(year, month, 15)
    prev_month = (cur - timedelta(30)).strftime(form)
    next_month = (cur + timedelta(30)).strftime(form)
    keyboard.add(InlineKeyboardButton(text='Предыдущий месяц', callback_data=f'month: {prev_month}'),
                 InlineKeyboardButton(text='Следующий месяц', callback_data=f'month: {next_month}'))

    return keyboard

def history_keyboard(req) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton('Повторить поиск', callback_data=f'set_from_req:{req}')
    keyboard.add(button1)
    return keyboard