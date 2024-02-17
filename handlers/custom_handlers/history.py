from loader import bot
from telebot.types import Message, CallbackQuery
from datetime import datetime, date, timedelta
from database.command import get_history_from_db, get_req_from_db
from handlers.custom_handlers.menu import main_menu_st1
from keyboards.inline import history_keyboard


@bot.message_handler(commands=["history"])
def history_com(message: Message) -> None:
    history(message.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data == "/history")
def history_inl(call: CallbackQuery) -> None:
    history(call.from_user.id)


def history(user_id: int) -> None:
    hotel_history = get_history_from_db(user_id)
    if hotel_history:

        bot.send_message(user_id, r"*ИСТОРИЯ ЗАПРОСОВ*", parse_mode="Markdown")
        for req_id, date_req, city, check_in, check_out, sort_from_db in hotel_history:

            sort = "По возрастанию стоимости"
            if sort_from_db == "PHTL":
                sort = "По убыванию стоимости"
            elif sort_from_db == "DFL":
                sort = "Ближе к центру"

            bot.send_message(
                user_id,
                f"<b>Дата запроса:</b> {date_req}\n"
                f"<b>Город:</b> <i>{city}</i>\n"
                f"<b>Даты проживания:</b> <i>с {check_in} по {check_out}</i>\n"
                f"<b>Сортировка:</b> <i>{sort}</i>",
                reply_markup=history_keyboard(req_id),
                parse_mode="HTML",
            )
        bot.send_message(user_id, r"*КОНЕЦ ИСТОРИИ ЗАПРОСОВ*", parse_mode="Markdown")

    else:
        bot.send_message(user_id, "История запросов пуста.")


@bot.callback_query_handler(func=lambda call: call.data.startswith("set_from_req:"))
def set_from_req(call: CallbackQuery) -> None:
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id
    req = call.data.replace("set_from_req:", "")
    record = get_req_from_db(req)
    with bot.retrieve_data(user_id) as data:
        data["city"] = record[2]  # Текстовое наименование локации
        data["city_id"] = record[1]  # ID текущей локации
        check_in = datetime.strptime(record[3], "%Y-%m-%d").date()
        if check_in < date.today():
            data["check_in"] = date.today()  # Дата заезда
            data["check_out"] = date.today() + timedelta(1)  # Дата выезда
        else:
            data["check_in"] = check_in  # Дата заезда
            data["check_out"] = datetime.strptime(record[4], "%Y-%m-%d").date()

    main_menu_st1(call.message.chat.id, user_id)
