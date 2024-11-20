def create_key(plain_text_list):
    key = []
    l = len(plain_text_list)
    for i in range(1, l + 1):
        for j in range(len(plain_text_list[i - 1])):
            key.append(i + j)
    return key

# Function to calculate result


def calculate(plain_text, key):
    plain_text = plain_text.replace(' ', '')
    result = ''
    l = len(key)
    for i in range(l):
        char = ord(plain_text[i])
        if char + key[i] > 122:  # Wrap around if exceeding 'z'
            new_char = chr(char + key[i] - 26)
        else:
            new_char = chr(char + key[i])
        result += new_char
    return result

# Function to encrypt plaintext


def encrypt(plain_text):
    plain_text_list = plain_text.split()
    key = create_key(plain_text_list)
    return calculate(plain_text, key), key

# Main function to ask user input and print result


def main():
    plain_text = input("Enter the plain text: ")
    result = encrypt(plain_text)
    print(f"Key: {''.join(str(result[1]))}")
    print(f"Encrypted text: {result[0]}")


if __name__ == '__main__':
    main()
