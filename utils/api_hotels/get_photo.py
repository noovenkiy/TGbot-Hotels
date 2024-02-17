import requests
import random
from config_data.config import RAPID_API_KEY
from typing import Generator


def get_photo(hotel_id: int) -> Generator:
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    }
    payload = {"currency": "USD", "locale": "ru_RU", "propertyId": str(hotel_id)}
    response = requests.post(url, json=payload, headers=headers)
    response.encoding = "utf-8"
    response = response.json()
    response = response["data"]["propertyInfo"]["propertyGallery"]["images"]
    while True:
        random.shuffle(response)
        for elem in response:
            url = elem["image"]["url"]
            yield url
