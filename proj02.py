##############################################################################
# CSE 231 Project 02
#
# Until user enters negative number
#   Get income
#   For both 2017 and 2018:
#     Pick the correct tax bracket
#       Calculate taxes
#     Calculate difference between the two
#     Print everything
##############################################################################

# Get income and convert to int inline
income = int(input("Enter income as an integer with no commas: "))
while income >= 0:

    # 2017 tax bracket detection and calculation
    remainder = income
    seventeen = 0

    if income <= 9325:
        seventeen += .1 * income

    if 9326 <= income <= 37950:
        seventeen += 9325 * 0.1
        remainder -= 9325
        seventeen += remainder * 0.15

    if 37951 <= income <= 91900:
        seventeen += 9325 * 0.1
        remainder -= 9325
        seventeen += 0.15 * (37950 - 9325)
        remainder -= 37950 - 9325
        seventeen += remainder * 0.25

    if 91901 <= income <= 191650:
        seventeen += 9325 * 0.1
        remainder -= 9325
        seventeen += 0.15 * (37950 - 9325)
        remainder -= 37950 - 9325
        seventeen += 0.25 * (91900 - 37950)
        remainder -= 91900 - 37950
        seventeen += remainder * 0.28

    if 157501 <= income <= 416700:
        seventeen += 9325 * 0.1
        remainder -= 9325
        seventeen += 0.15 * (37950 - 9325)
        remainder -= 37950 - 9325
        seventeen += 0.25 * (91900 - 37950)
        remainder -= 91900 - 37950
        seventeen += 0.28 * (191650 - 91900)
        remainder -= 191650 - 91900
        seventeen += remainder * 0.33

    if 416701 <= income <= 418400:
        seventeen += 9325 * 0.1
        remainder -= 9325
        seventeen += 0.15 * (37950 - 9325)
        remainder -= 37950 - 9325
        seventeen += 0.25 * (91900 - 37950)
        remainder -= 91900 - 37950
        seventeen += 0.28 * (191650 - 91900)
        remainder -= 191650 - 91900
        seventeen += 0.33 * (416700 - 191650)
        remainder -= 416700 - 191650
        seventeen += remainder * 0.35

    if income > 418400:
        seventeen += 9325 * 0.1
        remainder -= 9325
        seventeen += 0.15 * (37950 - 9325)
        remainder -= 37950 - 9325
        seventeen += 0.25 * (91900 - 37950)
        remainder -= 91900 - 37950
        seventeen += 0.28 * (191650 - 91900)
        remainder -= 191650 - 91900
        seventeen += 0.33 * (416700 - 191650)
        remainder -= 416700 - 191650
        seventeen += 0.35 * (418400 - 416700)
        remainder -= 418400 - 416700
        seventeen += remainder * 0.396

    # 2018 tax bracket detection and calculation
    remainder = income
    eighteen = 0

    if income <= 9525:
        eighteen += .1 * income

    if 9526 <= income <= 38700:
        eighteen += 9525 * 0.1
        remainder -= 9525
        eighteen += remainder * 0.12

    if 38701 <= income <= 82500:
        eighteen += 9525 * 0.1
        remainder -= 9525
        eighteen += 0.12 * (38700 - 9525)
        remainder -= 38700 - 9525
        eighteen += remainder * 0.22

    if 82501 <= income <= 157500:
        eighteen += 9525 * 0.1
        remainder -= 9525
        eighteen += 0.12 * (38700 - 9525)
        remainder -= 38700 - 9525
        eighteen += 0.22 * (82500 - 38700)
        remainder -= 82500 - 38700
        eighteen += remainder * 0.24

    if 157501 <= income <= 200000:
        eighteen += 9525 * 0.1
        remainder -= 9525
        eighteen += 0.12 * (38700 - 9525)
        remainder -= 38700 - 9525
        eighteen += 0.22 * (82500 - 38700)
        remainder -= 82500 - 38700
        eighteen += 0.24 * (157500 - 82500)
        remainder -= 157500 - 82500
        eighteen += remainder * 0.32

    if 200001 <= income <= 500000:
        eighteen += 9525 * 0.1
        remainder -= 9525
        eighteen += 0.12 * (38700 - 9525)
        remainder -= 38700 - 9525
        eighteen += 0.22 * (82500 - 38700)
        remainder -= 82500 - 38700
        eighteen += 0.24 * (157500 - 82500)
        remainder -= 157500 - 82500
        eighteen += 0.32 * (200000 - 157500)
        remainder -= 200000 - 157500
        eighteen += remainder * 0.35

    if income > 500000:
        eighteen += 9525 * 0.1
        remainder -= 9525
        eighteen += 0.12 * (38700 - 9525)
        remainder -= 38700 - 9525
        eighteen += 0.22 * (82500 - 38700)
        remainder -= 82500 - 38700
        eighteen += 0.24 * (157500 - 82500)
        remainder -= 157500 - 82500
        eighteen += 0.32 * (200000 - 157500)
        remainder -= 200000 - 157500
        eighteen += 0.35 * (500000 - 200000)
        remainder -= 500000 - 200000
        eighteen += remainder * 0.37

    # Calculate differences
    difference = eighteen - seventeen
    percent = (difference / seventeen) * 100

    # Print everything
    print("Income:", income)
    print("2017 tax:", round(seventeen, 2))
    print("2018 tax:", round(eighteen, 2))
    print("Difference:", round(difference, 2))
    print("Difference (percent):", abs(round(percent, 2)))

    # Get income and convert to int inline
    income = int(input("Enter income as an integer with no commas: "))
