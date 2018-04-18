"""
A human-played version of Reversi
    Prompt for a color and board size
    Play moves until someone wins the game or there is a draw
    Offer hints to the user
"""

import string
from operator import itemgetter
import reversi

LETTERS = string.ascii_lowercase


def indexify(position):
    """Turns a string form of position into position indexes

    Arguments:
        position {str} -- Format "a2" or "z14"

    Assumes:
        Row is <= 26 (i.e.: Only one letter long)

    Returns:
        tuple -- (x_index, y_index)
    """

    x_str = position[0]
    y_str = position[1:]
    x_index = LETTERS.index(x_str)
    y_index = int(y_str)-1
    return (x_index, y_index)


def deindexify(row, col):
    """Turns an x, y index into a string form of position

    Arguments:
        row {int} -- Index of the row (letter in return string)
        col {int} -- Index of the column (number in return string)

    Raises:
        ValueError -- When the row can not be converted to a letter

    Returns:
        str -- Format "a2" or "z14"
    """

    out_str = ""
    if row > len(LETTERS)-1:
        raise ValueError("deindexify can only handle a row value of 25 or less")
    out_str += LETTERS[row]  # Row str
    out_str += str(col+1)  # Col str
    return out_str


def initialize(board):
    """Initializes a board using the start-game rules of Reversi

    Arguments:
        board {Board} -- board to initialize
    """

    board.place(board.length//2-1, board.length//2-1, reversi.Piece('white'))
    board.place(board.length//2, board.length//2, reversi.Piece('white'))
    board.place(board.length//2, board.length//2-1, reversi.Piece('black'))
    board.place(board.length//2-1, board.length//2, reversi.Piece('black'))


def count_pieces(board):
    """Counts number of black and white pieces on the board
    
    Arguments:
        board {Board} -- board to check
    
    Raises:
        ValueError -- If the function finds a color that isn't white or black
    
    Returns:
        tuple -- (black count, white count)
    """

    black_count = 0
    white_count = 0
    for row in range(board.length):
        for slot in range(board.length):
            if not board.is_free(row, slot):
                piece = board.get(row, slot)
                if piece.color() == "black":
                    black_count += 1
                elif piece.color() == "white":
                    white_count += 1
                else:
                    raise ValueError("Got a color that wasn't white or black")
    return (black_count, white_count)


def get_all_streaks(board, row, col, piece_arg):
    """Gets streaks in all directions for a player on a slot

    Arguments:
        board {Board} -- board to check
        row {int} -- row of reference point for streaks
        col {int} -- column of reference point for streaks
        piece_arg {Piece} -- piece of player to check for streaks of

    Returns:
        dict -- key = direction, value = positions of pieces in streak
    """

    streaks = {'e': None, 'w': None, 'n': None, 's': None, \
               'ne': None, 'nw': None, 'se': None, 'sw': None}

    color = piece_arg.color()
    other_color = 'white' if color == 'black' else 'black'

    # north
    L = []
    c = col
    for r in range(row-1, -1, -1):
        if not board.is_free(r, c):
            piece = board.get(r, c)
            if piece.color() == other_color:
                L.append((r, c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
    else:
        L = [] # streak not terminated with color piece
    streaks['n'] = sorted(L)

    # east
    L = []
    c = col
    r = row
    for c in range(col+1, board.length):
        if not board.is_free(r, c):
            piece = board.get(r, c)
            if piece.color() == other_color:
                L.append((r, c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
    else:
        L = [] # streak not terminated with color piece
    streaks['e'] = sorted(L)

    # south
    L = []
    c = col
    r = row
    for r in range(row+1, board.length):
        if not board.is_free(r, c):
            piece = board.get(r, c)
            if piece.color() == other_color:
                L.append((r, c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
    else:
        L = [] # streak not terminated with color piece
    streaks['s'] = sorted(L)

    # west
    L = []
    c = col
    r = row
    for c in range(col-1, -1, -1):
        if not board.is_free(r, c):
            piece = board.get(r, c)
            if piece.color() == other_color:
                L.append((r, c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
    else:
        L = [] # streak not terminated with color piece
    streaks['w'] = sorted(L)

    # northeast
    L = []
    c = col
    r = row
    c = col+1
    for r in range(row-1, -1, -1):
        if c == board.length:
            L = []  # terminated without finding color
            break
        if not board.is_free(r, c):
            piece = board.get(r, c)
            if piece.color() == other_color:
                L.append((r, c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
        c += 1
    else:
        L = [] # streak not terminated with color piece
    streaks['ne'] = sorted(L)

    # southeast
    L = []
    c = col
    r = row
    c = col+1
    for r in range(row+1, board.length):
        if c == board.length:
            L = []  # terminated without finding color
            break
        if not board.is_free(r, c):
            piece = board.get(r, c)
            if piece.color() == other_color:
                L.append((r, c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
        c += 1
    else:
        L = [] # streak not terminated with color piece
    streaks['se'] = sorted(L)

    # southwest
    L = []
    c = col
    r = row
    c = col - 1
    for r in range(row+1, board.length):
        if c == -1:
            L = []  # terminated without finding color
            break
        if not board.is_free(r, c):
            piece = board.get(r, c)
            if piece.color() == other_color:
                L.append((r, c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
        c = c - 1
    else:
        L = [] # streak not terminated with color piece
    streaks['sw'] = sorted(L)

    # northwest
    L = []
    c = col
    r = row
    c = col - 1
    for r in range(row-1, -1, -1):
        if c == -1:
            L = []  # terminated without finding color
            break
        if not board.is_free(r, c):
            piece = board.get(r, c)
            if piece.color() == other_color:
                L.append((r, c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
        c = c - 1
    else:
        L = [] # streak not terminated with color piece
    streaks['nw'] = sorted(L)

    return streaks


def get_all_capturing_cells(board, piece):
    """Gets all cells that will result in a capture and those captures

    Arguments:
        board {Board} -- board to use
        piece {Piece} -- piece to use

    Returns:
        dict -- {(row, col): [cells that will be captured]}
    """

    capturing_dict = {}
    for row in range(board.length):
        for slot in range(board.length):
            if board.is_free(row, slot):
                capturing_cells = []
                streaks = get_all_streaks(board, row, slot, piece)
                for value in streaks.values():
                    capturing_cells.extend(value)
                capturing_dict[(row, slot)] = sorted(capturing_cells)
        # Remove empty values
        ret_dict = {k: v for k, v in capturing_dict.items() if v != []}
    return ret_dict


def get_hint(board, piece):
    """Gets all possible moves that will result in a capture, sorted

    Arguments:
        board {Board} -- board to use
        piece {Piece} -- player piece to base search on

    Returns:
        list -- List of possible moves sorted by number of
    """


    capturing_cells = get_all_capturing_cells(board, piece)
    cells = []
    for k, v in capturing_cells.items():
        cells.append((deindexify(*k), len(v)))
    cells.sort(key=itemgetter(1, 0), reverse=True)
    return [cell[0] for cell in cells]


def place_and_flip(board, row, col, piece):
    """The main handler for a game move, with error checking

    Arguments:
        board {Board} -- board to modify for the move
        row {int} -- Row of the original move
        col {int} -- Column of the original move
        piece {Piece} -- A piece that matches the current player

    Raises:
        ValueError -- If move is outside of the board
        ValueError -- If move is not a capture
        ValueError -- If the space is already occupied
    """

    if row + 1 > board.length or col + 1 > board.length:
        raise ValueError("Can't place {:s} at '{:s}',".format(
                str(piece), deindexify(row, col)) +
                " invalid position. Type 'hint' to get suggestions.")
    if not board.is_free(row, col):
        raise ValueError("Can't place {:s} at '{:s}',".format(
            str(piece), deindexify(row, col)) +
            " already occupied. Type 'hint' to get suggestions.")
    # Flip pieces in streaks
    captures = []
    for direction, piece_list in get_all_streaks(board, row, col, piece).items():
        if piece_list:
            captures.extend(piece_list)
    if captures:
        board.place(row, col, piece)
        for slot in captures:
            board.get(*slot).flip()
    else:
        raise ValueError("Can't place {:s} at '{:s}',".format(
            str(piece), deindexify(row, col)) +
            " it's not a capture. Type 'hint' to get suggestions.")


def is_game_finished(board):
    """Checks whether the game is finished

    Arguments:
        board {Board} -- board to check in current state

    Returns:
        bool -- True if game finished, False if not
    """

    b_poss_moves = len(get_hint(board, reversi.Piece('black')))
    w_poss_moves = len(get_hint(board, reversi.Piece('white')))

    if b_poss_moves == 0 and w_poss_moves == 0 or board.is_full():
        return True

    return False


def get_winner(board):
    """Gets the winner by returning player with the most pieces on the board

    Arguments:
        board {Board} -- board to check in current state

    Returns:
        str -- "white" or "black"
    """

    count = count_pieces(board)
    b = count[0]
    w = count[1]

    if b > w:
        return 'black'
    elif w > b:
        return 'white'

    return 'draw'


def choose_color():
    """Prompts the user to choose a color with error checking

    Returns:
        tuple -- format (your color, opponent color)
    """

    COLOR_INPUT = "Pick a color: "
    ACCEPTABLE_COLORS = ['white', 'black']
    color = ""
    color = input(COLOR_INPUT)
    while color not in ACCEPTABLE_COLORS:
        print("Wrong color, type only 'black' or 'white', try again.")
        color = input(COLOR_INPUT)
    my_color = color
    opponent_color = 'white' if my_color == 'black' else 'black'
    print("You are '{}' and your opponent is '{}'.".format(my_color, opponent_color))
    return (my_color, opponent_color)


def game_play_human():
    """
    This is the main mechanism of the human vs. human game play.
    """

    banner = """
     _____                         _ 
    |  __ \                       (_)
    | |__) |_____   _____ _ __ ___ _ 
    |  _  // _ \ \ / / _ \ '__/ __| |
    | | \ \  __/\ V /  __/ |  \__ \ |
    |_|  \_\___| \_/ \___|_|  |___/_|
    
    Developed by The Students Inc.
    CSE231 Spring Semester 2018
    Michigan State University
    East Lansing, MI 48824, USA.
    """

    prompt = "[{:s}'s turn] :> "
    print(banner)

    # Choose the color here
    (my_color, opponent_color) = choose_color()

    # Take a board of size 8x8
    # Prompt for board size
    size = input("Input a board size: ")
    board = reversi.Board(int(size))
    initialize(board)

    # Decide on whose turn, use a variable called 'turn'.
    turn = my_color if my_color == 'white' else opponent_color

    # loop until the game is finished
    while not is_game_finished(board):
        try:
            # Count the pieces and assign into piece_count
            piece_count = count_pieces(board)

            print("Current board:")
            board.display(piece_count)

            # Get a piece according to turn
            piece = reversi.Piece(turn)

            # Get the command from user using input
            command = input(prompt.format(turn)).lower()

            # Now decide on different commands
            if command == 'exit':
                break
            elif command == 'hint':
                print("\tHint: " + ", ".join(get_hint(board, piece)))
            elif command == 'pass':
                hint = get_hint(board, piece)
                if not hint:
                    turn = my_color if turn == opponent_color \
                                        else opponent_color
                    print("\tHanded over to \'{:s}\'.".format(turn))
                else:
                    print("\tCan't hand over to opponent, you have moves," + \
                          " type 'hint'.")
            else:
                (row, col) = indexify(command)
                place_and_flip(board, row, col, piece)
                print("\t{:s} played {:s}.".format(turn, command))
                turn = my_color if turn == opponent_color else opponent_color
        except ValueError as err:
            print("Error:", err)

    # The loop is over.
    piece_count = count_pieces(board)
    print("Current board:")
    board.display(piece_count)
    winner = get_winner(board)
    if winner != 'draw':
        diff = abs(piece_count[0] - piece_count[1])
        print("\'{:s}\' wins by {:d}! yay!!".format(winner, diff))
    else:
        print("This game ends in a draw.")
    # --- end of game play ---


def figure_1(board):
    """
    You can use this function to test your program
    """
    board.place(0, 0, reversi.Piece('black'))
    board.place(0, 3, reversi.Piece('black'))
    board.place(0, 4, reversi.Piece('white'))
    board.place(0, 5, reversi.Piece('white'))
    board.place(0, 6, reversi.Piece('white'))
    board.place(1, 1, reversi.Piece('white'))
    board.place(1, 3, reversi.Piece('white'))
    board.place(1, 5, reversi.Piece('white'))
    board.place(1, 6, reversi.Piece('white'))
    board.place(1, 7, reversi.Piece('white'))
    board.place(2, 2, reversi.Piece('white'))
    board.place(2, 3, reversi.Piece('black'))
    board.place(2, 4, reversi.Piece('white'))
    board.place(2, 5, reversi.Piece('white'))
    board.place(2, 7, reversi.Piece('white'))
    board.place(3, 0, reversi.Piece('black'))
    board.place(3, 1, reversi.Piece('white'))
    board.place(3, 2, reversi.Piece('white'))
    board.place(3, 4, reversi.Piece('white'))
    board.place(3, 5, reversi.Piece('white'))
    board.place(3, 6, reversi.Piece('black'))
    board.place(3, 7, reversi.Piece('black'))
    board.place(4, 0, reversi.Piece('white'))
    board.place(4, 2, reversi.Piece('white'))
    board.place(4, 4, reversi.Piece('white'))
    board.place(5, 0, reversi.Piece('black'))
    board.place(5, 2, reversi.Piece('black'))
    board.place(5, 3, reversi.Piece('white'))
    board.place(5, 5, reversi.Piece('black'))
    board.place(6, 0, reversi.Piece('black'))
    board.place(6, 1, reversi.Piece('black'))
    board.place(6, 3, reversi.Piece('white'))
    board.place(6, 6, reversi.Piece('white'))
    board.place(7, 1, reversi.Piece('black'))
    board.place(7, 2, reversi.Piece('white'))
    board.place(7, 3, reversi.Piece('black'))
    board.place(7, 7, reversi.Piece('black'))


if __name__ == "__main__":
    game_play_human()
