from tkinter import *
from tkinter import ttk
from tkinter import font
import re

from csv_helper import *

class GUI:

    def __init__(self):
        self.root = Tk()
        self.root.title = "WorkoutVisualizer"

        self.mainframe = ttk.Frame(self.root, padding="20")
        self.mainframe.grid(column=1, row=1, sticky=(N, W, E, S))

        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)


        # styles and fonts
        s = ttk.Style()
        s.configure('Debug.TFrame', background='gray')

        medium_font = font.Font(family="Helvetica", size=14)
        small_font = font.Font(family="Helvetica", size=11)

        # date
        ttk.Label(self.mainframe, text="Date", font=medium_font).grid(column=1, row=1, pady=(25, 0), sticky=(E))
        ttk.Label(self.mainframe, text="##/##/####", font=small_font).grid(column=2, row=2, padx=15, sticky=(W))

        self.date = StringVar()
        self.date.trace_add("write", self.check_add_enabled)

        date_entry = ttk.Entry(self.mainframe, width=15, font=medium_font, textvariable=self.date)

        date_entry.grid(column=2, row=1, padx=15, pady=(25, 0), sticky=(W))

        # add button
        self.add_button = ttk.Button(self.mainframe, text='Add', command=self.add_entry)
        self.add_button.state(['disabled'])

        self.add_button.grid(column=3, row=1, padx=50, pady=(25, 0), sticky=(E))

        # --- Exercises Grid ---
        gridframe = ttk.Frame(self.mainframe, padding="20")
        gridframe.grid(column=1, row=3, columnspan=3, pady=(25, 0), sticky=(N, W, E, S))

        ttk.Label(gridframe, text="Exercise", font=medium_font).grid(column=1, row=1, padx=(0, 10), pady=10, sticky=(W))

        entries = []
        for row_value in range(10):

            top_row = (row_value*2)+2
            bottom_row = (row_value*2)+3

            self.exercise = StringVar()
            ttk.Entry(gridframe, width=25, font=medium_font, textvariable=self.exercise).grid(column=1, row=top_row, rowspan=2, pady=(0, 20), sticky=(W))

            ttk.Label(gridframe, text="Weight", font=small_font).grid(column=2, row=top_row, padx=(20, 0), sticky=(E))
            ttk.Label(gridframe, text="Reps", font=small_font).grid(column=2, row=bottom_row, pady=(0, 20), sticky=(E))

            for set_num in range(1, 6):

                column = set_num + 2

                ttk.Label(gridframe, text=f"Set {set_num}", font=small_font).grid(column=column, row=1, padx=10, pady=10)
                ttk.Entry(gridframe, width=10, font=small_font).grid(column=column, row=top_row, padx=10)
                ttk.Entry(gridframe, width=10, font=small_font).grid(column=column, row=bottom_row, padx=10, pady=(0, 20))


        # self.exercise = StringVar()
        # self.weight = StringVar()
        # self.reps = StringVar()

        # check_num_wrapper = (self.root.register(self.check_num_entry), '%P')
        # weight_entry = ttk.Entry(self.mainframe, width=15, textvariable=self.weight, validate='key', validatecommand=check_num_wrapper)
        # reps_entry = ttk.Entry(self.mainframe, width=15, textvariable=self.reps, validate='key', validatecommand=check_num_wrapper)

        self.root.mainloop()


    def check_num_entry(self, newval):
        return re.match('^[0-9]*$', newval) is not None and len(newval) <= 5


    def check_add_enabled(self, *args):
        date_valid = re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', self.date.get()) is not None
        valid = date_valid

        self.add_button.state(['!disabled'] if valid else ['disabled'])

        

    def add_entry(self, *args):

        add_csv_entry(self.date.get(), self.exercise.get(), self.weight.get(), self.reps.get())

        print(f"Added: {self.date.get()}, {self.exercise.get()}, {self.weight.get()}, {self.reps.get()}")

