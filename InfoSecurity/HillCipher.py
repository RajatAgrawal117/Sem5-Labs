import numpy as np
import math

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
    return None

def matrix_mod_inverse(matrix, mod):
    det = int(np.round(np.linalg.det(matrix)))  # Compute determinant
    gcd_det_mod = math.gcd(det, mod)  # Check gcd of determinant and mod

    if gcd_det_mod != 1:  # If gcd(det, 26) != 1, the matrix is not invertible
        raise ValueError(
            f"Key matrix is not invertible in mod {mod}. GCD is {gcd_det_mod}.")

    det_inv = mod_inverse(det, mod)  # Compute determinant inverse mod 26

    # Modular inverse matrix
    matrix_inv = det_inv * \
        np.round(det * np.linalg.inv(matrix)).astype(int) % mod
    return matrix_inv % mod

def encrypt(message, key, n):
    message_vector = []
    for i in range(n):
        message_vector.append(ord(message[i]) % 65)
    message_vector = np.array(message_vector).reshape(n, 1)

    key_matrix = create_key_matrix(key, n)

    cipher_matrix = np.dot(key_matrix, message_vector) % 26

    cipher_text = []
    for i in range(n):
        cipher_text.append(chr(cipher_matrix[i][0] + 65))

    return "".join(cipher_text)

def decrypt(ciphertext, key, n):
    cipher_vector = []
    for i in range(n):
        cipher_vector.append(ord(ciphertext[i]) % 65)
    cipher_vector = np.array(cipher_vector).reshape(n, 1)

    key_matrix = create_key_matrix(key, n)

    # Get inverse key matrix in mod 26
    key_matrix_inv = matrix_mod_inverse(key_matrix, 26)

    message_matrix = np.dot(key_matrix_inv, cipher_vector) % 26

    message_text = []
    for i in range(n):
        message_text.append(chr(int(message_matrix[i][0]) + 65))

    return "".join(message_text)

def hill_cipher_encrypt(message, key):
    n = int(len(key) ** 0.5)

    if len(message) % n != 0:
        while len(message) % n != 0:
            message += "X"  # Padding with 'X' to fit the key matrix size

    # Check if the key matrix is invertible before encryption
    key_matrix = create_key_matrix(key, n)
    try:
        matrix_mod_inverse(key_matrix, 26)  # This checks invertibility
    except ValueError as e:
        print(e)
        return ""

    cipher_text = ""
    for i in range(0, len(message), n):
        cipher_text += encrypt(message[i:i + n], key, n)

    return cipher_text

def hill_cipher_decrypt(cipher_text, key):
    n = int(len(key) ** 0.5)

    decrypted_text = ""
    for i in range(0, len(cipher_text), n):
        decrypted_text += decrypt(cipher_text[i:i + n], key, n)

    return decrypted_text

if __name__ == "__main__":
    message = input("Enter the plaintext: ").upper().replace(" ", "")
    key = input("Enter the key: ").upper().replace(" ", "")

    cipher_text = hill_cipher_encrypt(message, key)
    if cipher_text:
        print(f"Cipher Text: {cipher_text}")

        decrypted_text = hill_cipher_decrypt(cipher_text, key)
        print(f"Decrypted Text: {decrypted_text}")
