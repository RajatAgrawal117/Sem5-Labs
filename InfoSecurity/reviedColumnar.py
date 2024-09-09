import math

# Function to display the matrix (for debugging purposes)
def show_matrix(matrix):
    for row in matrix:
        print(' '.join(row))
    print()

# Function to encrypt using modified diagonal columnar cipher
def encrypt_diagonal_columnar(plain_text, key):
    n = len(key)
    m = len(plain_text)
    
    # Initialize the matrix with empty characters
    matrix = [['_' for _ in range(n)] for _ in range(n)]
    
    # Fill the matrix diagonally
    k = 0
    for d in range(2 * n - 1):  # Diagonal loops
        for i in range(n):
            j = d - i
            if 0 <= j < n and k < m:
                matrix[i][j] = plain_text[k]
                k += 1

    # Show matrix after diagonal filling (for debugging)
    print("Matrix after diagonal filling (Encryption):")
    show_matrix(matrix)

    # Sort the key and generate the ciphertext by reading columns in sorted order
    sorted_key = sorted(range(len(key)), key=lambda x: key[x])
    ciphertext = ''
    
    for col in sorted_key:
        for row in range(n):
            if matrix[row][col] != '_':
                ciphertext += matrix[row][col]
    
    return ciphertext

# Function to decrypt using modified diagonal columnar cipher
def decrypt_diagonal_columnar(cipher_text, key):
    n = len(key)
    m = len(cipher_text)
    
    # Initialize the matrix with empty characters
    matrix = [['_' for _ in range(n)] for _ in range(n)]
    
    # Sort the key to determine the order of columns to fill
    sorted_key = sorted(range(len(key)), key=lambda x: key[x])
    
    # Fill the matrix column-wise based on the sorted key
    k = 0
    for col in sorted_key:
        for row in range(n):
            if k < m and matrix[row][col] == '_':
                matrix[row][col] = cipher_text[k]
                k += 1

    # Show matrix after column-wise filling (for debugging)
    print("Matrix after column-wise filling (Decryption):")
    show_matrix(matrix)

    # Read the matrix diagonally to reconstruct the original plaintext
    plaintext = ''
    for d in range(2 * n - 1):
        for i in range(n):
            j = d - i
            if 0 <= j < n and matrix[i][j] != '_':
                plaintext += matrix[i][j]
    
    return plaintext


# Input from the user
plain_text = input("Enter plaintext: ")
key = input("Enter key: ")

# Encrypt the plaintext and display the encrypted text
encrypted_text = encrypt_diagonal_columnar(plain_text, key)
print("Encrypted Text:", encrypted_text)

# Decrypt the ciphertext and display the decrypted text
decrypted_text = decrypt_diagonal_columnar(encrypted_text, key)
print("Decrypted Text:", decrypted_text)
