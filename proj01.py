###########################################################
#  Project #1
#
#  Algorithm
#    Prompt for rods (float)
#    Run conversions to other units
#    Print those conversions
###########################################################

# Constants
ROD = 5.0292  # meters
FURLONG = 40  # rods
MILE = 1609.34  # meters
FOOT = 0.3048  # meters
WALKING_SPEED = 3.1  # miles per hour

# Take input and convert to float inline, then print
rods = float(input("Input rods: "))
print("You input", rods, "rods.\n")

# Run conversions, but don't round yet for accuracy
meters = rods * ROD
feet = meters / FOOT
miles = meters / MILE
furlongs = rods / FURLONG
walking_hours = miles / WALKING_SPEED
walking = walking_hours * 60  # Converts hours to minutes of walking

# Round all floats for prettier printing
meters = round(meters, 3)
feet = round(feet, 3)
miles = round(miles, 3)
furlongs = round(furlongs, 3)
walking = round(walking, 3)

# Print conversions
print("Conversions")
print("Meters:", meters)
print("Feet:", feet)
print("Miles:", miles)
print("Furlongs:", furlongs)
print("Minutes to walk", rods, "rods:", walking)
