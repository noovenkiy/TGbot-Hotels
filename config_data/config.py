import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены, так как отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("help", "Помощь"),
    ("history", "История запросов"),
    ("new_travel", "Выбрать город/даты")
)

NUMBER_OF_FOTO = 7  # количество выводимых фото по умолчанию
DES_TO_FILE = True  # запись запроса уточнения локации в файл
HOTELS_TO_FILE = False  # запись запроса отелей в файл
FOTO_TO_FILE = True  # запись запросов фото в файл
RESPONSE_FROM_FILE = True  # попытка считать ответ из файла, если подходящий есть в базе (только для FOTO и DES)