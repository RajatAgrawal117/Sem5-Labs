def caesar_cipher(text, shift):
    result = ""

    # Traverse the given text
    for i in range(len(text)):
        char = text[i]

        # Encrypt uppercase characters
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)

        # Encrypt lowercase characters
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)

        # If it's not a letter, leave it as it is
        else:
            result += char

    return result


# Get input from user
text = input("Enter the text to be encrypted: ")
shift = 7

# Encrypt the text
encrypted_text = caesar_cipher(text, shift)
print(f"Encrypted: {encrypted_text}")

# Decrypt the text
decrypted_text = caesar_cipher(encrypted_text, -shift)
print(f"Decrypted: {decrypted_text}")
