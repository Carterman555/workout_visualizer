from tkinter import *
from tkinter import ttk
import re

from csv_helper import *

class GUI:

    def __init__(self):
        self.root = Tk()
        self.root.title = "WorkoutVisualizer"

        self.mainframe = ttk.Frame(self.root, padding="20")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(self.mainframe, text="Workout Visualizer").grid(column=0, row=0, columnspan=2, sticky=(N))

        # entry labels
        ttk.Label(self.mainframe, text="Date").grid(column=0, row=1, sticky=(E))
        ttk.Label(self.mainframe, text="Exercise").grid(column=0, row=3, sticky=(E))
        ttk.Label(self.mainframe, text="Weight").grid(column=0, row=5, sticky=(E))
        ttk.Label(self.mainframe, text="Reps").grid(column=0, row=7, sticky=(E))

        # entries
        self.date = StringVar()
        self.exercise = StringVar()
        self.weight = StringVar()
        self.reps = StringVar()

        self.date.trace_add("write", self.check_add_enabled)
        self.exercise.trace_add("write", self.check_add_enabled)
        self.weight.trace_add("write", self.check_add_enabled)
        self.reps.trace_add("write", self.check_add_enabled)
        
        check_date_wrapper = (self.root.register(self.check_date_entry), '%P', '%V')
        date_entry = ttk.Entry(self.mainframe, width=15, textvariable=self.date, validate='all', validatecommand=check_date_wrapper)

        exercise_entry = ttk.Entry(self.mainframe, width=15, textvariable=self.exercise)

        check_num_wrapper = (self.root.register(self.check_num_entry), '%P')
        weight_entry = ttk.Entry(self.mainframe, width=15, textvariable=self.weight, validate='key', validatecommand=check_num_wrapper)
        reps_entry = ttk.Entry(self.mainframe, width=15, textvariable=self.reps, validate='key', validatecommand=check_num_wrapper)

        date_entry.grid(column=1, row=1, sticky=(E))
        exercise_entry.grid(column=1, row=3, sticky=(E))
        weight_entry.grid(column=1, row=5, sticky=(E))
        reps_entry.grid(column=1, row=7, sticky=(E))

        # error messages
        self.error_message = StringVar()
        msg = ttk.Label(self.mainframe, font='TkSmallCaptionFont', foreground='red', textvariable=self.error_message)
        msg.grid(column=0, row=2, columnspan=2, sticky='e')

        # buttons
        self.add_button = ttk.Button(self.mainframe, text='Add', command=self.add_entry)
        self.add_button.state(['disabled'])

        self.add_button.grid(column=0, row=9, columnspan=2)

        # padding
        self.mainframe.columnconfigure(1, pad=15)
        self.mainframe.rowconfigure(0, pad=25)

        for x in range(1, 9, 2):
            self.mainframe.rowconfigure(x, pad=15)

        for x in range(2, 9, 2):
            self.mainframe.rowconfigure(x, pad=5)

        self.mainframe.rowconfigure(9, pad=25)

        self.root.mainloop()


    def check_date_entry(self, newval, op):
        self.error_message.set('')
        valid = re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', newval) is not None

        error = "Date should be ##/##/####"

        if op=='key':
            ok_so_far = re.match(r'^[0-9/]+$', newval) is not None and len(newval) <= 10
            if not ok_so_far:
                self.error_message.set(error)
            return ok_so_far
        elif op=='focusout':
            if not valid:
                self.error_message.set(error)

        return valid


    def check_num_entry(self, newval):
        return re.match('^[0-9]*$', newval) is not None and len(newval) <= 5


    def check_add_enabled(self, *args):
        date_valid = re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', self.date.get()) is not None
        exercise_valid = len(self.exercise.get()) > 0
        weight_valid = len(self.weight.get()) > 0
        reps_valid = len(self.reps.get()) > 0

        valid = date_valid and exercise_valid and weight_valid and reps_valid

        self.add_button.state(['!disabled'] if valid else ['disabled'])

        

    def add_entry(self, *args):

        add_csv_entry(self.date.get(), self.exercise.get(), self.weight.get(), self.reps.get())

        print(f"Added: {self.date.get()}, {self.exercise.get()}, {self.weight.get()}, {self.reps.get()}")

