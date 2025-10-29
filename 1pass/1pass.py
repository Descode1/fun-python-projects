import random

NUMS = "0123456789"
LOWER = "abcdefghijklmnopqrstuvwxyz"
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SYMBOLS = "~!@#$%^&*()_-+=}{:;><.,/?"

CHAR_SETS = [NUMS, LOWER, UPPER, SYMBOLS]

def get_password():
    password = ""
    for _ in range(18):
        char_set = random.choice(CHAR_SETS)
        password += random.choice(char_set)
    return password

print(get_password())





