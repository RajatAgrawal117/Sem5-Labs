def encrypt_gronsfeld(plaintext, key):
    # Convert key to list of integers for easier manipulation
    key = [int(k) for k in str(key)]

    # Find the smallest letter in the plaintext to use as a filler
    filler = min(plaintext)

    # Repeat the plaintext and key to ensure they match in length
    plaintext += filler * (len(key) - len(plaintext))
    key = (key * ((len(plaintext) // len(key)) + 1))[:len(plaintext)]

    # Encrypt each character in plaintext
    ciphertext = ""
    for i, char in enumerate(plaintext):
        shift = key[i]
        # Calculate the shifted character
        encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        ciphertext += encrypted_char

    return ciphertext


# Input from user
plaintext = input("Enter plaintext (capital letters only): ").upper()
key = input("Enter key (numbers only): ")

# Encryption
ciphertext = encrypt_gronsfeld(plaintext, key)
print("Encrypted message:", ciphertext)
