import numpy as np


def create_key_matrix(key, n):
    key_matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(ord(key[i * n + j]) % 65)
        key_matrix.append(row)
    return np.array(key_matrix)

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return 1

def calculate_determinant(matrix):
    det = int(np.round(np.linalg.det(matrix)))
    return det % 26  # Determinant modulo 26


def encrypt(message, key, n):
    message_vector = []
    for i in range(n):
        message_vector.append(ord(message[i]) % 65)
    message_vector = np.array(message_vector).reshape(n, 1)

    key_matrix = create_key_matrix(key, n)

    # Calculate the determinant of the key matrix
    determinant = calculate_determinant(key_matrix)

    # Multiply the key matrix with the message vector
    cipher_matrix = np.dot(key_matrix, message_vector)

    # Add the determinant to each value in the cipher matrix
    cipher_matrix = (cipher_matrix + determinant) % 26

    cipher_text = []
    for i in range(n):
        cipher_text.append(chr(cipher_matrix[i][0] + 65))

    return "".join(cipher_text)


def hill_cipher(message, key):
    n = int(len(key) ** 0.5)

    if len(message) % n != 0:
        while len(message) % n != 0:
            message += "X"  # Padding with 'X' to fit the key matrix size

    cipher_text = ""
    for i in range(0, len(message), n):
        cipher_text += encrypt(message[i:i + n], key, n)

    return cipher_text


if __name__ == "__main__":
    message = input("Enter the plaintext: ").upper().replace(" ", "")
    key = input("Enter the key: ").upper().replace(" ", "")

    cipher_text = hill_cipher(message, key)
    print(f"Cipher Text: {cipher_text}")
