import pandas as pd
import numpy as np
import os
import platform
import subprocess

CSV_PATH = "data/processed/exercises.csv"

def csv_exists():
    return os.path.exists(CSV_PATH)


def create_new_csv():

    df = pd.DataFrame({
        'date': [],
        'exercise': [],
        'set num': [],
        'weight': [],
        'reps': []
    })

    df.to_csv(CSV_PATH, index=False)

    return df


def add_csv_entry(date, exercise, set_num, weight, reps):

    if csv_exists():
        df = pd.read_csv(CSV_PATH)
    else:
        df = create_new_csv()

    new_entry = pd.DataFrame({
        'date': [date],
        'exercise': [exercise],
        'set num': [set_num],
        'weight': [weight],
        'reps': [reps]
    })

    new_df = pd.concat([df, new_entry], ignore_index=True)
    new_df = new_df.drop_duplicates()

    new_df.to_csv(CSV_PATH, index=False)


def add_strong_csv_entries(file_path):

    if csv_exists():
        processed_df = pd.read_csv(CSV_PATH)
    else:
        processed_df = create_new_csv()

    strong_df = pd.read_csv(file_path)

    # TODO - finish


def nano_edit_csv():
    subprocess.run(["nano", CSV_PATH])


def open_csv_notepad(system=None):
    subprocess.run(["notepad.exe", CSV_PATH])


def remove_invalid_entries():
    if csv_exists():
        df = pd.read_csv(CSV_PATH)
    else:
        df = create_new_csv()

    new_df = new_df.drop_duplicates()

def format_dates():
    pass

def process_csv():
    remove_invalid_entries()
    format_dates()


def print_csv():
    if csv_exists():
        df = pd.read_csv(CSV_PATH)
    else:
        df = create_new_csv()

    print(df);