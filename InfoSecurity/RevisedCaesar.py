def vigenere_cipher(text, keyword, encrypt=True):
    result = []
    keyword = keyword.lower()
    keyword_repeated = (keyword * (len(text) // len(keyword) + 1))[:len(text)]
    shift_direction = 1 if encrypt else -1

    for i, char in enumerate(text):
        if char.isalpha():
            shift = shift_direction * (ord(keyword_repeated[i]) - ord('a'))
            if char.isupper():
                result.append(
                    chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            elif char.islower():
                result.append(
                    chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
        else:
            result.append(char)

    return ''.join(result)


# Get input from user
text = input("Enter the text to be encrypted: ")
keyword = input("Enter the keyword: ")

# Encrypt the text
encrypted_text = vigenere_cipher(text, keyword, encrypt=True)
print(f"Encrypted: {encrypted_text}")

# Decrypt the text
decrypted_text = vigenere_cipher(encrypted_text, keyword, encrypt=False)
print(f"Decrypted: {decrypted_text}")
