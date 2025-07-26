import pandas as pd
import numpy as np
import os
import platform
import subprocess

from helper import format_date

CSV_PATH = "data/processed/exercises.csv"

def csv_exists():
    return os.path.exists(CSV_PATH)


def get_df():
    if csv_exists():
        try:
            df = pd.read_csv(CSV_PATH)
        except Exception as e:
            print(f"Error trying to read csv {e}. Edit csv to correct format.")
    else:
        df = create_new_csv()

    return df


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

    df = get_df()

    new_entry = pd.DataFrame({
        'date': [date],
        'exercise': [exercise],
        'set num': [set_num],
        'weight': [weight],
        'reps': [reps]
    })

    new_df = pd.concat([df, new_entry], ignore_index=True)
    new_df.to_csv(CSV_PATH, index=False)

    remove_invalid_entries()


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
    df = get_df()

    new_df = df.drop_duplicates().dropna()

    new_df.to_csv(CSV_PATH, index=False)


def format_dates():
    df = get_df()

    for num, data in df.iterrows():
        date = data['date']
        df.loc[num, 'date'] = format_date(date)

    df.to_csv(CSV_PATH, index=False)


def process_csv():
    remove_invalid_entries()
    format_dates()
    remove_invalid_entries() # to remove duplicates after formating dates


def print_csv():
    print(get_df())


def replace_exercise_names(old_name, new_name):
    df = get_df()
    
    for num, data in df.iterrows():
        name = data['exercise']
        if name == old_name:
            df.loc[num, 'exercise'] = new_name

    df.to_csv(CSV_PATH, index=False)

