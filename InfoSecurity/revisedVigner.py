def generate_key(plaintext, key):
    key = list(key)
    if len(plaintext) == len(key):
        return key
    else:
        for i in range(len(plaintext) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

def xor_vigenere_encrypt(plaintext, key):
    ciphertext = []
    for i in range(len(plaintext)):
        # XOR each character and then convert back to an A-Z character
        x = (ord(plaintext[i]) - ord('A')) ^ (ord(key[i]) - ord('A'))
        x = (x % 26) + ord('A')  # Keep it within A-Z range
        ciphertext.append(chr(x))
    return "".join(ciphertext)

def xor_vigenere_decrypt(ciphertext, key):
    plaintext = []
    for i in range(len(ciphertext)):
        # XOR the ciphertext character with the key to retrieve the original plaintext
        x = (ord(ciphertext[i]) - ord('A')) ^ (ord(key[i]) - ord('A'))
        x = (x % 26) + ord('A')  # Keep it within A-Z range
        plaintext.append(chr(x))
    return "".join(plaintext)

# Input from the user
plaintext = input("Enter the plaintext: ").upper()
key = input("Enter the key: ").upper()

# Generate the key
key = generate_key(plaintext, key)

# Encrypt the plaintext
ciphertext = xor_vigenere_encrypt(plaintext, key)
print(f"Ciphertext: {ciphertext}")

# Decrypt the ciphertext
decrypted_text = xor_vigenere_decrypt(ciphertext, key)
print(f"Decrypted text: {decrypted_text}")
