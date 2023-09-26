import json
import sys
import requests
from dateutil import parser
from datetime import datetime

def get_user_input():
    print("Currency converter")

    if len(sys.argv) > 3:
        print("Provide the currency and date: ")
        sys.exit(1)

    try:
        currency = sys.argv[1]
    except IndexError:
        currency = input("Provide the currency: ")

    try:
        input_date = sys.argv[2]
    except IndexError:
        input_date = input("Provide the date: ")

    return currency.upper(), input_date

def validate_currency(currency):
    if not currency.isalpha() or len(currency) != 3:
        raise ValueError("Invalid currency format. Please provide a 3-letter currency code.")

def check_currency_code_exists(currency):
    with open('currency_codes.txt', 'r') as file:
        codes = file.read().splitlines()
    
    if currency not in codes:
        raise ValueError("This currency doesn't exist in NBP database.")

def validate_date(input_date):
    try:
        date_parsed = parser.parse(input_date)
        date_adjust = date_parsed.strftime("%Y-%m-%d")
        date_print = date_parsed.strftime("%Y/%m/%d")
        
    except ValueError:
        raise ValueError("Invalid date format. Please provide the date in YYYY-MM-DD format.")


    if date_parsed.year < 2002:
        raise ValueError("Invalid year. Please provide a year between 2002 and 2023.")


    if date_parsed.date() > datetime.now().date():
        raise ValueError("Invalid date. Please provide a date in the past.")
        

    return date_adjust, date_print

def get_exchange_rate(currency, date_adjust):
    url = f"http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{date_adjust}/?format=json"
    resp = requests.get(url)

    if resp.status_code == 404:
        raise ValueError("No data. You probably chose a day off.")

    if not resp.ok:
        raise ValueError("Unexpected server response")

    return resp.json()

def extract_currency_rate(resp_js):
    try:    
        currency_rate = resp_js["rates"][0]["mid"]
    except json.decoder.JSONDecodeError:
        raise ValueError("No data")

    return currency_rate

def main():
    currency, input_date = get_user_input()
    validate_currency(currency)
    check_currency_code_exists(currency)
    date_adjust, date_print = validate_date(input_date)
    resp_js = get_exchange_rate(currency, date_adjust)
    currency_rate = extract_currency_rate(resp_js)

    print(f"1 {currency} = {currency_rate} PLN on the day {date_print}")

if __name__ == '__main__':
    main()