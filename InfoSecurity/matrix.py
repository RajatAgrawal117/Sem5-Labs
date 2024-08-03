import random
import math
# to generate random value of 3 alphabets


def random_Alphabet():

    return random.randint(1, 13), random.randint(2, 10), random.randint(1, 10)
# to make math function as of ax^2+bx+c


def math_function_shift(index, a, t, e):

    return (a * index**2 + t * index + e) % 26
# encryption function


def revised_encrypt(text, key):

    a, t, e = random_Alphabet()
    encrypted_text = ''
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    index = 0
    for char in text.upper():
        if char in letters:
            shift = (math_function_shift(index, a, t, e) + key) % 26
            new_index = (letters.index(char) + shift) % 26
            encrypted_text += letters[new_index]
            index += 1
        else:
            encrypted_text += char
    return encrypted_text, a, t, e
# decryption function


def revised_decrypt(encrypted_text, a, t, e, key):

    decrypted_text = ''
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    index = 0
    for char in encrypted_text.upper():
        if char in letters:
            shift = (math_function_shift(index, a, t, e) + key) % 26
            new_index = (letters.index(char) - shift) % 26
            decrypted_text += letters[new_index]
            index += 1
        else:
            decrypted_text += char
    return decrypted_text


# User Input
plaintext = input("Enter the text you want to encrypt: ")
key = int(input("Enter the value of the shift: "))
# encryption
encrypted_text, a, t, e = revised_encrypt(plaintext, key)
print("Encrypted: " + encrypted_text + ", a=" +
      str(a) + ", t=" + str(t) + ", e=" + str(e))
# Decryption
decrypted_text = revised_decrypt(encrypted_text, a, t, e, key)
print("Decrypted: " + decrypted_text)
