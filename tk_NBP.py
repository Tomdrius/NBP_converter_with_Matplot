from tkinter import *

def window_initialization():
    root = Tk()
    # root.resizable(width=False, height=True)
    root.geometry("500x300")
    root.title('Currency exchanger')

    return root


def title_init(root):
    title = Label(root, text='Currency exchange rates of the National Bank of Poland (NBP)')
    title.grid(row=0, column=0)
    
    return title


def frame_init(root):
    frame = Frame(root, borderwidth=4)  # ramka
    frame.grid(row=1, column=0)
    frame.config(background='black')

    return frame

def label_currency_init(frame, currency):
    label_currency = Label(frame, text='Provide the currency (default: USD): ', width=33, anchor=W)
    label_currency.grid(sticky=W, row=0, column=0, padx=5, pady=5)
    entry_currency = Entry(frame, width=20)
    entry_currency.grid(sticky=W,row=0,column=1,padx=5, pady=5)
    # currency = entry_currency.get()

    return label_currency, entry_currency

def label_start_init(frame, date_start):
    label_start = Label(frame, text='Provide the start date (default: yesterday): ', width=33, anchor=W)
    label_start.grid(sticky=W, row=1, column=0, padx=5, pady=5)
    entry_start = Entry(frame, width=20)
    entry_start.grid(sticky=W,row=1,column=1,padx=5, pady=5)
    date_start = entry_start.get()

    return label_start, date_start

def label_end_init(frame, date_end):
    label_end = Label(frame, text='Provide the end date (default: today): ', width=33, anchor=W)
    label_end.grid(sticky=W, row=2, column=0, padx=5, pady=5)
    entry_end = Entry(frame, width=20)
    entry_end.grid(sticky=W,row=2,column=1,padx=5, pady=5)
    date_end = entry_end.get()

    return label_end, date_end


def label_show_init(frame, currency, date_start, date_end):
    label_currency = Label(frame, text=f'Currency: {currency}. Start Date: {date_start}. End Date: {date_end}', width=52, anchor=W)
    label_currency.grid(sticky=W, row=3, columnspan=2, padx=5, pady=5)


def button_init(root, frame, entry_currency, date_start, date_end):
    button = Button(root, text="Show", command=lambda: label_show_init(frame, currency, date_start, date_end))
    button.grid(row=2, column=0, columnspan=2, padx=(210, 0), pady=10)
    button.config(background='red', foreground='#FFFF00')
    currency = entry_currency.get()
    
    return button


def windows_init(root):
    title = title_init(root)
    frame = frame_init(root)
    

    return title, frame

if __name__ == '__main__':
    currency = "USD"
    date_start = "2023-07-22"
    date_end = "2023-08-13"
    root = window_initialization()
    title, frame = windows_init(root)
    label_currency, currency = label_currency_init(frame, currency)
    label_start, date_start = label_start_init(frame, date_start)
    label_end, date_end = label_end_init(frame, date_end)
    button = button_init(root, frame, currency, date_start, date_end)

    root.mainloop()
