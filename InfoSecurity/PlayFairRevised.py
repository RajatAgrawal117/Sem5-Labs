def toLowerCase(text):
    return text.lower()

def removeExtraSpace(text):
    return text.replace(" ", "")

def diagraph(text):
    diagraph = []
    group = 0
    for i in range(2, len(text), 2):
        diagraph.append(text[group:i])
        group = i
    diagraph.append(text[group:])
    return diagraph

def fillerLetter(text):
    k = len(text)
    new_word = ""
    if k % 2 == 0:
        for i in range(0, k, 2):
            if text[i] == text[i+1]:
                new_word = text[:i+1] + 'x' + text[i+1:]
                new_word = fillerLetter(new_word)
                break
        else:
            new_word = text
    else:
        for i in range(0, k-1, 2):
            if text[i] == text[i+1]:
                new_word = text[:i+1] + 'x' + text[i+1:]
                new_word = fillerLetter(new_word)
                break
        else:
            new_word = text
    return new_word

list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm',
         'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def generateKeyTable(word, list1):
    key_letters = []
    for i in word:
        if i not in key_letters:
            key_letters.append(i)

    compElements = key_letters[:]
    for i in list1:
        if i not in compElements:
            compElements.append(i)

    matrix = []
    while compElements:
        matrix.append(compElements[:5])
        compElements = compElements[5:]

    return matrix

def search(mat, letter):
    for i in range(5):
        for j in range(5):
            if mat[i][j] == letter:
                return i * 5 + j  # Return index in flattened matrix
    return -1  # In case the letter is not found

def calculateDifferences(matrix):
    differences = {}
    for i in range(5):
        for j in range(5):
            letter = matrix[i][j]
            original_index = list1.index(letter)
            current_index = i * 5 + j
            difference = original_index - current_index
            differences[letter] = difference
    return differences

def encryptByCustomRule(differences, text):
    encrypted_text = ""
    for char in text:
        if char in differences:
            diff = differences[char]
            original_index = list1.index(char)
            new_index = (original_index - diff) % 25  # Ensure the index wraps around correctly
            encrypted_text += list1[new_index]
    return encrypted_text

# User input
text_Plain = input("Enter the plain text: ").replace('j', 'i')
key = input("Enter the key text: ")

# Process plain text and key
text_Plain = removeExtraSpace(toLowerCase(text_Plain))
PlainTextList = diagraph(fillerLetter(text_Plain))
if len(PlainTextList[-1]) != 2:
    PlainTextList[-1] = PlainTextList[-1] + 'z'

key = toLowerCase(key)
Matrix = generateKeyTable(key, list1)

# Calculate differences based on the custom rule
differences = calculateDifferences(Matrix)

# Encrypt plain text using the custom rule
CipherText = encryptByCustomRule(differences, ''.join(PlainTextList))
print("CipherText:", CipherText)
