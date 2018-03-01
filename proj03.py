"""
CSE 231 Proj 03

Algorithm:
    Until the user is done
        Set constant strings
        Get user's desired conversion information, and perform error checking
        Make API call to Google Finance
        Format response and give to user

"""

import urllib.request

# Set constants so they can be easily changed later
FROM_INPUT = "What is the original currency? "
TO_INPUT = "What currency do you want to convert to? "
AMT_INPUT = "How much do you want to convert (int)? "
PROCEED_INPUT = "Do you want to convert another currency? "

API_DOMAIN = "https://finance.google.com"
API_ENDPOINT = "/finance/converter?a={}&from={}&to={}"

# Run until the user says no and breaks the while
while True:
    # Get the user's desired conversion
    currency_from = input(FROM_INPUT).upper()
    currency_to = input(TO_INPUT).upper()
    currency_amt = input(AMT_INPUT)
    # Check the amount was actually an int
    while not currency_amt.isdigit():
        print("The value you input must be an integer. Please try again.")
        currency_amt = input(AMT_INPUT)
    currency_amt = int(currency_amt)

    # Make the API call
    url = API_DOMAIN+API_ENDPOINT \
          .format(currency_amt, currency_from, currency_to)

    # Interpret the API call
    response = urllib.request.urlopen(url)
    result = str(response.read())
    conversion_start = result.rfind('<span class=bld>')+len('<span class=bld>')
    conversion_end = result.rfind('</span>')-4
    # Final conversion, expressed as a float with more than two decimals
    conversion = float(result[conversion_start:conversion_end])

    # Put together and format the output
    output = "{} {} is {:.2f} {}" \
             .format(currency_amt, currency_from, conversion, currency_to)
    print()
    print(output)

    # Ask if the user wants to do more conversions
    proceed = input(PROCEED_INPUT)
    if proceed.lower() == "no":
        break
