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
        'Date': [],
        'Exercise': [],
        'Set Order': [],
        'Weight': [],
        'Reps': []
    })

    df.to_csv(CSV_PATH, index=False)

    return df


def add_csv_entry(date, exercise, set_order, weight, reps):

    df = get_df()

    new_entry = pd.DataFrame({
        'Date': [date],
        'Exercise': [exercise],
        'Set Order': [set_order],
        'Weight': [weight],
        'Reps': [reps]
    })

    new_df = pd.concat([df, new_entry], ignore_index=True)
    new_df.to_csv(CSV_PATH, index=False)

    remove_invalid_entries()


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
        date = data['Date']
        df.loc[num, 'Date'] = format_date(date)

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
        name = data['Wxercise']
        if name == old_name:
            df.loc[num, 'Exercise'] = new_name

    df.to_csv(CSV_PATH, index=False)


def one_rep_max_calc(weight, reps):
    return weight * (1 + 0.03 * reps)

def get_1RMs(exercise):

    df = get_df()

    filtered_df = df[df['Exercise'] == exercise]

    filtered_df = filtered_df.drop_duplicates(subset='Date', keep='first')

    dates = list(filtered_df['Date'])
    weights = list(filtered_df['Weight'])
    rep_amounts = list(filtered_df['Reps'])

    if len(dates) != len(weights) or len(weights) != len(rep_amounts):
        print(f"Error: Mismatched lengths - \ndate: {len(dates)}, weights: {len(weights)}, reps: {len(rep_amounts)}")
        return None, None

    maxes = []
    for weight, reps in zip(weights, rep_amounts):
        max = one_rep_max_calc(weight, reps)
        maxes.append(max)

    return dates, maxes


def add_strong_csv_entries(file_path):

    df = get_df()

    strong_df = pd.read_csv(file_path)

    filter = strong_df['Set Order'] != 'Rest Timer'

    dates = list(strong_df[filter]['Date'])
    dates = list(map(format_date, dates))
    exercises = list(strong_df[filter]['Exercise Name'])
    set_orders = list(strong_df[filter]['Set Order'])
    weights = list(strong_df[filter]['Weight'])
    rep_amounts = list(strong_df[filter]['Reps'])

    if len(dates) != len(exercises) or len(exercises) != len(set_orders) or \
        len(set_orders) != len(weights) or len(weights) != len(rep_amounts):
        print(f"Error: Mismatched lengths - dates: {len(dates)}, exercises: {len(exercises)}, set_orders: {len(set_orders)}, weights: {len(weights)}, rep_amounts: {len(rep_amounts)}")

    new_entries = pd.DataFrame({
        'Date': dates,
        'Exercise': exercises,
        'Set Order': set_orders,
        'Weight': weights,
        'Reps': rep_amounts
    })

    new_df = pd.concat([df, new_entries], ignore_index=True)
    new_df.to_csv(CSV_PATH, index=False)
