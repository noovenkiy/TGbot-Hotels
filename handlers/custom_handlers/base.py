import urllib3.exceptions
from loader import bot
from telebot.types import InputMediaPhoto, CallbackQuery
import telebot.apihelper
from utils.api_hotels import get_hotels, get_photo
from handlers.custom_handlers.menu import main_menu_st1
from database.command import save_request_to_db

# Здесь определены базовые команды бота.

@bot.callback_query_handler(func=lambda call: call.data == 'lowprice')
def low_price(call: CallbackQuery) -> None:
    handler_command(call.message.chat.id, call.from_user.id, 'lowprice')

@bot.callback_query_handler(func=lambda call: call.data == 'bestdeal')
def low_price(call: CallbackQuery) -> None:
    handler_command(call.message.chat.id, call.from_user.id, 'bestdeal')

@bot.callback_query_handler(func=lambda call: call.data == 'highprice')
def low_price(call: CallbackQuery) -> None:
    handler_command(call.message.chat.id, call.from_user.id, 'highprice')


def handler_command(chat_id: int, user_id: int, command: str = 'lowprice') -> None:
    bot.send_message(user_id, 'Получаем информацию...')

    sort, sort_to_db = 'PRICE', 'P'
    if command == 'highprice':
        sort, sort_to_db = 'PRICE_HIGHEST_FIRST', 'PHF'
    elif command == 'bestdeal':
        sort, sort_to_db = 'DISTANCE_FROM_LANDMARK', 'DFL'

    with bot.retrieve_data(user_id, chat_id) as data:
        hotels = get_hotels(data, sortOrder=sort)
        send_hotels(hotels, user_id, data['foto'])
    save_request_to_db(hotels, user_id, sort_to_db, **data)
    main_menu_st1(chat_id, user_id)


def send_hotels(hotels: list, user_id: int, number_foto: int = False) -> None:
    for hotel in hotels:
        text = f"<b>{hotel['name']}</b>\n" \
               f"<i>{hotel['address']}</i>\n" \
               f"{hotel['price']}\n" \
               f"{hotel['url']}"
        if number_foto:
            foto = get_photo(hotel['id'])
            for _ in range(3):
                foto_list = [InputMediaPhoto(next(foto)) for _ in range(number_foto - 1)]
                foto_list.append(InputMediaPhoto(next(foto), caption=text, parse_mode='HTML'))
                try:
                    bot.send_media_group(user_id, foto_list)
                    break
                except [telebot.apihelper.ApiTelegramException, urllib3.exceptions.ReadTimeoutError] as msg:
                    print('Ошибка отправки медиагруппы. ID отеля:', hotel['id'], msg)
            else:
                text = 'Фото получить не удалось.\n\n' + text
                bot.send_message(user_id, text,
                                 parse_mode='HTML',
                                 disable_web_page_preview=True,
                                 )
        else:
            bot.send_message(user_id, text,
                             parse_mode='HTML',
                             disable_web_page_preview=True,
                             )