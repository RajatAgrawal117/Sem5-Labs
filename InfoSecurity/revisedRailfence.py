def reorder_rows(rail, order):
    return [rail[i] for i in order]

def reverse_reorder_rows(rail, order):
    reverse_order = sorted(range(len(order)), key=lambda k: order[k])
    return [rail[i] for i in reverse_order]

def print_rail_matrix(rail):
    for row in rail:
        print(' '.join(row))
    print("\n")

def encrypt_rail_fence(text, key):
    if key == 1:
        return text, []

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

    print("Rail Matrix before Reordering:")
    print_rail_matrix(rail)
    
    # Define the row order for reordering (example: [2, 0, 1] for 3 rows)
    row_order = list(range(key))
    row_order = row_order[::-1]  # Reverse the order as an example
    
    reordered_rail = reorder_rows(rail, row_order)
    
    print("Rail Matrix after Reordering:")
    print_rail_matrix(reordered_rail)
    
    cipher_text = []
    for row in reordered_rail:
        cipher_text.extend([char for char in row if char != ' '])
    
    return "".join(cipher_text), row_order

def decrypt_rail_fence(cipher, key, row_order):
    if key == 1:
        return cipher
    
    rail = [[' ' for _ in range(len(cipher))] for _ in range(key)]
    row, col = 0, 0
    dir_down = None

    # Mark the positions where characters will be placed
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
    
    # Place the cipher characters into the rail matrix
    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*' and index < len(cipher):
                rail[i][j] = cipher[index]
                index += 1

    # Reverse the reordering to get back to the original order
    reordered_rail = reverse_reorder_rows(rail, row_order)

    print("Rail Matrix after Reordering Back and Filling:")
    print_rail_matrix(reordered_rail)

    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        
        if reordered_rail[row][col] != ' ':
            result.append(reordered_rail[row][col])
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
cipher_text, row_order = encrypt_rail_fence(text, key)
print(f"Encrypted Text: {cipher_text}")

# Decrypt the text
original_text = decrypt_rail_fence(cipher_text, key, row_order)
print(f"Decrypted Text: {text}")
