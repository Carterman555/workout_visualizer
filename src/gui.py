from tkinter import *
from tkinter import ttk
from tkinter import font
import re
from pytrie import StringTrie

from csv_helper import add_csv_entry
from csv_helper import get_exercise_names

class GUI:

    def __init__(self, file_name):

        self.file_name = file_name

        self.root = Tk()
        self.root.title = "WorkoutVisualizer"

        self.mainframe = ttk.Frame(self.root, padding="20")
        self.mainframe.grid(column=1, row=1, sticky=(N, W, E, S))

        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)

        # styles and fonts
        s = ttk.Style()
        s.configure('Debug.TFrame', background='gray')

        self.medium_font = font.Font(family="Helvetica", size=14)
        self.small_font = font.Font(family="Helvetica", size=11)

        # date
        ttk.Label(self.mainframe, text="Date", font=self.medium_font).grid(column=1, row=1, pady=(25, 0), sticky=(E))
        ttk.Label(self.mainframe, text="##/##/####", font=self.small_font).grid(column=2, row=2, padx=15, sticky=(W))

        self.date = StringVar()
        self.date.trace_add("write", self.check_add_enabled)

        date_entry = ttk.Entry(self.mainframe, width=15, font=self.medium_font, textvariable=self.date)

        date_entry.grid(column=2, row=1, padx=15, pady=(25, 0), sticky=(W))

        # add button
        self.add_button = ttk.Button(self.mainframe, text='Add', command=self.add_entries)
        self.add_button.state(['disabled'])

        self.add_button.grid(column=3, row=1, padx=50, pady=(25, 0), sticky=(E))

        # clear button
        self.clear_button = ttk.Button(self.mainframe, text='Clear', command=self.clear_entries)
        self.clear_button.grid(column=4, row=1, pady=(25, 0), sticky=(W))

        # exercise suggestions
        self.suggestionsvar = StringVar(value=[])
        self.suggestions_listbox = Listbox(self.root, font=self.medium_font, listvariable=self.suggestionsvar)
        self.suggestions_listbox.bind(
            "<<ListboxSelect>>",
            lambda e: self.set_suggestion(self.suggestions_listbox.curselection()[0])
        )

        # exercises grid
        gridframe = ttk.Frame(self.mainframe, padding="20")
        gridframe.grid(column=1, row=3, columnspan=4, pady=(25, 0), sticky=(N, W, E, S))

        ttk.Label(gridframe, text="Exercise", font=self.medium_font).grid(column=1, row=1, padx=(0, 10), pady=10, sticky=(W))

        self.entries = []
        self.exericise_entries = []
        for row_value in range(10):

            top_row = (row_value*2)+2
            bottom_row = (row_value*2)+3

            exercise = StringVar()
            exercise_entry = ttk.Entry(gridframe, width=25, font=self.medium_font, textvariable=exercise)
            exercise_entry.grid(column=1, row=top_row, rowspan=2, pady=(0, 20), sticky=(W))
            self.exericise_entries.append(exercise_entry)

            exercise_entry.bind("<FocusIn>", lambda e, ex=exercise: self.show_suggestions(ex.get()))
            exercise_entry.bind("<FocusOut>", lambda e: self.hide_suggestions())
            exercise.trace_add('write', lambda *args, ex=exercise: self.update_suggestions(ex.get()))

            ttk.Label(gridframe, text="Weight", font=self.small_font).grid(column=2, row=top_row, padx=(20, 0), sticky=(E))
            ttk.Label(gridframe, text="Reps", font=self.small_font).grid(column=2, row=bottom_row, pady=(0, 20), sticky=(E))

            weights = []
            rep_amounts = []
            for set_num in range(1, 6):

                column = set_num + 2

                ttk.Label(gridframe, text=f"Set {set_num}", font=self.small_font).grid(column=column, row=1, padx=10, pady=10)

                check_num_wrapper = (self.root.register(self.check_num_entry), '%P')

                weight = StringVar()
                weightEntry = ttk.Entry(gridframe, width=10, font=self.small_font, textvariable=weight, validate='key', validatecommand=check_num_wrapper)
                weightEntry.grid(column=column, row=top_row, padx=10)
                weights.append(weight)

                reps = StringVar()
                reps_entry = ttk.Entry(gridframe, width=10, font=self.small_font, textvariable=reps, validate='key', validatecommand=check_num_wrapper)
                reps_entry.grid(column=column, row=bottom_row, padx=10, pady=(0, 20))
                rep_amounts.append(reps)

            d = {
                "Exercise": exercise,
                "Weights": tuple(weights),
                "RepAmounts": tuple(rep_amounts)
            }

            self.entries.append(d)

        # events
        self.root.bind('<Return>', self.focus_exercise_entry)
        self.root.bind('<Shift-Return>', self.add_entries)

        def on_click(event):
            widget = event.widget
            # Only clear focus if click is not on an Entry or Listbox
            if not isinstance(widget, (ttk.Entry, Entry, Listbox)):
                self.root.focus_set()

        self.root.bind('<Button-1>', on_click)

        self.root.mainloop()
    

    def check_num_entry(self, newval):
        return re.match('^[0-9]*$', newval) is not None and len(newval) <= 5


    def check_add_enabled(self, *args):
        date_valid = re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', self.date.get()) is not None
        valid = date_valid

        self.add_button.state(['!disabled'] if valid else ['disabled'])


    def focus_exercise_entry(self, e):
        for entry_values, entry in zip(self.entries, self.exericise_entries):
            if entry_values["Exercise"].get() == "":
                entry.focus_set()
                return


    def add_entries(self, *args):

        if self.add_button.instate(["disabled"]):
            return

        for entry in self.entries:
            if entry["Exercise"].get() == "":
                break

            if len(entry["Weights"]) != len(entry["RepAmounts"]):
                print(f"Error: mismatching lengths for {entry["Exercise"].get()} - Weights: {len(entry["Weights"])}, Reps: {len(entry["RepAmounts"])}")
                return

            for i in range(len(entry["Weights"])):
                if entry["Weights"][i].get() == "":
                    break

                set_order = int(i+1)
                add_csv_entry(
                    self.date.get(),
                    entry["Exercise"].get(),
                    set_order,
                    entry["Weights"][i].get(),
                    entry["RepAmounts"][i].get(),
                    self.file_name
                )

            
        self.clear_entries()

    def clear_entries(self):

        self.date.set("")

        for entry in self.entries:
            entry["Exercise"].set("")

            for weight in entry["Weights"]:
                weight.set("")

            for reps in entry["RepAmounts"]:
                reps.set("")

    
    def try_place_suggestion_listbox(self):
        widget = self.root.focus_get()
        if widget and isinstance(widget, ttk.Entry):
            x = widget.winfo_rootx() - self.root.winfo_rootx()
            y = widget.winfo_rooty() - self.root.winfo_rooty() + widget.winfo_height()

            self.suggestions_listbox.place(x=x, y=y, width=widget.winfo_width())

    def show_suggestions(self, exercise):
        self.trie = StringTrie()

        for key in get_exercise_names():
            self.trie[key] = key

        self.update_suggestions(exercise)

    def update_suggestions(self, exercise):
        self.suggestions = self.trie.values(exercise)
        self.suggestionsvar.set(self.suggestions)
        if len(self.suggestions) > 0:
            if not self.suggestions_listbox.winfo_ismapped():
                self.try_place_suggestion_listbox()
            self.suggestions_listbox['height'] = len(self.suggestions)
        elif self.suggestions_listbox.winfo_ismapped():
            self.hide_suggestions()

    def hide_suggestions(self):
        self.suggestions_listbox.place_forget()


    def set_suggestion(self, suggestion_index):

        focused_widget = self.root.focus_get()
        stringvar = None
        for entry_values, entry in zip(self.entries, self.exericise_entries):
            if focused_widget == entry:
                stringvar = entry_values['Exercise']

        if stringvar:
            stringvar.set(self.suggestions[suggestion_index])
            self.suggestions_listbox.selection_clear(0, len(self.suggestions) - 1)



        

        

