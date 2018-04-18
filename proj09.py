"""Proj 09
Asks the user which attack they would like to perform
    If chosen plaintext
        Get relevant information from user
        Return the decrypted string
    If Ngram
        Get relevant information from the user
        Check all possible shifts and perform fitness tests
        Return the most likely solution
"""

from math import log10
import string
from operator import itemgetter

# Constants
FILE_INPUT = "Input a file name: "
FILE_ERROR = "Unable to open the file. Please try again."
WAIT_PROMPT = "\npress any key to continue..."
BANNER = """\
------------------------------------------------------------------------
Welcome to the world of code breaking. This program is meant to help
decipher encrypted ciphertext in absence of knowledge of algorithm/key.
------------------------------------------------------------------------
"""
MENU = """\
1. Chosen plaintext attack
2. Ngram frequency analysis
"""


def open_file():
    """Opens a file with error checking

    Returns:
        file pointer
    """
    file_entered = False
    while not file_entered:
        try:
            file_name = input(FILE_INPUT)
            data_file = open(file_name)
            return data_file
        except FileNotFoundError:
            print(FILE_ERROR)


def log_probability_dictionary(fp):
    """Creates a dictionary of quadgrams and their probabilities

    Arguments:
        fp {file pointer} -- file to read with quadgram and occurances

    Returns:
        dict -- Quadgram dictionary with key of quadgram and value of
            [frequency, log probability]
    """

    quadgram_dictionary = {}
    lines_list = fp.readlines()

    # Calculate total for all quadgrams
    total_quadgrams = 0
    for line in lines_list:
        freq = int(line.split()[1])
        total_quadgrams += freq

    # Build the dictionary
    for line in lines_list:
        line_list = line.split()  # Separate key from value
        quad = line_list[0]
        freq = int(line_list[1])
        probability = log10(freq/total_quadgrams)
        quadgram_dictionary[quad] = [freq, probability]

    # Create a sorted list of quadgrams
    quadgram_list = []
    for quadgram, value in quadgram_dictionary.items():
        quadgram_list.append([quadgram, *value])  # Spread values out
    sorted_quadgrams = sorted(quadgram_list, key=itemgetter(1), reverse=True)

    # Print that list
    print("\n{:<8s}{:>13s}{:>22s}".format(
        'Quadgram', 'Count', 'Log Probability'
        ))
    print("-"*43)
    for quad in sorted_quadgrams[:10]:
        print("{:<8s}{:>13d}{:>22f}".format(
            *quad  # Spread out quadgram data for all 3 format args
        ))
    return quadgram_dictionary


def fitness_calculator(potential_plaintext, quadgram_dictionary):
    """Calculates fitness of a plaintext string based on quadgrams

    Arguments:
        potential_plaintext {str} -- text to check against
        quadgram_dictionary {dict} -- A dict of quadgrams to use as data

    Raises:
        ValueError -- If potential_plaintext is less than 4 characters

    Returns:
        float -- Sum of log probabilities for the whole potential_plaintext
    """

    debug = False  # Enable this to view extra debugging output
    word_length = len(potential_plaintext)
    probability_sum = 0
    if word_length < 4:
        raise ValueError
    for i in range(word_length-4+1):
        if debug:
            print(" "*i+"[{}]".format(potential_plaintext[i:i+4]))
        try:
            quadgram = potential_plaintext[i:i+4]
            log_prob = quadgram_dictionary[quadgram][1]
            probability_sum += log_prob
        except KeyError:
            if debug:
                print("Quadgram not found: " + quadgram)
            continue
    return probability_sum


def chosen_plaintext_attack(plaintext, ciphertext, bifurcation, texttodecrypt):
    """Runs a chosen plaintext attack

    Arguments:
        plaintext {str} -- Plaintext to use in cipher
        ciphertext {str} -- Ciphertext that goes with plaintext
        bifurcation {int} -- Num of characters in ciphertext that equal 1
            plaintext character
        texttodecrypt {str} -- Text to decrypt using plaintext and ciphertext

    Returns:
        str -- The decrypted text
    """

    debug = False  # Enable this to view extra debugging output

    decryption_dict = {}
    for i, ch in enumerate(plaintext):
        cipher_start = i*bifurcation
        cipher_end = cipher_start + bifurcation
        if debug:
            print("Cipher fragment: " + ciphertext[cipher_start:cipher_end])
        decryption_dict[ciphertext[cipher_start:cipher_end]] = ch

    # Split texttodecrypt into fragments that match keys in decryption_dict
    split_text = []
    for i in range(0, len(texttodecrypt), bifurcation):
        if debug:
            print("Text to decrypt fragment: " + texttodecrypt[i:i+bifurcation])
        split_text.append(texttodecrypt[i:i+bifurcation])

    ret_str = ""
    for item in split_text:
        try:
            ret_str += decryption_dict[item]
        except KeyError:
            print("Decryption interrupted. Key not found:  {}".format(item))
            return None

    print("Decrypted text: \t" + ret_str)
    return ret_str


def bruteforce_shift_cipher(ciphertext, ngrams_dictionary):
    """Checks a ciphertext against all possible shifts and uses quadgrams to
            determine the best fitting solution

    Arguments:
        ciphertext {str} -- Text to decrypt
        ngrams_dictionary {dict} -- Dictionary containing quadgrams and
            probabilities

    Assumes:
        ciphertext consists of only uppercase characters, with no space or
            punctuation
    """

    fitness_list = []
    alphabet = string.ascii_uppercase

    # Try all possible shifts
    for key in range(len(alphabet)):
        plaintext = ""
        for ch in ciphertext:
            index = alphabet.find(ch)
            plaintext += alphabet[(index + key) % 26]
        fitness = fitness_calculator(plaintext, ngrams_dictionary)
        fitness_list.append((key, plaintext, fitness))

    fitness_list.sort(key=itemgetter(2), reverse=True)  # Sort by fitness

    print("{:<5s}{:^35s}   {:>10s}".format("\nKey", "Plaintext", "Fitness"))
    print("-"*54)
    for potential_solution in fitness_list[:5]:
        print("{:<5d}{:^.35s}   {:>10.4f}".format(*potential_solution))

    solution = fitness_list[0]
    input(WAIT_PROMPT)
    print("\nDecrypted ciphertext: {}".format(solution[1]))


def main():
    """The main functionality of the program, which calls other functions
    """
    print(BANNER)
    print(MENU)
    menu_choice = None
    while menu_choice not in ["1", "2", "q"]:
        menu_choice = input("Choice: ")
        menu_choice = menu_choice.lower()
        # Chosen plaintext attack
        if menu_choice == "1":
            plaintext = input("Plaintext: ")
            ciphertext = input("Ciphertext: ")
            bifurcation = int(input("Bifurcation: "))
            decrypt = input("Text to decrypt: ")
            chosen_plaintext_attack(plaintext, ciphertext, bifurcation, decrypt)

        # Ngram frequency analysis
        elif menu_choice == "2":
            file = open_file()
            D = log_probability_dictionary(file)
            ciphertext = input("Ciphertext: ")
            uc_ciphertext = ciphertext.upper()
            normalized_cipher = ""
            for ch in uc_ciphertext:
                if ch in string.ascii_uppercase:
                    normalized_cipher += ch
            bruteforce_shift_cipher(normalized_cipher, D)

        elif menu_choice == "q":
            pass

        else:
            print("Invalid input.")


if __name__ == "__main__":
    main()
