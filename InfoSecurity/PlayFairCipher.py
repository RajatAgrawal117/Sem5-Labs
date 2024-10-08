def toLowerCase(text):
    return text.lower()

# Function to remove all spaces in a string
def removeExtraSpace(text):
    return text.replace(" ", "")

# Function to group 2 elements of a string as a list element
def diagraph(text):
    diagraph = []
    group = 0
    for i in range(2, len(text), 2):
        diagraph.append(text[group:i])
        group = i
    diagraph.append(text[group:])
    return diagraph

# Function to fill a letter in a string element if 2 letters in the same string match
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
                return i, j

def encrypt_RowRule(matr, e1r, e1c, e2r, e2c):
    char1 = matr[e1r][0] if e1c == 4 else matr[e1r][e1c + 1]
    char2 = matr[e2r][0] if e2c == 4 else matr[e2r][e2c + 1]
    return char1, char2

def encryptColumnRule(matr, e1r, e1c, e2r, e2c):
    char1 = matr[0][e1c] if e1r == 4 else matr[e1r + 1][e1c]
    char2 = matr[0][e2c] if e2r == 4 else matr[e2r + 1][e2c]
    return char1, char2

def encrypt_RectangleRule(matr, e1r, e1c, e2r, e2c):
    char1 = matr[e1r][e2c]
    char2 = matr[e2r][e1c]
    return char1, char2

def encryptByPlayfairCipher(Matrix, plainList):
    CipherText = []
    for pair in plainList:
        ele1_x, ele1_y = search(Matrix, pair[0])
        ele2_x, ele2_y = search(Matrix, pair[1])

        if ele1_x is None or ele2_x is None:
            raise ValueError(f"Character '{pair[0]}' or '{pair[1]}' not found in matrix")

        if ele1_x == ele2_x:
            c1, c2 = encrypt_RowRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        elif ele1_y == ele2_y:
            c1, c2 = encryptColumnRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        else:
            c1, c2 = encrypt_RectangleRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)

        CipherText.append(c1 + c2)
    return CipherText

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

# Encrypt plain text
CipherList = encryptByPlayfairCipher(Matrix, PlainTextList)

CipherText = "".join(CipherList)
print("CipherText:", CipherText)
