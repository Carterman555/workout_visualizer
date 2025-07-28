import pandas as pd
import os
import subprocess
import traceback

from helper import format_date

CSV_PATH = "data/processed"

def csv_exists(file_name):
    file_path = os.path.join(CSV_PATH, file_name)
    return os.path.exists(file_path)


def any_csv_exists():
    return len(os.listdir(CSV_PATH)) > 0


def get_csv_df(file_name):
    file_path = os.path.join(CSV_PATH, file_name)

    if csv_exists(file_name):
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"Error trying to read csv {e}. Edit csv to correct format.")
    else:
        df = create_new_csv(file_name)
        print("Created new file")

    return df


def get_all_dfs():
    dfs = []
    for file_name in os.listdir(CSV_PATH):
        df = get_csv_df(file_name)
        dfs.append(df)
    return dfs


def get_unified_df():

    unified_df = pd.DataFrame()
    dfs = get_all_dfs()
    for df in dfs:
        unified_df = pd.concat([unified_df, df], ignore_index=True)

    return unified_df
        

def create_new_csv(file_name):

    df = pd.DataFrame({
        'Date': [],
        'Exercise': [],
        'Set Order': [],
        'Weight': [],
        'Reps': []
    })

    file_path = os.path.join(CSV_PATH, file_name)
    df.to_csv(file_path, index=False)

    return df


def add_csv_entry(file_name, date, exercise, set_order, weight, reps):

    file_path = os.path.join(CSV_PATH, file_name)
    df = get_csv_df(file_path)

    new_entry = pd.DataFrame({
        'Date': [date],
        'Exercise': [exercise],
        'Set Order': [set_order],
        'Weight': [weight],
        'Reps': [reps]
    })

    new_df = pd.concat([df, new_entry], ignore_index=True)
    new_df.to_csv(file_path, index=False)

    remove_invalid_entries(file_name)


def open_csv_notepad(file_name):
    file_path = os.path.join(CSV_PATH, file_name)
    subprocess.run(["notepad.exe", file_path])


def remove_invalid_entries(file_name):
    df = get_csv_df(file_name)

    new_df = df.drop_duplicates().dropna()

    file_path = os.path.join(CSV_PATH, file_name)
    new_df.to_csv(file_path, index=False)


# format dates (set invalid dates to none, so those entries will be removed)
def format_dates():
    for file_name in os.listdir(CSV_PATH):
        df = get_csv_df(file_name)

        for num, data in df.iterrows():
            date = data['Date']
            df.loc[num, 'Date'] = format_date(date)

        file_path = os.path.join(CSV_PATH, file_name)
        df.to_csv(file_path, index=False)


def process_csvs():
    format_dates()
    for file_name in os.listdir(CSV_PATH):
        remove_invalid_entries(file_name)


def print_csvs():
    for file_name, df in zip(os.listdir(CSV_PATH), get_all_dfs()):
        print(f"\n{file_name}:")
        print(f"{df}\n")


def replace_exercise_names(file_name, old_name, new_name):
    df = get_csv_df(file_name)

    for num, data in df.iterrows():
        name = data['Exercise']
        if name == old_name:
            df.loc[num, 'Exercise'] = new_name

    file_path = os.path.join(CSV_PATH, file_name)
    df.to_csv(file_path, index=False)


def replace_exercise_names_all(old_name, new_name):
    for file_name in os.listdir(CSV_PATH):
        replace_exercise_names(file_name, old_name, new_name)


def one_rep_max_calc(weight, reps):
    return weight * (1 + 0.03 * reps)

def get_1RMs(exercise):

    df = get_unified_df()

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


def add_strong_csv_entries(strong_file_path, export_file_name):

    df = get_csv_df(export_file_name)

    strong_df = pd.read_csv(strong_file_path)

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
    
    file_path = os.path.join(CSV_PATH, export_file_name)
    new_df.to_csv(file_path, index=False)


def get_exercise_names():
    df = get_unified_df()
    if df is not None and 'Exercise' in df.columns:
        return list(df['Exercise'])
    return []


def delete_csv_file(file_name):
    file_path = os.path.join(CSV_PATH, file_name)
    os.remove(file_path)


def delete_all_csv_files():
    for file_name in os.listdir(CSV_PATH):
        delete_csv_file(file_name)