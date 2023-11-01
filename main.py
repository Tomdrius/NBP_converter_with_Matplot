import json
import requests
from dateutil import parser
from datetime import datetime, timedelta
import tkinter as tk
from typing import List, Tuple, Dict, Callable

from tk_NBPupg import window_initialization, windows_init, result_frame_inti, clear_result_frame
from panda import add_matplotlib_widget
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
        date_parsed_start = parser.parse(date_start, dayfirst=True)
        date_start = date_parsed_start.strftime(DATA_FORMAT)
        date_parsed_end = parser.parse(date_end, dayfirst=True)
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

    if not resp.ok:
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


def label_show_init(result_frame: tk.Frame, currency_rates: List[float], currency: str, currency2: str, dates: List[str]) -> None:
    clear_result_frame(result_frame)
    
    for i, c in enumerate(currency_rates):
        result = f"1 {currency.upper()} = {c} {currency2.upper()} on the day {dates[i]}"
        label = tk.Label(result_frame, text=result, width=52, anchor=tk.W)
        label.pack()

def combo_change_handler(root: tk.Tk, result_frame: tk.Frame, entries: List[tk.Entry]) -> Callable[[tk.Event], any]:
    def handler(event):
        button, on_button_click = button_init(root, result_frame, entries)
        on_button_click()

    return handler


def button_init(root: tk.Tk, result_frame, entries) -> Tuple[tk.Button, Callable[[], any]]:

    def on_button_click() -> (List[datetime], List[float]):
        currency = entries[0].get() if entries[0].get() else DEFAULT_CURRENCY
        currency2 = entries[1].get() if entries[0].get() else DEFAULT_CURRENCY
        date_start = entries[2].get() if entries[1].get() else (datetime.now()-timedelta(days=7)).strftime(DATA_FORMAT)
        date_end = entries[3].get() if entries[2].get() else datetime.now().strftime(DATA_FORMAT)
        
        validate_currency(currency)
        validate_currency(currency2)
        date_start, date_end = validate_date(date_start, date_end)

        if currency != 'PLN' and currency2 != 'PLN':
            resp_js = get_exchange_rate(currency, date_start, date_end)
            resp_js2 = get_exchange_rate(currency2, date_start, date_end)
            currency_rates1 = extract_currency_rates(resp_js)
            currency_rates2 = extract_currency_rates(resp_js2)
            currency_rates = [rate1 / rate2 for rate1, rate2 in zip(currency_rates1, currency_rates2)]

        elif currency2 == 'PLN':
            resp_js = get_exchange_rate(currency, date_start, date_end)
            currency_rates = extract_currency_rates(resp_js)
            
        else:
            resp_js = get_exchange_rate(currency2, date_start, date_end)
            currency_rates = extract_currency_rates(resp_js)
            currency_rates = [ 1/c for c in currency_rates]
        
        dates = [item["effectiveDate"] for item in resp_js["rates"]]
        label_show_init(result_frame, currency_rates, currency, currency2, dates)
        
        return dates, currency_rates,

    button = tk.Button(root, text="Show", command=on_button_click)
    button.grid(row=1, column=0, padx=(240, 10), pady=10)
    button.config(background='green', foreground='white')
    return button, on_button_click

def combo_change(root: tk.Tk, result_frame: tk.Frame, entries: List[tk.Entry]) -> None:
    combo1 = entries[0]
    combo2 = entries[1]
    combo1.bind('<<ComboboxSelected>>', combo_change_handler(root, result_frame, entries))
    combo2.bind('<<ComboboxSelected>>', combo_change_handler(root, result_frame, entries))


codes = check_currency_code_exists()
codes.insert(0, 'PLN')

def main() -> None:
    root = window_initialization()
    result_frame = result_frame_inti(root)
    frame, entries = windows_init(root, codes)
    
    clear_result_frame(result_frame)
    button, on_button_click = button_init(root, result_frame, entries)
    combo_change(root, result_frame, entries)
    add_matplotlib_widget(root, on_button_click)
    root.mainloop()

if __name__ == '__main__':
    main()