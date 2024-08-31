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

def matrix_mod_inverse(matrix, mod):
    det = int(np.round(np.linalg.det(matrix)))  # Compute determinant
    det_inv = mod_inverse(det, mod)  # Compute determinant inverse mod 26

    if det_inv is None:
        raise ValueError("Matrix is not invertible in mod 26.")

    # Modular inverse matrix
    matrix_inv = det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % mod
    return matrix_inv % mod

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

def decrypt(ciphertext, key, n):
    cipher_vector = []
    for i in range(n):
        cipher_vector.append(ord(ciphertext[i]) % 65)
    cipher_vector = np.array(cipher_vector).reshape(n, 1)

    key_matrix = create_key_matrix(key, n)

    # Calculate the determinant of the key matrix
    determinant = calculate_determinant(key_matrix)

    # Subtract the determinant from the cipher vector
    adjusted_cipher_vector = (cipher_vector - determinant) % 26

    # Calculate the inverse of the key matrix
    key_matrix_inv = matrix_mod_inverse(key_matrix, 26)

    # Decrypt by multiplying the inverse key matrix with the adjusted cipher vector
    message_matrix = np.dot(key_matrix_inv, adjusted_cipher_vector) % 26

    message_text = []
    for i in range(n):
        message_text.append(chr(int(message_matrix[i][0]) + 65))

    return "".join(message_text)

def hill_cipher_encrypt(message, key):
    n = int(len(key) ** 0.5)

    if len(message) % n != 0:
        while len(message) % n != 0:
            message += "X"  # Padding with 'X' to fit the key matrix size

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
    print(f"Cipher Text: {cipher_text}")

    decrypted_text = hill_cipher_decrypt(cipher_text, key)
    print(f"Decrypted Text: {decrypted_text}")
