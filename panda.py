import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def add_matplotlib_widget(master, get_x_func):
    fig = Figure(figsize=(10, 4), dpi=100)
    fig.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.15)
    ax = fig.add_subplot(111)

    
    canvas_visible = tk.BooleanVar()
    canvas_visible.set(False)
    
    canvas = FigureCanvasTkAgg(fig, master=master)

    def toggle_canvas():
        dates, values = get_x_func()
        draw_chart(dates, values)
        if canvas_visible.get():
            canvas.get_tk_widget().grid_forget()
            toggle_button.config(text="Show Canvas")
        else:
            canvas.get_tk_widget().grid(row=0, column=2, rowspan=4)
            toggle_button.config(text="Hide Canvas")

        canvas_visible.set(not canvas_visible.get())       

    def draw_chart(dates, values):
        ax.clear()

        data = {'x': dates, 'y': values}

        ax.plot(data['x'], data['y'], color='black', markerfacecolor='blue', markeredgecolor='red')
        ax.tick_params(axis='x', rotation=35, labelsize=6)
        ax.set_ylabel('Currency value')
        ax.set_facecolor('#AFC2AD')
        ax.set_ylim(min(values)*0.95, max(values)*1.05)




        canvas.draw()

    toggle_button = tk.Button(master, text="Show Canvas", command=toggle_canvas)
    # toggle_button.grid(row=0, column=1)
    toggle_button.grid(row=1, column=0, sticky="e", padx=(10, 20), pady=10)