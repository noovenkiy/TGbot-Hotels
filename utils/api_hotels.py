import os
import requests
import json
import re
from typing import Optional, Literal, Dict
from config_data.config import RAPID_API_KEY

def request_to_api_hotel(querystring: dict, mode: Literal['des', 'hotel', 'foto'] = 'hotel',
                         to_file: bool = False) -> Optional[dict]:
    if mode != 'hotel':
        file_name = ''
        if mode == 'des':
            file_name = 'DES_' + querystring['query']
        elif mode == 'foto':
            file_name = f'FOTO_{querystring["id"]}'
        file_name = r'materials\\api_request\\' + file_name + '.json'
        print('Попытка выполнить запрос из файла. Ищем файл:', file_name, end=' ')
        if os.path.isfile(file_name):
            with open(file_name, 'r', encoding='utf-8') as file:
                response = json.load(file)
            print(' -->>> Файл найден. Запрос выполнен из файла')
            return response
        else:
            print(' -->>> Файл не найден. Запрос выполняется из API')

    endpoint = 'properties/list'
    if mode == 'des':
        endpoint = 'locations/v2/search'
    elif mode == 'foto':
        endpoint = 'properties/get-hotel-photos'

    url = 'https://hotels4.p.rapidapi.com/' + endpoint
    headers = {'X-RapidAPI-Host': 'hotels4.p.rapidapi.com', 'X-RapidAPI-Key': RAPID_API_KEY}
    for i in range(3):
        try:
            print(f'Запрос, попытка {i + 1} ::: {querystring} -->>> ', end='')
            response = requests.get(url, headers=headers, params=querystring, timeout=10)
            if response.status_code == 200:
                print('Ответ успешно получен.')
                break
        except requests.exceptions.RequestException as message:
            print('Ошибка request', message)
    else:
        return None

    response.encoding = 'utf-8'
    response = response.json()

    return response
def get_destination(location: str) -> Optional[Dict[str, str]]:

    querystring = {"query": location, "locale": "ru_RU", "currency": "USD"}
    response = request_to_api_hotel(querystring, 'des', True)
    if not response:
        return None
    result = {}
    for elem in response['suggestions']:
        if elem['group'] in ['CITY_GROUP', 'TRANSPORT_GROUP']:
            for line in elem['entities']:
                name = re.sub(r'<.*?>', '', line['caption'])
                result[name] = line['destinationId']
    return result