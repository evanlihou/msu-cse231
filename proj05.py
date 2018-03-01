"""
Project 5

Gets a file name from the user
Asks the user whether they want to search by countries or regions
Prompts for a search string
For each country that matches
    Print the data for that country
Find and print the mean happiness score for the matching countries
"""


def open_file():
    '''
    Prompts the user for a file name, does error checking, opens the file
    Returns: list of tuples of country data
    '''
    file_str = input("Input a file name: ")
    while True:
        try:
            fp = open(file_str, 'r')
            data = []
            for line in fp:
                data.append(tuple(line.split(',')))
            return data
        except FileNotFoundError:
            print("Unable to open the file. Please try again.")
            file_str = input("Input a file name: ")


def display_line(country_name=None, region_name=None, happiness_score=None):
    '''
    Prints country data using a uniform format
    country_name (str): Name of the country
    region_name (str): Name of the country's region
    happiness_score (float): Happiness score of the country
    Does not return anything.
    '''
    print("{:24s}{:<32s}{:<17.2f}".format(
            country_name, region_name, happiness_score))


def read_data(data, input_str, search_str):
    '''
    Searches for matching countries based on region/country and search string
    data (list of tuples): Data for all countries (country, region, score)
    input_str (str): Whether to search countries or regions
    search_str (str): What to search for
    Returns average of scores from the matches to be used in printing a footer
    '''
    match_scores = []
    if input_str == "1":
        search_index = 0  # Search countries
    elif input_str == "2":
        search_index = 1  # Search regions
    for country in data:
        if search_str.lower() in country[search_index].lower():
            display_line(country[0], country[1], float(country[2]))
            match_scores.append(float(country[2]))
    if len(match_scores) != 0:
        average = sum(match_scores)/len(match_scores)
    else:
        average = 0.0
    return average


def main():
    '''
    The main function that calls other functions prints the table
    '''
    fp = open_file()
    while True:
        input_str = input("Input 1 to search in country names,"
                          " 2 to search in regions: ")
        if input_str == "1" or input_str == "2":
            break
        else:
            print("Invalid choice, please try again!")
    search_str = input("What do you want to search for? ")

    # Table Header
    print("{:24s}{:<32s}{:<17s}".format(
            "Country", "Region", "Happiness Score"))
    print("-"*71)
    # Data
    average_score = read_data(fp, input_str, search_str)
    # Table Footer
    print("-"*71)
    print("{:24s}{:<32s}{:<17.2f}".format(
            "Average Happiness Score", "", average_score))


if __name__ == '__main__':
    main()
