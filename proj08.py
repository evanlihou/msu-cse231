"""
PROJ 08
Gets and analyzes pollution data for a particular state

Prompts for a state
Prompts for a year
Displays data for that state
Prompts the user to plot the data
"""
import csv
import pylab

# Constants
FILE_PROMPT = "Input a file name: "
FILE_ERROR = "Error opening file. Please try again."


def open_file():
    """Opens a file with error checking

    Returns:
        file pointer
    """

    file_str = input(FILE_PROMPT)
    file_opened = False
    while not file_opened:
        try:
            fp = open(file_str)
            file_opened = True
        except FileNotFoundError:
            print(FILE_ERROR)
            file_str = input(FILE_PROMPT)
    return fp


def ppb(row, data_index):
    """Checks whether a number is in parts per billion, and if not makes it so

    Arguments:
        row {list} -- A row from the CSV data file
        data_index {int} -- The index of the number you want returned ppb'ed

    Returns:
        int -- Concentration of the given index in parts per billion
    """

    if "million" in row[data_index-1]:
        return float(row[data_index])*1000
    # Otherwise..
    return float(row[data_index])

def read_file(fp):
    """Reads a CSV file and returns the relevant data after removing headers

    Arguments:
        fp {file pointer} -- The file to read from

    Returns:
        dict -- A dictionary with keys as state names and values as lists of
            lists with format [city, date, no2mean, o3mean, so2mean, comean]
    """

    csv_data = csv.reader(fp)
    next(csv_data)
    data_dict = {}
    previous_city = ""
    previous_date = ""
    for row in csv_data:
        state = row[5]
        city = row[7]
        date = row[8]
        no2mean = ppb(row, 10)
        o3mean = ppb(row, 15)
        so2mean = ppb(row, 20)
        comean = ppb(row, 25)

        # Check for blank AQI values
        if row[13] == "" or row[18] == "" or row[23] == "" or row[28] == "":
            continue

        # Check for duplicates
        if city == previous_city and date == previous_date:
            continue
        previous_city = city
        previous_date = date

        if state not in data_dict.keys():
            data_dict[state] = []

        data_dict[state].append([city, date, no2mean, o3mean, so2mean, comean])

    fp.close()
    return data_dict


def total_years(D, state):
    """Gets the total for all years 2000-2016 for the given state

    Arguments:
        D {dictionary} -- The dictionary returned from read_file
        state {str} -- The state to search for

    Returns:
        tuple -- with format ([[0,0,0,0] for year in 2000-2016], overall max,
                              overall min)
    """

    raw_state_data = D[state]
    state_data_w_years = []
    r_list = [] # 2000-2016
    for item in raw_state_data:
        date = item[1]
        year = int(date.split('/')[2])
        state_data_w_years.append([year, item])
    # state_data_w_years.sort()
    for year in range(2000, 2016 + 1):
        no2 = 0
        o3 = 0
        so2 = 0
        co = 0
        for item in state_data_w_years:
            if item[0] == year:
                no2 += item[1][2]
                o3 += item[1][3]
                so2 += item[1][4]
                co += item[1][5]
        r_list.append([no2, o3, so2, co])

    # Get min and max
    flat_list = [item for year in r_list for item in year]

    return (r_list, max(flat_list), min(flat_list))


def cities(D, state, year):
    """Gets total pollution for each city in a given state

    Arguments:
        D {dictionary} -- The dictionary returned from read_file()
        state {string} -- The state to get data for
        year {int} -- The year to get data

    Returns:
        dictionary -- a dictionary with format {city: [no2, o3, so2, co], ...}
    """

    ret_dict = {}
    for data in D[state]:
        if int(data[1].split("/")[2]) == year:
            city = data[0]
            if city not in ret_dict.keys():
                ret_dict[city] = [0, 0, 0, 0]

            ret_dict[city][0] += data[2]
            ret_dict[city][1] += data[3]
            ret_dict[city][2] += data[4]
            ret_dict[city][3] += data[5]
    return ret_dict


def months(D, state, year):
    """Gets top months for each pollutant

    Arguments:
        D {dict} -- The dictionary returned from read_file()
        state {str} -- State to get data for
        year {int} -- Year to get data for

    Returns:
        tuple of lists -- Inner lists contain top 5 months for each pollutant
    """

    months_list = [[0, 0, 0, 0] for i in range(1, 12+1)]
    # Get data for each month
    for data in D[state]:
        if int(data[1].split("/")[2]) == year:
            month_int = int(data[1].split("/")[0])
            month_total = months_list[month_int-1]
            month_total[0] += data[2]
            month_total[1] += data[3]
            month_total[2] += data[4]
            month_total[3] += data[5]

    # Create top lists for each pollutant
    no2 = [i[0] for i in months_list]
    o3 = [i[1] for i in months_list]
    so2 = [i[2] for i in months_list]
    co = [i[3] for i in months_list]

    top_no2 = sorted(no2, reverse=True)[:5]
    top_o3 = sorted(o3, reverse=True)[:5]
    top_so2 = sorted(so2, reverse=True)[:5]
    top_co = sorted(co, reverse=True)[:5]

    return (top_no2, top_o3, top_so2, top_co)



def display(totals_list, maxval, minval, D_cities, top_months):
    """Displays the data gotten from other functions in this module

    Arguments:
        totals_list {list} -- List of totals by year
        maxval {float} -- Maximum overall value
        minval {float} -- Minimum overall value
        D_cities {dict} -- Dict with keys cities and values pollution levels
        top_months {list} -- list of lists with top months for each pollution
    """

    print("\nMax and Min pollution")
    print("\n{:>10s}{:>10s}".format("Minval", "Maxval"))
    print("{:>10.2f}{:>10.2f}".format(minval, maxval))

    print("\nPollution totals by year")
    print("\n{:<6s}{:>8s} {:>8s} {:>8s} {:>10s}".format("Year", "NO2", "O3", "SO2", "CO"))
    for year, totals in enumerate(totals_list):
        if totals == [0, 0, 0, 0]:
            continue
        print("{:<6d}{:>8.2f} {:>8.2f} {:>8.2f} {:>10.2f}".format(year+2000, *totals))

    print("\nPollution by city")
    print("\n{:<16s}{:>8s} {:>8s} {:>8s} {:>8s}".format("City", "NO2", "O3", "SO2", "CO"))
    for city, totals in D_cities.items():
        print("{:<16s}{:>8.2f} {:>8.2f} {:>8.2f} {:>8.2f}".format(city, *totals))

    print("\nTop Months")
    print("\n{:>8s} {:>8s} {:>8s} {:>8s}".format("NO2", "O3", "SO2", "CO"))
    for i in range(5):
        no2 = top_months[0][i]
        o3 = top_months[1][i]
        so2 = top_months[2][i]
        co = top_months[3][i]
        print("{:>8.2f} {:>8.2f} {:>8.2f} {:>8.2f}".format(no2, o3, so2, co))


def plot_years(totals_list, maxval, minval):
    """Plots the data

    Arguments:
        totals_list {list} -- List of totals by year
        maxval {float} -- Unused.
        minval {float} -- Unused.
    """

    no2 = []
    so2 = []
    o3 = []
    co = []
    years = []

    for i in range(2000, 2017):
        years.append(i)

    for i in totals_list:
        no2.append(i[0])
        o3.append(i[1])
        so2.append(i[2])
        co.append(i[3])

    fig, ax = pylab.subplots()
    pylab.ylabel('Average Concentration')
    pylab.xlabel('Year')
    pylab.title('Total Average Pollution Per Year')
    ax.plot(years, no2, 'ro')
    ax.plot(years, o3, 'bo')
    ax.plot(years, so2, 'go')
    ax.plot(years, co, 'yo')
    ax.plot(years, no2, 'ro', label='NO2')
    ax.plot(years, o3, 'bo', label='O3')
    ax.plot(years, so2, 'go', label='SO2')
    ax.plot(years, co, 'yo', label='CO')

    ax.legend(loc='upper right', shadow=True, fontsize='small')

    pylab.show()

def get_state(data):
    """Get state with error checking

    Arguments:
        data {dict} -- Data returned from read_file(), to check state exists

    Returns:
        str or None -- returns state name or None if quit
    """

    state_entered = False
    while not state_entered:
        state = input("Enter a state ('quit' to quit): ")
        if state.lower() == "quit":
            return None
        elif state not in data.keys():
            print("Invalid state.")
        else:
            return state

def get_year():
    """Get year with error checking

    Returns:
        str or None -- returns state name or None if quit
    """

    year_entered = False
    while not year_entered:
        year = input("Enter a year ('quit' to quit): ")
        if year.lower() == "quit":
            return None
        if year.isdigit():
            year = int(year)
        else:
            print("Invalid year.")
            continue
        if year not in range(2000, 2017+1):
            print("Invalid year.")
        else:
            return year


def main():
    """See module docstring for description of main()
    """

    data = read_file(open_file())
    while True:
        state = get_state(data)
        if not state:
            break

        year = get_year()
        if not year:
            break

        total_years_data = total_years(data, state)
        cities_data = cities(data, state, year)
        months_data = months(data, state, year)

        display(*total_years_data, cities_data, months_data)

        plot_str = input("Do you want to plot (yes/no)? ")
        if plot_str.lower() in ['yes', 'no', 'y', 'n']:
            if plot_str.lower() == 'yes' or plot_str.lower() == 'y':
                plot_years(*total_years_data)
        else:
            print("It was a yes or no question... Start over.")


if __name__ == "__main__":
    main()
