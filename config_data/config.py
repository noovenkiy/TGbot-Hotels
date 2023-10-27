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
    ("low", "Сначала дешевле"),
    ("high", "Сначала дороже"),
    ("custom", "Цена от/до"),
    ("history", "История запросов"),
    ("new_travel", "Выбрать город/даты")
)