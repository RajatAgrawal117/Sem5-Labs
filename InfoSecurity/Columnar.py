import math

# Function to encrypt the plain text using columnar transposition cipher


def encrypt_columnar(plain_text, key):
    # Determine the number of rows required to fit the plain text into the matrix
    num_rows = math.ceil(len(plain_text) / len(key))

    # Initialize the matrix with empty spaces (size: num_rows x len(key))
    matrix = [[' ' for _ in range(len(key))] for _ in range(num_rows)]

    # Fill the matrix with the plain text characters, row by row
    k = 0  # Index to track the current character in the plain text
    for i in range(num_rows):
        for j in range(len(key)):
            if k < len(plain_text):  # Ensure we don't go out of bounds of plain text
                # Assign the character to the matrix
                matrix[i][j] = plain_text[k]
                k += 1  # Move to the next character in the plain text

    # Sort the columns based on the key's character positions
    sorted_key = sorted(range(len(key)), key=lambda x: key[x])
    result = ''

    # Read the matrix column by column in the sorted order to generate the cipher text
    for col in sorted_key:
        for row in range(num_rows):
            # Concatenate characters to form the cipher text
            result += matrix[row][col]

    return result  # Return the encrypted text

# Function to decrypt the cipher text using columnar transposition cipher


def decrypt_columnar(cipher_text, key):
    # Calculate the number of rows in the matrix
    num_rows = len(cipher_text) // len(key)

    # Calculate if there are any extra characters to handle uneven columns
    extra_chars = len(cipher_text) % len(key)

    # Initialize the matrix with empty spaces (extra row to handle extra characters)
    matrix = [[' ' for _ in range(len(key))] for _ in range(num_rows + 1)]

    # Sort the key to determine the column reading order
    sorted_key = sorted(range(len(key)), key=lambda x: key[x])

    # Fill the matrix column by column based on the sorted key
    k = 0  # Index to track the current character in the cipher text
    for col in sorted_key:
        # Extra row for columns with extra characters
        for row in range(num_rows + (col < extra_chars)):
            # Assign the character to the matrix
            matrix[row][col] = cipher_text[k]
            k += 1  # Move to the next character in the cipher text

    # Read the matrix row by row to reconstruct the plain text
    plaintext = ''
    for row in range(num_rows + 1):
        for col in range(len(key)):
            if matrix[row][col] != ' ':  # Skip empty spaces
                # Concatenate characters to form the plain text
                plaintext += matrix[row][col]

    # Output the decrypted plain text
    print("Decrypted text:", plaintext)


# Input from the user
plain_text = input("Enter the plain text: ")
key = input("Enter the key: ")

# Encrypt the plain text and print the cipher text
cipher_text = encrypt_columnar(plain_text, key)
print("Encrypted text:", cipher_text)

# Decrypt the cipher text and print the original plain text
decrypt_columnar(cipher_text, key)
