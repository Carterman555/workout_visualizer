import argparse

from datetime import datetime

from gui import GUI
from helper import *
from csv_helper import *


def main():
    parser = argparse.ArgumentParser(description="Workout Visualizer")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # add
    add_parser = subparsers.add_parser('add', help='Add a word to the file')
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

    # process
    process_parser = subparsers.add_parser('process', help='Removes invalid entries and formats dates')

    # print
    print_parser = subparsers.add_parser('print', help='Prints workout data')

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
    elif args.command == 'process':
        pass
    elif args.command == 'print':
        print_csv()



if __name__ == "__main__":
    main()
