def generate_key(plaintext, key):
    key = list(key)
    if len(plaintext) == len(key):
        return key
    else:
        for i in range(len(plaintext) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)


def encrypt_vigenere(plaintext, key):
    ciphertext = []
    for i in range(len(plaintext)):
        x = (ord(plaintext[i]) + ord(key[i])) % 26
        x += ord('A')
        ciphertext.append(chr(x))
    return "".join(ciphertext)


def decrypt_vigenere(ciphertext, key):
    plaintext = []
    for i in range(len(ciphertext)):
        x = (ord(ciphertext[i]) - ord(key[i]) + 26) % 26
        x += ord('A')
        plaintext.append(chr(x))
    return "".join(plaintext)



plaintext = input("Enter the plaintext: ").upper()
key = input("Enter the key: ").upper()

key = generate_key(plaintext, key)

ciphertext = encrypt_vigenere(plaintext, key)
print(f"Ciphertext: {ciphertext}")

decrypted_text = decrypt_vigenere(ciphertext, key)
print(f"Decrypted text: {decrypted_text}")