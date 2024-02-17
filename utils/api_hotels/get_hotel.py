import requests
from config_data.config import RAPID_API_KEY
from typing import Dict, List


def get_hotels(data: dict, sort: str) -> List[dict]:
    def parse(hotel_data: Dict[str, dict]) -> Dict:
        item = {
            "id": hotel_data["id"],
            "url": f'https://www.hotels.com/ho{hotel_data["id"]}',
            "name": hotel_data["name"],
            "price": hotel_data["price"]["lead"]["formatted"],
            "distance": hotel_data["destinationInfo"]["distanceFromDestination"][
                "value"
            ],
            "reviews_score": hotel_data["reviews"]["score"],
            "reviews_total": hotel_data["reviews"]["total"],
        }
        return item

    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    }

    payload = {
        "currency": "USD",
        "locale": "ru_RU",
        "destination": {"regionId": str(data["city_id"])},
        "checkInDate": {
            "day": data["check_in"].day,
            "month": data["check_in"].month,
            "year": data["check_in"].year,
        },
        "checkOutDate": {
            "day": data["check_out"].day,
            "month": data["check_out"].month,
            "year": data["check_out"].year,
        },
        "rooms": [{"adults": 1}],
        "sort": sort,
    }

    response = requests.post(url, json=payload, headers=headers)
    response.encoding = "utf-8"
    response = response.json()
    response = response["data"]["propertySearch"]["properties"]
    result = []
    while len(result) < data["number_hotels"]:
        for elem in response:
            result.append(parse(elem))

    return result[: data["number_hotels"]]
