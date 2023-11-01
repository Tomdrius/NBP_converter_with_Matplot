import tkinter as tk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from typing import List, Tuple, Callable

def window_initialization() -> tk.Tk:
    root = tk.Tk()
    root.resizable(width=False, height=True)
    root.geometry("+0+0")
    root.title('Currency exchanger')
    return root

def frame_init(root: tk.Tk) -> tk.Frame:
    frame = tk.Frame(root, borderwidth=4)
    frame.grid(row=0, column=0)
    frame.config(background='lightblue')
    return frame

def result_frame_inti(root: tk.Tk) -> tk.Frame:
    result_frame = tk.Frame(root, borderwidth=4)
    result_frame.grid(row=3, column=0)
    # result_frame.pack
    result_frame.config(background='#AFC2AD')
    return result_frame

def entry_init_text(frame: tk.Frame, label_text: str, options: List[str], default_value: str) -> Tuple[tk.Label, tk.ttk.Combobox]:
    label = tk.Label(frame, text=label_text, width=33, anchor=tk.W)
    label.grid(sticky=tk.W, row=len(frame.winfo_children()), column=0, padx=2, pady=2)
    label.config(background='#E8EEE8', font=('Arial', 12))
    combo = tk.ttk.Combobox(frame, values=options, width=20)
    combo.set(default_value)
    combo.grid(sticky=tk.W, row=len(frame.winfo_children()) - 1, column=1, padx=2, pady=2)
    combo.config(background='#E8EEE8', font=('Arial', 12))
    return label, combo


def entry_init_date(frame: tk.Frame, label_text: str, is_first: bool = False) -> Tuple[tk.Label, DateEntry]:
    label = tk.Label(frame, text=label_text, width=33, anchor=tk.W)
    label.grid(sticky=tk.W, row=len(frame.winfo_children()), column=0, padx=2, pady=2)
    label.config(background='#E8EEE8', font=('Arial', 12))
    date_picker = DateEntry(frame, width=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
    if is_first:
        date_picker.set_date(datetime.now() - timedelta(days=7))
    else:
        date_picker.set_date(datetime.now())
    date_picker.grid(sticky=tk.W, row=len(frame.winfo_children()) - 1, column=1, padx=2, pady=2)
    date_picker.config(background='#E8EEE8', font=('Arial', 12))
    return label, date_picker


def label_show_init(result_frame: tk.Frame, entries: List[tk.Entry]) -> None:
    currency, currency2, date_start, date_end = entries
    label = tk.Label(result_frame, text=f'Currency: {currency.get()}/{currency2.get()}. Start Date: {date_start.get()}. End Date: {date_end.get()}', width=52, anchor=tk.W)
    label.grid(sticky=tk.W, row=2, columnspan=2, padx=2, pady=2)
    label.config(background='#E8EEE8', font=('Arial', 12))

def button_init(root: tk.Tk, result_frame: tk.Frame, entries: List[tk.Entry]) -> Tuple[tk.Button, Callable[[], None]]:
    button = tk.Button(root, text="Show", command=lambda: label_show_init(result_frame, entries))
    button.grid(row=2, column=0, columnspan=2, padx=(210, 0), pady=10)
    button.config(background='green', foreground='white', font=('Arial', 14))
    return button

def combo_change_handler(result_frame: tk.Frame, entries: List[tk.Entry]) -> Callable[[tk.Event], any]:
    def handler(event):
        label_show_init(result_frame, entries)
    return handler



def clear_result_frame(result_frame: tk.Frame) -> None:
    for widget in result_frame.winfo_children():
        widget.destroy()

def windows_init(root: tk.Tk, codes: List[str]) -> Tuple[tk.Frame, List[tk.Entry]]:
    frame = frame_init(root)
    entries = []

    label, currency = entry_init_text(frame, 'Provide the currency (default: USD): ', codes, 'USD')
    entries.append(currency)

    label, currency = entry_init_text(frame, 'Provide the currency (default: PLN): ', codes, 'PLN')
    entries.append(currency)

    label, date_start = entry_init_date(frame, 'Provide the start date (default: 7 days ago): ', is_first=True)
    entries.append(date_start)

    label, date_end = entry_init_date(frame, 'Provide the end date (default: yesterday): ')
    entries.append(date_end)

    return frame, entries

def main() -> None:
    codes = ['PLN', 'THB', 'USD', 'AUD', 'HKD', 'CAD', 'NZD', 'SGD', 'EUR', 'HUF', 'CHF', 'GBP', 'UAH', 'JPY', 'CZK', 'DKK', 'ISK', 'NOK', 'SEK', 'RON', 'BGN', 'TRY', 'ILS', 'CLP', 'PHP', 'MXN', 'ZAR', 'BRL', 'MYR', 'IDR', 'INR', 'KRW', 'CNY', 'XDR']
    root = window_initialization()
    result_frame = result_frame_inti(root)
    frame, entries = windows_init(root, codes)

    combo1 = entries[0]
    combo2 = entries[1]
    
    combo1.bind('<<ComboboxSelected>>', combo_change_handler(result_frame, entries))
    combo2.bind('<<ComboboxSelected>>', combo_change_handler(result_frame, entries))

    clear_result_frame(result_frame)
    button = button_init(root, result_frame, entries)
    root.mainloop()

if __name__ == '__main__':
    main()