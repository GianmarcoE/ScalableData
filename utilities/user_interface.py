import ttkbootstrap as ttk
import tkinter as tk
from tkinter.filedialog import askopenfilename
import csv
from utilities import operations


def ui():
    root = ttk.Window(themename='superhero')
    root.title('Scalable earnings calculator')
    root.minsize(320, 120)
    lbl = ttk.Label(root, text=f'Pick your Scalable report', font='Calibri 13')
    lbl.pack(padx=30, pady=(20, 0))
    button = ttk.Button(root, text='Find File', command=open_file)
    button.pack(pady=30)

    root.mainloop()


def open_file():
    global list_rows
    list_rows = []
    filename = askopenfilename()
    if 'ScalableCapital-Broker' in filename:
        with open(filename, 'r') as f:
            input_file = csv.reader(f, delimiter=';')
            for row in input_file:
                if row[2] != 'Cancelled' and row[2] != 'status':
                    list_rows.append(row)
    list_rows.reverse()
    capital, dates = operations.find_capital(list_rows)
    stock_list, interests = operations.find_closed_positions(list_rows)
    table2(interests, capital, dates, round(interests*100/capital, 2), stock_list)


def table2(interests, capital, dates, interest_rate, stock_list):
    root = ttk.Window(themename='superhero')
    root.title('Results')
    root.minsize(350, 160)

    lbl = ttk.Label(root, text=dates, font='Calibri 11 bold', foreground='#69E141', background='#303c54')
    lbl.pack(fill='x', padx=30, pady=(30, 10))

    lbl = ttk.Label(root, text=f'Invested capital: {capital}€',
                    font='Calibri 11', foreground='white', background='#303c54')
    lbl.pack(fill='x', padx=30, pady=(20, 10))

    if interest_rate >= 0:
        lbl = ttk.Label(root, text=f'Money gained: {interests}€      (+{interest_rate}%)',
                        font='Calibri 11', foreground='white', background='#303c54')
        lbl.pack(fill='x', padx=30, pady=(20, 10))
    else:
        lbl = ttk.Label(root, text=f'Money lost: {interests}€      ({interest_rate}%)',
                        font='Calibri 11', foreground='white', background='#303c54')
        lbl.pack(fill='x', padx=30, pady=(20, 10))

    button = ttk.Button(root, text=f'See details', command=lambda: table_details(stock_list))
    button.pack(side='left', padx=30, pady=(20, 10))

    root.mainloop()


def table_details(stock_list):
    root = ttk.Window(themename='superhero')
    root.title('Closed Positions')
    root.minsize(400, 200)
    container = ttk.Frame(root)

    canvas = tk.Canvas(container)
    canvas.config(width=400, height=200)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    global scrollable_frame
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    def _on_mouse_wheel(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    canvas.bind_all(
        "<MouseWheel>",
        _on_mouse_wheel
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame.columnconfigure(6, minsize=140)

    stock_list.reverse()
    for stock in range(len(stock_list)):
        lbl = ttk.Label(scrollable_frame, text=f'{stock_list[stock].name}:',
                        font='Calibri 11', foreground='white', background='#303c54')
        lbl.grid(row=stock, column=0, padx=(15, 0), pady=(15, 0), sticky='EW')
        lbl = ttk.Label(scrollable_frame, text=f'{round(stock_list[stock].price_diff, 2)}€',
                        font='Calibri 11', foreground='white', background='#303c54')
        lbl.grid(row=stock, column=1, padx=(30, 0), pady=(15, 0), sticky='NS')
        if round(stock_list[stock].price_diff * 100 / stock_list[stock].money_in, 2) >= 0:
            lbl = ttk.Label(scrollable_frame, text=f'+{round(stock_list[stock].price_diff * 100 / stock_list[stock].money_in, 2)}%',
                            font='Calibri 11', foreground='#008000', background='#303c54')
        else:
            lbl = ttk.Label(scrollable_frame, text=f'{round(stock_list[stock].price_diff * 100 / stock_list[stock].money_in, 2)}%',
                            font='Calibri 11', foreground='#FF5349', background='#303c54')
        lbl.grid(row=stock, column=2, padx=(30, 0), pady=(15, 0), sticky='E')

    container.pack(fill="both", expand=True)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    root.mainloop()