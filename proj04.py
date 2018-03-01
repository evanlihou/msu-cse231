"""
CSE 231 Project 04

Asks user if they want to encrypt, decrypt, or quit until they want to quit
    Encrypt:
        Recursively encrypts each letter with Affine and punctuation with
        Caesar cipher
    Decrypt:
        Recursively do the opposite math on each letter and punctuation using
        Affine and Caesar ciphers
    Quit:
        Terminates the program
"""

import math
import string

# Alphabet strings
PUNCTUATION = string.punctuation
ALPHA_NUM = string.ascii_lowercase + string.digits

# Input strings
JOB_INPUT = "Input a command (e)ncrypt, (d)ecrypt, (q)uit: "
ENCRYPT_INPUT = "Input a string to encrypt: "
DECRYPT_INPUT = "Input a string to decrypt: "
ROTATION_INPUT = "Input a rotation (int): "

# Error Strings
WRONG_ROTATION = "Error; rotation must be an integer."
INVALID_CHAR = "Error with character: {}\nCannot encrypt this string."


def multiplicative_inverse(A, M):
    '''
    Return the multiplicative inverse for A given M.
    Find it by trying possibilities until one is found.
    '''
    for x in range(M):
        if (A * x) % M == 1:
            return x


def check_co_prime(num, M):
    '''
    Check whether a number is a co-prime
    num (int) = number to check
    M (int) = length of the alphabet
    Returns: boolean
    '''
    return math.gcd(num, M) == 1


def get_smallest_co_prime(M):
    '''
    Recursively check coprimes from 2 to M until the first one is found.
    M (int) = length of the alphabet
    Returns: int
    '''
    for x in range(2, M+1):
        if check_co_prime(x, M):
            return x


def caesar_cipher_encryption(ch, N, alphabet):
    '''
    Encrypt ch using a caesar cipher.
    ch (str) = character to encrypt
    N (int) = rotation
    alphabet (str) = alphabet to use in encryption
    Returns: str
    '''
    old_index = alphabet.find(ch)
    new_index = (old_index+N) % len(alphabet)
    return alphabet[new_index]


def caesar_cipher_decryption(ch, N, alphabet):
    '''
    Decrypt ch using a caesar cipher.
    ch (str) = character to encrypt
    N (int) = rotation
    alphabet (str) = alphabet to use in encryption
    Returns: str
    '''
    old_index = alphabet.find(ch)
    new_index = (old_index-N) % len(alphabet)
    return alphabet[new_index]


def affine_cipher_encryption(ch, N, alphabet):
    '''
    Encrypt ch using an affine cipher.
    ch (str) = character to encrypt
    N (int) = rotation
    alphabet (str) = alphabet to use in encryption
    Returns: str
    '''
    A = get_smallest_co_prime(len(alphabet))
    old_index = alphabet.find(ch)
    new_index = ((A * old_index) + N) % len(alphabet)
    return alphabet[new_index]


def affine_cipher_decryption(ch, N, alphabet):
    '''
    Decrypt ch using an affine cipher.
    ch (str) = character to encrypt
    N (int) = rotation
    alphabet (str) = alphabet to use in encryption
    Returns: str
    '''
    A = get_smallest_co_prime(len(alphabet))
    A_inverse = multiplicative_inverse(A, len(alphabet))
    old_index = alphabet.find(ch)
    new_index = A_inverse*(old_index-N) % len(alphabet)
    return alphabet[new_index]


def main():
    '''
    The main section of the program which processes input and calls other
    necessary functions.
    '''
    while True:
        N = input(ROTATION_INPUT)
        if N.isdigit():
            N = int(N)
            break
        else:
            print(WRONG_ROTATION)
    job = input(JOB_INPUT)
    while True:
        if job.lower() == "e":
            to_encrypt = input(ENCRYPT_INPUT)
            encrypted = ""
            for ch in to_encrypt:
                ch = ch.lower()
                if ch in PUNCTUATION:
                    encrypted += caesar_cipher_encryption(ch, N, PUNCTUATION)
                elif ch in ALPHA_NUM:
                    encrypted += affine_cipher_encryption(ch, N, ALPHA_NUM)
                else:
                    print(INVALID_CHAR.format(ch))
                    break
            else:
                print("Plain text: " + to_encrypt)
                print("Cipher text: " + encrypted)
        elif job.lower() == "d":
            to_decrypt = input(DECRYPT_INPUT)
            decrypted = ""
            for ch in to_decrypt:
                ch = ch.lower()
                if ch in PUNCTUATION:
                    decrypted += caesar_cipher_decryption(ch, N, PUNCTUATION)
                elif ch in ALPHA_NUM:
                    decrypted += affine_cipher_decryption(ch, N, ALPHA_NUM)
                else:
                    print(INVALID_CHAR.format(ch))
                    break
            else:
                print("Cipher text: " + to_decrypt)
                print("Plain text: " + decrypted)

        elif job.lower() == "q":
            break
        else:
            print("Error; Invalid command")
        job = input(JOB_INPUT)


if __name__ == "__main__":
    main()
