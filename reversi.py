class Board(object):
    """
    This class encapsulates a Board object. A board can be of two sizes, small
    which is a 4x4 board and a large which is 8x8 board. The board may contain 
    pieces to be played with.
    
    A 8x8 board with white piece on position (0, 0) or "a1" and a black piece on 
    position (7,7) or "h8" will look like this:

        1   2   3   4   5   6   7   8
      +---+----------------------------
    a | W |   |   |   |   |   |   |   |
      +---+----------------------------
    b |   |   |   |   |   |   |   |   |
      ---------------------------------
    c |   |   |   |   |   |   |   |   |
      ---------------------------------
    d |   |   |   |   |   |   |   |   |
      ---------------------------------
    e |   |   |   |   |   |   |   |   |
      ---------------------------------
    f |   |   |   |   |   |   |   |   |
      ---------------------------------
    g |   |   |   |   |   |   |   |   |
      ---------------------------------
    h |   |   |   |   |   |   |   | B |
      ---------------------------------
    """

    def __init__(self, length=8):
        """
        The default size of the board is 8x8. It allocates the cells according
        to the given length of the board. i.e. It will create a NxN list of
        lists of None if the provided length is N.
        """
        if length > 1:
            self.length = length    # the length of the board
            # running a loop to build a 2D list into cell
            # (i.e. list of lists)
            self.cell = [[None for c in range(self.length)] \
                                for r in range(self.length)]
        else:
            raise ValueError("The minimum allowed length of a board is 2.")

    def is_free(self, row, col):
        """
        Resturns True if the given position (i.e. tuple) is free.
        """
        return self.cell[row][col] is None

    def place(self, row, col, piece):
        """
        Places a piece at the position given by the row-column index.
        This does not check any validity condition.
        """
        self.cell[row][col] = piece

    def get(self, row, col):
        """
        Gets the piece located at the position indexed by the row-column value.
        Does not check any validity condition.
        """
        return self.cell[row][col]

    def remove(self, row, col):
        """
        Removes a piece from the position given by the row-column index.
        This does not check any validity condition.
        """
        self.cell[row][col] = None

    def is_empty(self):
        """
        Returns True if the whole board is empty.
        """
        for r in range(self.length):
            for c in range(self.length):
                if not self.is_free(r, c):
                    return False
        return True

    def is_full(self):
        """
        Returns True if the whole board is filled up.
        """
        for r in range(self.length):
            for c in range(self.length):
                if self.is_free(r, c):
                    return False
        return True

    def display(self, count=None):
        """
        Displays the board, if a count of black and white pieces (in a tuple)
        is provided, it will show the counts at the bottom.
        """
        print(self)
        if count is not None:
            print("  Black: {:d}, White: {:d}"\
                  .format(count[0], count[1]))

    def __str__(self):
        """
        The string representation of the board.
        """
        vline = '\n' + (' ' * 2) + ('+---' * self.length) + '+' + '\n'
        numline = ' '.join([(' ' + str(i) + ' ') \
                            for i in range(1, self.length + 1)])
        str_ = (' ' * 3) + numline + vline
        for r in range(0, self.length):
            str_ += chr(97 + r) + ' |'
            for c in range(0, self.length):
                str_ += ' ' + \
                    (str(self.cell[r][c]) \
                         if self.cell[r][c] is not None else ' ') + ' |'
            str_ += vline
        return str_

    def __repr__(self):
        """
        Function for the REPL printing.
        """
        return self.__str__()
                

class Piece(object):
    """
    This class encapsulates a Piece object. In the Reversi game a piece is
    a small piece which is colored black on once side and white on the other.
    """
    
    """ The symbols for the pieces: black and white circles. """
    # These symbols might not work on mimir
    symbols = [u"\u2593", u"\u2591"] # box-element unicode
    # symbols = ['â–“', 'â–‘'] # box-element ascii
    # If that's the case, then use this instead.
    # symbols = ['B', 'W']
    
    def __init__(self, color_ = 'black'):
        """
        The default color is always black, i.e. 'black'.
        """
        if color_.isalpha():
            color_ = color_.lower()
            if color_ == 'black' or color_ == 'white':
                self.__color = color_.lower()
            else:
                raise ValueError("A piece must be \'black\' or \'white\'.")
        else:
            raise ValueError("A piece must be \'black\' or \'white\'.")
        
    def color(self):
        """
        Returns the top color of the piece. 
        """
        return self.__color
    
    def flip_color(self):
        """
        Returns the bottom color of the piece.
        """
        return 'black' if self.__color == 'white' else 'white'
        
    def is_black(self):
        """
        Returns a boolean True if the piece is black.
        """
        return self.__color == 'black'
    
    def is_white(self):
        """
        Returns a boolean True if the piece is white.
        """
        return self.__color == 'white'

    def flip(self):
        """
        Flip a piece.
        """
        self.__color = 'black' if self.__color == 'white' else 'white'

    def __str__(self):
        """
        String represetation of a piece.
        """
        if self.__color == 'black':
            return self.symbols[0]
        else:
            return self.symbols[1]

    def __repr__(self):
        """
        The function for the REPL printing.
        """
        return self.__str__()
    
if __name__ == "__main__":
    """
    The main function tests all the capabilities of Piece and Board class.
    """
    bp = Piece()
    wp = Piece('white')
    print("bp: ", bp, ", wp: ", wp)
    bp.flip()
    wp.flip()
    print("bp: ", bp, ", wp: ", wp)
    print("bp.is_black(): ", bp.is_black(), ", wp.is_white(): ", wp.is_white())
    print("bp.color(): ", bp.color(), ", wp.color(): ", wp.color())
    print("bp.flip_color(): ", bp.flip_color(), \
          ", wp.flip_color(): ", wp.flip_color())

    b2 = Board(2)
    b4 = Board(4)
    b6 = Board(6)
    b8 = Board(8)
    b10 = Board(10)
    print("b2:")
    print(b2)
    print("b4:")
    print(b4)
    print("b6:")
    print(b6)
    print("b8:")
    print(b8)
    print("b10:")
    print(b10)
    print("b10.is_empty(): ", b10.is_empty())

    b2.place(0, 0, bp)
    print("b2:")
    print(b2)
    print("b2.is_empty(): ", b2.is_empty())
    print("b2.is_free(0, 0): ", b2.is_free(0, 0), \
          ", b2.is free(0, 1): ", b2.is_free(0, 1))
    b2.remove(0, 0)
    print("b2.remove(0, 0):\n", b2)
    print("b2.is_free(0, 0): ", b2.is_free(0, 0))
    b2.place(0, 0, bp)
    print("b2.place(0, 0, bp)):\n", b2)
    p = b2.get(0, 0)
    print("p = b2.get(0, 0)): ", p)
    p.flip()
    print("p.flip(): ", p)
    print("b2:")
    print(b2)
    b2.display((0, 0))
    try:
        b1 = Board(1)
    except ValueError as err:
        print(str(err.__class__), err)
