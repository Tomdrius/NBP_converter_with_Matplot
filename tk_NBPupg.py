import tkinter as tk

def window_initialization():
    root = tk.Tk()
    # root.geometry("500x300")
    root.resizable(width=False, height=True)
    root.title('Currency exchanger')
    return root

def frame_init(root):
    frame = tk.Frame(root, borderwidth=4)
    frame.grid(row=0, column=0)
    frame.config(background='lightblue')
    return frame

def result_frame_inti(root):
    result_frame = tk.Frame(root, borderwidth=4)
    result_frame.grid(row=3, column=0)
    # result_frame.pack
    result_frame.config(background='blue')
    return result_frame

def entry_init(frame, label_text):
    label = tk.Label(frame, text=label_text, width=33, anchor=tk.W)
    label.grid(sticky=tk.W, row=len(frame.winfo_children()), column=0, padx=2, pady=2)
    entry = tk.Entry(frame, width=20)
    entry.grid(sticky=tk.W, row=len(frame.winfo_children()) - 1, column=1, padx=2, pady=2)
    return label, entry

def label_show_init(result_frame, entries):
    currency, date_start, date_end = entries
    label = tk.Label(result_frame, text=f'Currency: {currency.get()}. Start Date: {date_start.get()}. End Date: {date_end.get()}', width=52, anchor=tk.W)
    label.grid(sticky=tk.W, row=2, columnspan=2, padx=2, pady=2)

def button_init(root, result_frame, entries):
    button = tk.Button(root, text="Show", command=lambda: label_show_init(result_frame, entries))
    button.grid(row=2, column=0, columnspan=2, padx=(210, 0), pady=10)
    button.config(background='green', foreground='white')
    return button

def clear_result_frame(result_frame):
    for widget in result_frame.winfo_children():
        widget.destroy()



def windows_init(root):
    frame = frame_init(root)
    entries = []

    label, currency = entry_init(frame, 'Provide the currency (default: USD): ')
    entries.append(currency)

    label, date_start = entry_init(frame, 'Provide the start date (default: 7 days ago): ')
    entries.append(date_start)

    label, date_end = entry_init(frame, 'Provide the end date (default: today): ')
    entries.append(date_end)

    return frame, entries

if __name__ == '__main__':
    root = window_initialization()
    frame, entries = windows_init(root)
    result_frame = result_frame_inti(root)
    clear_result_frame(result_frame)
    button = button_init(root, result_frame, entries)
    root.mainloop()
