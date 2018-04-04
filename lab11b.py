"""
LAB 11B:
A time class and demonstration of the class.
"""

class Time():
    """
    A class to represent a specific time
    """


    def __init__(self, __hour=0, __min=0, __sec=0):
        """Constructs the time class.

        Keyword Arguments:
            __hour {int} -- hours of the time (default: {0})
            __min {int} -- minutes of the time (default: {0})
            __sec {int} -- seconds of the time (default: {0})
        """
        self.hour = __hour
        self.min = __min
        self.sec = __sec


    def __repr__(self):
        """Creates the shell representation of a time with proper formatting

        Returns:
            string -- the representation of the time
        """

        outstr = "Class Time: {:0>2d}:{:0>2d}:{:0>2d}"
        return outstr.format(self.hour, self.min, self.sec)


    def __str__(self):
        """Creates the string representation of a time with proper formatting

        Returns:
            string -- the representation of the time
        """

        outstr = "{:0>2d}:{:0>2d}:{:0>2d}"
        return outstr.format(self.hour, self.min, self.sec)


    def from_str(self, time_str):
        """Updates the Time in place with a given str

        Arguments:
            time_str {str} -- Time to convert with format hh:mm:ss
        """

        time_lst = time_str.split(":")
        self.hour = int(time_lst[0])
        self.min = int(time_lst[1])
        self.sec = int(time_lst[2])


    def add_times(self, other):
        """Adds two times together

        Arguments:
            other {Time} -- Other time to add to this one

        Returns:
            Time -- A new instance of time after addition
        """

        new_hour = self.hour + other.hour
        new_min = self.min + other.min
        if new_min > 60:
            new_hour += new_min // 60
            new_min = new_min % 60
        new_sec = self.sec + other.sec
        if new_min > 60:
            new_min += new_sec // 60
            new_sec = new_sec % 60

        return Time(new_hour, new_min, new_sec)


    def __add__(self, other):
        return self.add_times(other)


    # End Time class


A = Time(12, 25, 30)

print(A)
print(repr(A))
print(str(A))
print()

B = Time(2, 25, 3)

print(B)
print(repr(B))
print(str(B))
print()

C = Time(2, 25)

print(C)
print(repr(C))
print(str(C))
print()

D = Time()

print(D)
print(repr(D))
print(str(D))
print()

D.from_str("03:09:19")

print(D)
print(repr(D))
print(str(D))
