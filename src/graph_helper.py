import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def open_line_plot(title, ylabel, dates, y_values):

    dates = pd.to_datetime(dates)

    fig, ax = plt.subplots()
    ax.plot(dates, y_values, marker='o')

    ax.xaxis.set_major_locator(mdates.AutoDateLocator())  # auto spacing
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # readable format

    ax.set_title(title)
    ax.set_xlabel("Date") 
    ax.set_ylabel(ylabel)  

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()