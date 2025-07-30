# Workout Visualizer
--- 
Workout Visualizer is an app to track, store, and visualize the progress of your workouts. It can also import data from the Strong app.

## Getting Started
---
### Prerequisites:
- Knowledge of basic CLI usage
- Python 3.6+
- Tkinter
	 - When installing Python check "tcl/tk and IDLE" under optional features

### Setup:
1. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Initialize the correct virtual environment: `source .venv/bin/activate`
3. Add dependencies
	- uv add argparse
	- uv add datetime
	- uv add matplotlib
	- uv add pandas
	- uv add pytrie

### Commands:
The default file name is default.csv.

##### `add`
Add an exercise entry which represents one set

`./run.sh add <date> <exercise> <set_num> <weight> <reps> [-f FILE_NAME]`

Example:
`./run.sh add 7/30/2025 "Bench Press" 1 135 8`

##### `delete`
Deletes csv file(s) storing workout data.

`./run.sh delete [-f FILE_NAME] [-a]`

`-a`: Delete **all** CSV files

##### `open`
Open file in notepad

`./run.sh open [-f FILE_NAME]`

##### `print`
Prints workout data

`./run.sh print`

##### `list`
List out all csv files

`./run.sh list`

##### `process`
Removes invalid entries and formats dates

`./run.sh process`

##### `gui`
Open gui for entering workout sets

`./run.sh gui [-f FILE_NAME]`

##### `replace`
Replace all instances of an exercise name with a new one

`./run.sh replace <old_name> <new_name> [-f FILE_NAME] [-a]`

`-a`: Replace instances in **all** CSV files

##### `graph`
Show a graph to visualize progress over time

`./run.sh graph [-e EXERCISE] [-a]`

`-a`: The graph can switch between all exercises

##### `strong`
 Import data from Strong app

`./run.sh strong <path> [-f FILE_NAME]`


##### For help
./run.sh --help
./run.sh [command] -h