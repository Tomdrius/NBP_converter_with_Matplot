import json

import requests
import click
from dateutil import parser
from datetime import datetime, timedelta
from typing import List, Tuple, Dict


DEFAULT_CURRENCY = "USD"
DATA_FORMAT = "%Y-%m-%d"
URL_BETWEEN = "http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{date_start}/{date_end}/?format=json"


def validate_currency(currency:str) -> None:
    if not currency.isalpha() or len(currency) != 3:
        raise ValueError("Invalid currency format. Please provide a 3-letter currency code.")

def check_currency_code_exists() -> List[str]:
    with open('currency_codes.txt', 'r') as file:
        codes = file.read().splitlines()
        return codes


def validate_date(date_start:str, date_end:str) -> Tuple[str]:
    try:
        date_parsed_start = parser.parse(date_start)
        date_start = date_parsed_start.strftime(DATA_FORMAT)
        date_parsed_end = parser.parse(date_end)
        date_end = date_parsed_end.strftime(DATA_FORMAT)
    except ValueError:
        raise ValueError("Invalid date format. Please provide the date in YYYY-MM-DD format.")


    if date_parsed_start.year < 2002 and date_parsed_end.year < 2002:
        raise ValueError("Invalid year. Please provide a year after 2001.")


    if date_parsed_start.date() > datetime.now().date() or date_parsed_end.date() > datetime.now().date():
        raise ValueError("Invalid date. Please provide a date in the past.")
        

    return date_start, date_end

def get_exchange_rate(currency:str, date_start:str, date_end:str) -> Dict:
    url = URL_BETWEEN.format(currency=currency, date_start=date_start, date_end=date_end)
    resp = requests.get(url)

    if resp.status_code == 404:
        raise ValueError("No data. You probably chose a day off.")

    if not resp.ok: #How to test?
        raise ValueError("Unexpected server response")

    return resp.json()

def extract_currency_rates(resp_js:Dict) -> List:
    try:    
        currency_rates = [item["mid"] for item in resp_js["rates"]]
    
    except json.decoder.JSONDecodeError:
        raise ValueError("No data")
    
    except KeyError:
        raise KeyError("Empty key")
    
    except TypeError:
        raise TypeError("Invalid data")

    return currency_rates


codes = check_currency_code_exists()
@click.command()
@click.argument('currency', default=DEFAULT_CURRENCY, type=click.Choice(codes, case_sensitive=False))
@click.argument('date_start', default=(datetime.now()-timedelta(days=3)).strftime(DATA_FORMAT))
@click.argument('date_end', default=datetime.now().strftime(DATA_FORMAT))
def main(currency, date_start, date_end):

# codes = check_currency_code_exists()
# @click.command()
# @click.option('--currency', '-c', default=DEFAULT_CURRENCY, prompt='Provide the currency', help='The currency code (3 letters)', type=click.Choice(codes, case_sensitive=False))
# @click.option('--date_start', '-s', default=(datetime.now()-timedelta(days=1)).strftime(DATA_FORMAT), prompt='Provide the start date', help='The date in YYYY-MM-DD format')
# @click.option('--date_end', '-e', default=datetime.now().strftime(DATA_FORMAT), prompt='Provide the end date', help='The date in YYYY-MM-DD format')
# def main(currency, date_start, date_end):
    validate_currency(currency)
    date_start, date_end = validate_date(date_start, date_end)
    resp_js = get_exchange_rate(currency, date_start, date_end)
    currency_rates = extract_currency_rates(resp_js)
    dates = [item["effectiveDate"] for item in resp_js["rates"]]
    for i, c in enumerate(currency_rates):
        print(f"1 {currency.upper()} = {c} PLN on the day {dates[i]}")


if __name__ == '__main__':
    main()