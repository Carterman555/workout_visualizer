from tkinter import *
from tkinter import ttk

class GUI:

    def __init__(self):
        self.root = Tk()
        self.root.title = "WorkoutVisualizer"

        self.mainframe = ttk.Frame(self.root, padding="20")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(self.mainframe, text="Workout Visualizer").grid(column=0, row=0, columnspan=2, sticky=(N))

        ttk.Label(self.mainframe, text="Date").grid(column=0, row=1, sticky=(E))
        ttk.Label(self.mainframe, text="Exercise").grid(column=0, row=2, sticky=(E))
        ttk.Label(self.mainframe, text="Weight").grid(column=0, row=3, sticky=(E))
        ttk.Label(self.mainframe, text="Reps").grid(column=0, row=4, sticky=(E))

        self.date = StringVar()
        ttk.Entry(self.mainframe, width=15, textvariable=self.date).grid(column=1, row=1, sticky=(E))

        self.exercise = StringVar()
        ttk.Entry(self.mainframe, width=15, textvariable=self.exercise).grid(column=1, row=2, sticky=(E))

        self.weight = StringVar()
        ttk.Entry(self.mainframe, width=15, textvariable=self.weight).grid(column=1, row=3, sticky=(E))

        self.reps = StringVar()
        ttk.Entry(self.mainframe, width=15, textvariable=self.reps).grid(column=1, row=4, sticky=(E))

        ttk.Button(self.mainframe, text="Add", command=self.add_entry).grid(column=0, row=5, columnspan=2)

        self.mainframe.columnconfigure(1, pad=15)
        self.mainframe.rowconfigure(0, pad=15)
        self.mainframe.rowconfigure(1, pad=15)
        self.mainframe.rowconfigure(2, pad=15)
        self.mainframe.rowconfigure(3, pad=15)
        self.mainframe.rowconfigure(4, pad=15)
        self.mainframe.rowconfigure(5, pad=25)

        self.root.mainloop()

    def add_entry(self, *args):
        print(f"Added: {self.date.get()}, {self.exercise.get()}, {self.weight.get()}, {self.reps.get()}")

