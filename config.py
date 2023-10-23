import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены, так как отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

DB_PATH = "database.db"

DEFAULT_COMMANDS = (
    ("help", "Какие команды есть в боте"),
    ("low", "Самая низкая стоимость"),
    ("high", "Самая высокая стоимость"),
    ("custom", "Определенная стоимость"),
    ("history", "История запросов")
)