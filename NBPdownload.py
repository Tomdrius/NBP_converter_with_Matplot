import requests

url = "http://api.nbp.pl/api/exchangerates/tables/A/?format=json"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    currencies = [rate['code'] for rate in data[0]['rates']]

    # Zapisz do pliku
    with open('currency_codes.txt', 'w') as file:
        for currency in currencies:
            file.write(f"{currency}\n")

    print("The file with currency codes has been downloaded and saved as 'currency_codes.txt'")
else:
    print(f"Error while fetching data. Status code: {response.status_code}")
