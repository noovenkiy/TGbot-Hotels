import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены, так как отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Помощь"),
    ("history", "История запросов"),
    ("city", "Выбрать город"),
    ("date", "Выбрать даты"),
)

NUMBER_OF_FOTO = 5  # количество выводимых фото по умолчанию
DES_TO_FILE = True  # запись запроса уточнения локации в файл
RESPONSE_FROM_FILE = True  # попытка считать ответ из файла, если подходящий есть в базе
