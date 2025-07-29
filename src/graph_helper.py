import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.widgets as widgets
import pandas as pd

def open_line_plot(title, ylabel, dates, y_values):

    dates = pd.to_datetime(dates)

    df = pd.DataFrame({'date': dates, 'y': y_values}).sort_values('date')
    dates = df['date']
    y_values = df['y']

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


def open_line_plots(title, exercises, dates_list, y_values_list):

    dates_list = [pd.to_datetime(dates) for dates in dates_list]
    plot_num = len(dates_list)

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.3)  # Increase bottom margin for buttons

    current_plot = [0]

    def plot_index(idx):
        ax.clear()

        df = pd.DataFrame({'date': dates_list[idx], 'y': y_values_list[idx]}).sort_values('date')
        dates = df['date']
        y_values = df['y']

        ax.plot(dates, y_values, marker='o')
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.set_xlabel("Date")
        ax.set_title(f"{exercises[idx]} {title}")
        plt.setp(ax.get_xticklabels(), rotation=45)
        fig.canvas.draw_idle()

    # Move buttons lower by decreasing the y-position
    axprev = plt.axes([0.7, 0.01, 0.1, 0.075])
    axnext = plt.axes([0.81, 0.01, 0.1, 0.075])
    bnext = widgets.Button(axnext, 'Next')
    bprev = widgets.Button(axprev, 'Previous')

    def next_plot(event):
        if current_plot[0] < plot_num - 1:
            current_plot[0] += 1
            plot_index(current_plot[0])

    def prev_plot(event):
        if current_plot[0] > 0:
            current_plot[0] -= 1
            plot_index(current_plot[0])

    bnext.on_clicked(next_plot)
    bprev.on_clicked(prev_plot)

    plot_index(current_plot[0])
    plt.show()