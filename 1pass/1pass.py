import random
import json
import cryptography


def get_password():
    NUMS = "0123456789"
    LOWER = "abcdefghijklmnopqrstuvwxyz"
    UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    SYMBOLS = "~!@#$%^&*()_-+=}{:;><.,/?"
    CHAR_SETS = [NUMS, LOWER, UPPER, SYMBOLS]

    password = ""
    for _ in range(18):
        char_set = random.choice(CHAR_SETS)
        password += random.choice(char_set)
    return password
password = get_password()
passwords = {}
passwords['github'] = password
a = json.dumps(passwords)
print(a)






