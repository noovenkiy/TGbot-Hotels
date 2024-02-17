from loader import bot
from telebot.types import CallbackQuery
from keyboards.inline import main_menu_st2_keyboard
from config_data.config import NUMBER_OF_FOTO


@bot.callback_query_handler(func=lambda call: call.data == "need_foto")
def change_show_foto(call: CallbackQuery) -> None:
    bot.answer_callback_query(call.id)
    with bot.retrieve_data(call.from_user.id) as data:
        num = data["number_hotels"]
        foto = data["foto"]
        if foto:
            data["foto"] = 0
        else:
            data["foto"] = NUMBER_OF_FOTO
    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.id,
        reply_markup=main_menu_st2_keyboard(num, not foto),
    )


@bot.callback_query_handler(func=lambda call: call.data == "number_hotels")
def change_number_hotels(call: CallbackQuery) -> None:
    bot.answer_callback_query(call.id)
    with bot.retrieve_data(call.from_user.id) as data:
        num = data.get("number_hotels")
        foto = data["foto"]
        if num < 30:
            num += 5
        else:
            num = 5
        data["number_hotels"] = num
    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.id,
        reply_markup=main_menu_st2_keyboard(number_hotels=num, foto=foto),
    )
