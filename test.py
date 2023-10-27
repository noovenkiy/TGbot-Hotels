import requests

url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

payload = {
	"currency": "USD",
	"eapid": 1,
	"locale": "en_US",
	"siteId": 300000001,
	"propertyId": "9209612"
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "7f9a95d7femsh5b063cc08e78b69p14c8eajsnb9d0c15da769",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())