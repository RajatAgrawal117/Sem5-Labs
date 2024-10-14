def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

# Function to compute (x^y) % p


def power(x, y, p):
    result = 1
    x = x % p
    while y > 0:
        if y % 2 != 0:
            result = (result * x) % p
        y = y // 2
        x = (x * x) % p
    return result

# Function to shift and XOR the message before encryption


def shift_and_xor_message(msg, shift_amount, xor_key):
    modified_msg = ""
    for char in msg:
        # Shift the character and XOR it
        shifted_char = chr((ord(char) + shift_amount) ^ xor_key)
        modified_msg += shifted_char
    return modified_msg

# Function to reverse XOR and shift after decryption


def unshift_and_xor_message(msg, shift_amount, xor_key):
    original_msg = ""
    for char in msg:
        # Reverse the XOR and shift
        unshifted_char = chr((ord(char) ^ xor_key) - shift_amount)
        original_msg += unshifted_char
    return original_msg

# RSA encryption


def RSA_encrypt(msg, e, n):
    encrypted_text = [power(ord(char), e, n) for char in msg]
    return encrypted_text

# RSA decryption


def RSA_decrypt(encrypted_text, d, n):
    decrypted_text = ''.join(chr(power(char, d, n)) for char in encrypted_text)
    return decrypted_text


def main():
    p = int(input("Enter a prime number p: "))
    q = int(input("Enter a prime number q: "))

    msg = input("Enter the message to be encrypted: ")

    # generate n and phi
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17  # public key exponent
    d = 0

    # Calculate d such that (e * d) % phi == 1
    while (e * d) % phi != 1:
        d += 1

    print(f"Public Key (e, n) = ({e}, {n})")
    print(f"Private Key (d, n) = ({d}, {n})")

    shift_amount = 3  # shift each character by 3
    xor_key = 5       # XOR key value

    # Shift and XOR the message before encryption
    modified_message = shift_and_xor_message(msg, shift_amount, xor_key)

    # Encrypt the modified message using RSA
    encrypted_text = RSA_encrypt(modified_message, e, n)
    print("Encrypted message:", ' '.join(map(str, encrypted_text)))

    # Decrypt the message using RSA
    decrypted_text = RSA_decrypt(encrypted_text, d, n)
    print("Decrypted message (shifted and XOR-ed):", decrypted_text)

    # Reverse XOR and Shift to get the original message
    original_message = unshift_and_xor_message(
        decrypted_text, shift_amount, xor_key)
    print("Original message:", original_message)


if __name__ == "__main__":
    main()
