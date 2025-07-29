import argparse
import sys
from datetime import datetime

from gui import GUI
from helper import *
from csv_helper import *
from graph_helper import *


def file_check(file_name):
    if not file_name.endswith('.csv'):
        print(f"Error: file is not csv: {file_name}")
        return False

    if csv_exists(file_name):
        return True
    else:
        print(f"Error: file doesn't exist: {file_name}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Workout Visualizer')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # add
    add_parser = subparsers.add_parser('add', help='Add an exercise entry which represents one set')
    add_parser.add_argument('file_name', help='name of file to add entry to')
    add_parser.add_argument('date', help='date of exercise')
    add_parser.add_argument('exercise', help='exercise name')
    add_parser.add_argument('set_num', type=int, help='order of set')
    add_parser.add_argument('weight', type=float, help='weight used in exercise')
    add_parser.add_argument('reps', type=int, help='reps completed in set')

    # Delete
    delete_parser = subparsers.add_parser('delete', help='Deletes csv file(s) storing workout data.')
    delete_parser.add_argument('-f', '--file_name', default='default.csv', help='file to delete')
    delete_parser.add_argument('-a', '--all', action='store_true', help='delete all files')

    # open
    open_parser = subparsers.add_parser('open', help='Open file in notepad')
    open_parser.add_argument('file_name', default="default.csv", help='name of file to open')

    # print
    subparsers.add_parser('print', help='Prints workout data')

    # process
    subparsers.add_parser('process', help='Removes invalid entries and formats dates')

    # gui
    gui_parser = subparsers.add_parser('gui', help='Open gui for entering workout sets')
    gui_parser.add_argument('-f', '--file_name', default='default.csv', help='file name to write to')

    # replace
    replace_parser = subparsers.add_parser('replace', help='Replace all instances of an exercise name with a new one')
    replace_parser.add_argument('old_name', help='current exercise name to replace')
    replace_parser.add_argument('new_name', help='new exercise name to use')
    replace_parser.add_argument('-f', '--file_name', default='default.csv', help='file name to replace exercises in')
    replace_parser.add_argument('-a', '--all', action='store_true', help='replace in all files')

    # graph
    graph_parser = subparsers.add_parser('graph', help='Show a graph to visualize progress over time')
    graph_parser.add_argument('-e', '--exercise', help='name of exercise to graph')
    graph_parser.add_argument('-a', '--all', action="store_true", help='name of exercise to graph')

    # import strong data
    strong_parser = subparsers.add_parser('strong', help='Import data from Strong app')
    strong_parser.add_argument('path', help='path to strong export')
    strong_parser.add_argument('-f', '--file_name', default='strong.csv', help='file name to export exercises to')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'add':
        date = format_date(args.date)
        add_csv_entry(args.file_name, date, args.exercise, args.set_num, args.weight, args.reps)
    elif args.command == 'delete':
        if args.all:
            delete_all_csv_files()
        else:
            if not file_check(args.file_name):
                return
            
            delete_csv_file(args.file_name)
    elif args.command == 'open':
        if not file_check(args.file_name):
            return
        
        open_csv_notepad(args.file_name)
    elif args.command == 'print':
        print_csvs()
    elif args.command == 'process':
        process_csvs()
    elif args.command == 'gui':
        GUI(args.file_name)
    elif args.command == 'replace':
        if args.all:
            replace_exercise_names_all(args.old_name, args.new_name)
        else:
            if not file_check(args.file_name):
                return
            
            replace_exercise_names(args.file_name, args.old_name, args.new_name)
    elif args.command == 'graph':
        if args.all:
            exercises = list(get_exercise_names())
            all_dates = []
            all_maxes = []
            for exercise in exercises:
                dates, maxes = get_1RMs(exercise)
                all_dates.append(dates)
                all_maxes.append(maxes)
            open_line_plots(f"1RM", exercises, all_dates, all_maxes)
        else:
            dates, maxes = get_1RMs(args.exercise)
            open_line_plot(f"{args.exercise} 1RM", "1RM", dates, maxes)
    elif args.command == 'strong':
        add_strong_csv_entries(args.path, args.file_name)



if __name__ == "__main__":
    main()
