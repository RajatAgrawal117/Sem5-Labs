def print_rail_matrix(rail, text_len):
    for row in rail:
        for col in range(text_len):
            print(row[col], end=" ")
        print("\n")
    print("\n")


def encrypt_rail_fence(text, key):
    if key == 1:
        return text
    
    # Create the rail matrix
    rail = [[' ' for _ in range(len(text))] for _ in range(key)]
    row, col = 0, 0
    dir_down = False

    for char in text:
        rail[row][col] = char
        col += 1
        
        if row == 0 or row == key - 1:
            dir_down = not dir_down
        
        if dir_down:
            row += 1
        else:
            row -= 1

    print("Rail Matrix during Encryption:")
    print_rail_matrix(rail, len(text))
    
    # Construct the cipher text from the rail matrix
    cipher_text = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != ' ':
                cipher_text.append(rail[i][j])
    
    return "".join(cipher_text)


def decrypt_rail_fence(cipher, key):
    if key == 1:
        return cipher
    
    # Create the rail matrix
    rail = [[' ' for _ in range(len(cipher))] for _ in range(key)]
    row, col = 0, 0
    dir_down = None

    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        
        rail[row][col] = '*'
        col += 1
        
        if dir_down:
            row += 1
        else:
            row -= 1

    print("Rail Matrix after marking positions during Decryption:")
    print_rail_matrix(rail, len(cipher))

    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*' and index < len(cipher):
                rail[i][j] = cipher[index]
                index += 1

    print("Rail Matrix after filling in cipher text during Decryption:")
    print_rail_matrix(rail, len(cipher))

    # Reconstruct the original text
    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        
        if rail[row][col] != ' ':
            result.append(rail[row][col])
            col += 1
        
        if dir_down:
            row += 1
        else:
            row -= 1
    
    return "".join(result)


# Example usage
text = "WEAREDISCOVEREDFLEEATONCE"
key = 3

# Encrypt the text
cipher_text = encrypt_rail_fence(text, key)
print(f"Encrypted Text: {cipher_text}")

# Decrypt the text
original_text = decrypt_rail_fence(cipher_text, key)
print(f"Decrypted Text: {original_text}")
