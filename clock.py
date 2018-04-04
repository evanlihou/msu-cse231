"""
A clock class.
"""


class Time():
    """
    A class to represent time
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