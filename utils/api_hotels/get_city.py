import requests
from config_data.config import RAPID_API_KEY, RESPONSE_FROM_FILE, DES_TO_FILE
from utils.api_hotels.write_response import write_response
from typing import Optional, Dict
import os
import json


def get_destination(location: str) -> Optional[Dict[str, str]]:
    if RESPONSE_FROM_FILE:
        file_name = "city_" + location
        file_name = r"materials\\api_request\\" + file_name + ".json"
        print("Попытка выполнить запрос из файла. Ищем файл:", file_name, end=" ")
        if os.path.isfile(file_name):
            with open(file_name, "r", encoding="utf-8") as file:
                response = json.load(file)
            print(" -->>> Файл найден. Запрос выполнен из файла")
            return response
        else:
            print(" -->>> Файл не найден. Запрос выполняется из API")

    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    }
    querystring = {"q": location, "locale": "ru_RU"}
    response = requests.get(url, headers=headers, params=querystring)
    if not response:
        return None
    response.encoding = "utf-8"
    response = response.json()

    result = {}
    for elem in response["sr"]:
        if elem["type"] == "CITY":
            name = elem["regionNames"]["fullName"]
            result[name] = elem["gaiaId"]

    if DES_TO_FILE:
        write_response(result, response["q"])

    return result
