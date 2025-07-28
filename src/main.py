import argparse

from datetime import datetime

from gui import GUI
from helper import *
from csv_helper import *
from graph_helper import *


def main():
    parser = argparse.ArgumentParser(description="Workout Visualizer")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # add
    add_parser = subparsers.add_parser('add', help='Add an exercise entry which represents one set')
    add_parser.add_argument('date', help='date of exercise')
    add_parser.add_argument('exercise', help='exercise name')
    add_parser.add_argument('set_num', type=int, help='order of set')
    add_parser.add_argument('weight', type=float, help='weight used in exercise')
    add_parser.add_argument('reps', type=int, help='reps completed in set')

    # clear
    clear_parser = subparsers.add_parser('clear', help='Clears all workout data')

    # open
    open_parser = subparsers.add_parser('open', help='Open file contains workout data')
    open_parser.add_argument('-n', '--nano', action='store_true', help='edit data using nano')
    open_parser.add_argument('-s', '--system', default=None, choices=['windows', 'mac', 'linux'], help='operating system')

    # print
    print_parser = subparsers.add_parser('print', help='Prints workout data')

    # process
    process_parser = subparsers.add_parser('process', help='Removes invalid entries and formats dates')

    # gui
    gui_parser = subparsers.add_parser('gui', help='Open gui for entering workout sets')
    gui_parser.add_argument('-f', '--file', default=None, help="File name to write to")

    # replace
    replace_parser = subparsers.add_parser('replace', help='Replace all instances of an exercise name with a new one')
    replace_parser.add_argument('old_name', help='current exercise name to replace')
    replace_parser.add_argument('new_name', help='new exercise name to use')

    # graph
    graph_parser = subparsers.add_parser('graph', help='Show a graph to visualize progress over time')
    graph_parser.add_argument('exercise', help='name of exercise to graph')

    # import strong data
    strong_parser = subparsers.add_parser('strong', help='Import data from Strong app')
    strong_parser.add_argument('path', help='path to strong export')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'add':
        date = format_date(args.date)
        add_csv_entry(date, args.exercise, args.set_num, args.weight, args.reps)
    elif args.command == 'clear':
        create_new_csv()
    elif args.command == 'open':
        if args.nano:
            nano_edit_csv()
        else:
            open_csv()
    elif args.command == 'print':
        print_csv()
    elif args.command == 'process':
        process_csv()
    elif args.command == 'gui':
        gui = GUI(args.file)
    elif args.command == 'replace':
        replace_exercise_names(args.old_name, args.new_name)
    elif args.command == 'graph':
        dates, maxes = get_1RMs(args.exercise)
        open_line_plot(f"{args.exercise} 1RM", "1RM", dates, maxes)
    elif args.command == 'strong':
        add_strong_csv_entries(args.path)



if __name__ == "__main__":
    main()
