import matplotlib.pyplot as plt

def open_line_plot(title, ylabel, dates, y_values):

    plt.plot(dates, y_values, marker='o', label="Data Points")

    plt.title(title)
    plt.xlabel("Date") 
    plt.ylabel(ylabel)  

    plt.show()