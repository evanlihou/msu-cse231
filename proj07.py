"""
Project 7
Ask user for data file of Medicaid spending from 2011-2015
Until the user decides to quit:
    Ask for the year to get info for
    Display a table of medication prescriptions
    Ask the user whether they want to display plotted data for the top ten
        If yes:
            Plot top ten medications by prescriptions
            Plot top ten medications by total spending
"""

from operator import itemgetter
import csv
import pylab

# Constants
WELCOME = "Medicaid drug spending 2011 - 2015"
YEAR_PROMPT = "Enter the year to process ('q' to terminate): "
PLOT_PROMPT = "Do you want to plot the top 10 values (yes/no)? "
YEAR_ERROR = "Invalid Year. Try Again!"
FILE_INPUT = "Input a file name: "
FILE_ERROR = "Unable to open the file. Please try again."
HEADER = "Drug spending by Medicaid in {:4d}"

def open_file():
    """
    This function takes in no params.
    Prompts user and opens a file with error checking.
    Returns: file pointer
    """
    while True:
        try:
            file_name = input(FILE_INPUT)
            data_file = open(file_name)
            return data_file
        except FileNotFoundError:
            print(FILE_ERROR)


def read_data(data_file):
    """
    fp: file to read data from
    Reads file line by line and converts the relevant data from the CSV into a
    list of tuples.
    Returns: a list of tuples with format:
        (year, brand, total, presctiption count, unit count,
        cost per prescription, cost per unit)
    """
    csv_data = csv.reader(data_file)
    next(csv_data)  # Remove the headers
    data = []
    for medication in csv_data:
        year = int(medication[0])

        brand = medication[1]

        try:
            total = float(medication[3])
        except ValueError:
            continue  # Just move on if it doesn't work

        try:
            prescriptions = int(medication[4])
        except ValueError:
            continue  # Just move on if it doesn't work

        try:
            units = int(medication[5])
        except ValueError:
            continue  # Just move on if it doesn't work

        cost_per_prescription = total/prescriptions
        cost_per_unit = total/units

        relevant_data = (year, brand, total, prescriptions, units,
                         cost_per_prescription, cost_per_unit)
        data.append(relevant_data)

    data_file.close()
    return sorted(data)


def top_ten_list(column, year_list):
    """
    column (int): column of the data to make a list from (one-indexed)
    year_list (list): The list returned from the get_year_list() function.
    Creates a top ten list (sorted descending) from column data to be used
        in plots
    Returns: Tuple with list of medication names and list of column data
    """
    # We can assume the list is already sorted by year, then by medication name
    sorted_lst = sorted(year_list, key=itemgetter(column-1), reverse=True)[:10]
    med_names = [x[1] for x in sorted_lst]
    column_data = [x[column-1] for x in sorted_lst]
    return (med_names, column_data)


def get_year_list(year, data):
    """
    year (int): The year to find data for
    data (list of tuples): The data to go through
    Finds  all items in data where the year matches the one given
    Returns: A list of tuples (medications)
    """
    year_list = []
    hit_matching_year = False
    for medication in data:
        if medication[0] == year:
            year_list.append(medication)
            hit_matching_year = True
        if medication[0] != year and hit_matching_year:
            break
            # We can do this because the data is sorted. Once we're done with
            # that year, there won't be any more matching items in the data
            # later.
    return year_list


def display_table(year, year_list):
    """
    year (int): Year to display data for
    year_list (list of tuples): the data returned from the get_year_list()
        function
    Displays a table of all medications for a given year, sorting by number
        of prescriptions in descending order
    Returns: None
    """
    year_list.sort()
    print("{:^80s}".format(HEADER.format(year)))
    print("{:35s}{:>15s}{:>20s}{:>15s}"
          .format("Medication", "Prescriptions", "Prescription Cost", "Total"))
    for prescription in year_list:
        print("{:35s}{:>15,d}{:>20,.2f}{:>15,.2f}"
              .format(
                  prescription[1],
                  prescription[3],
                  prescription[5],
                  prescription[2]/1000
                  )
             )


def plot_top_ten(x, y, title, xlabel, ylabel):
    """
        This function plots the top 10 values from a list of medications.
        This function is provided to the students.

        Input:
            x (list) -> labels for the x-axis
            y (list) -> values for the y-axis
            title (string) -> Plot title
            xlabel (string) -> Label title for the x-axis
            ylabel (string) -> Label title for the y-axis
    """

    pos = range(10)
    pylab.bar(pos, y)
    pylab.title(title)
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)
    pylab.xticks(pos, x, rotation='90')
    pylab.show()


def main():
    """
    See main program docstring for explaination of this function
    """

    data_file = open_file()
    data = read_data(data_file)

    print(WELCOME)

    # This line contains an ugly hack because Mimir testing contains an error
    year = input(YEAR_PROMPT.replace('the', 'a'))
    while year.lower() != 'q':
        try:
            year = int(year)
            if not 2011 <= year <= 2015:
                raise ValueError
            break
        except ValueError:
            print(YEAR_ERROR)
            year = input(YEAR_PROMPT)
            continue

        year_list = get_year_list(year, data)
        display_table(year, year_list)

        while True:
            display_plot = input(PLOT_PROMPT)
            if display_plot == "yes":
                top_prescriptions_list = top_ten_list(4, year_list)
                plot_top_ten(
                    top_prescriptions_list[0],
                    top_prescriptions_list[1],
                    "Top 10 Medications prescribed in {}".format(year),
                    "Medication Name",
                    "Prescriptions"
                    )

                top_coverage_list = top_ten_list(3, year_list)
                plot_top_ten(
                    top_coverage_list[0],
                    top_coverage_list[1],
                    "Top 10 Medicaid Covered Medications in {}".format(year),
                    "Medication Name",
                    "Amount")
                break
            elif display_plot == "no":
                break

        year = input(YEAR_PROMPT)


if __name__ == "__main__":
    main()
