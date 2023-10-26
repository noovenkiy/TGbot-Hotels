import datetime
from telebot.types import Message
from states.OrderImformation import OrderImformation
from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    bot.set_state(message.from_user.id, OrderImformation.country, message.chat.id)
    bot.reply_to(message, f"Приветствую, {message.from_user.full_name}! Данный бот служит для "
                          f"бронирования отелей. Пожалуйста, напишите название страны, которую вы бы хотели посетить")


@bot.message_handler(state=OrderImformation.country)
def country(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.chat.id, "Отлично. Теперь введите напишите количество человек")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['country'] = message.text
        bot.set_state(message.from_user.id, OrderImformation.num_of_ppl, message.chat.id)
    else:
        bot.send_message(message.chat.id, "Ошибка. Название страны не должно содержать цифр")

@bot.message_handler(state=OrderImformation.num_of_ppl)
def num_of_ppl(message: Message) -> None:
    if not message.text.isalpha():
        bot.send_message(message.chat.id, "Отлично. Теперь выберите интересующую дату в формате день, месяц, год (30.12.2023)")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['num_of_ppl'] = message.text
        bot.set_state(message.from_user.id, OrderImformation.date, message.chat.id)
    else:
        bot.send_message(message.chat.id, "Ошибка. Пожалуйста, укажите количество человек числом")

@bot.message_handler(state=OrderImformation.date)
def date(message: Message) -> None:
    try:
        datetime.datetime.strptime(message.text, '%d.%m.%Y')
        flag = True
    except Exception:
        flag = False
    if flag:
        bot.send_message(message.chat.id, "Отлично. Сколько результатов вы хотите видеть? (не более 10)")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['date'] = message.text
        bot.set_state(message.from_user.id, OrderImformation.res_count, message.chat.id)
    else:
        bot.send_message(message.chat.id, "Ошибка. Формат даты должен быть xx.yy.zzzz")

@bot.message_handler(state=OrderImformation.res_count)
def res_count(message: Message) -> None:
    if not message.text.isalpha():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if int(message.text) <= 10:
                data['res_count'] = message.text
            else:
                data['res_count'] = '10'
            bot.send_message(message.chat.id, f"Вот указанные вами данные:\n"
                                              f"Страна: {data['country']}\n"
                                              f"Количество человек: {data['num_of_ppl']}\n"
                                              f"Дата: {data['date']}\n"
                                              f"Количество результатов: {data['res_count']}\n"
                                              f"Вот ваши результаты")
    else:
        bot.send_message(message.chat.id, "Ошибка. Пожалуйста, укажите количество результатов числом")