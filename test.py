import requests
import json

url = "https://hotels4.p.rapidapi.com/v2/get-meta-data"

headers = {
	"X-RapidAPI-Key": "7f9a95d7femsh5b063cc08e78b69p14c8eajsnb9d0c15da769",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
answer = response.json()
print(json.dumps(answer, indent=4))