def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

# Function to find (x^y) % p


def power(x, y, p):
    result = 1
    x = x % p
    while y > 0:
        if y % 2 != 0:
            result = (result * x) % p
        y = y // 2
        x = (x * x) % p
    return result

# Function to encrypt the plaintext


def RSA_encrypt(msg, e, n):
    # Convert each character to ASCII and encrypt
    encrypted_text = [power(ord(char), e, n) for char in msg]
    return encrypted_text

# Function to decrypt the encrypted text


def RSA_decrypt(encrypted_text, d, n):
    # Decrypt each character and convert back to text
    decrypted_text = ''.join([chr(power(char, d, n))
                             for char in encrypted_text])
    return decrypted_text

# Main RSA Program


def main():
    p = int(input("Enter a prime number p: "))

    # Check if p is prime
    while not all(p % i != 0 for i in range(2, int(p**0.5) + 1)):
        print("p is not prime")
        p = int(input("Enter a prime number p: "))

    q = int(input("Enter a prime number q: "))

    # Check if q is prime and different from p
    while p == q or not all(q % i != 0 for i in range(2, int(q**0.5) + 1)):
        print("q is not prime or q is equal to p")
        q = int(input("Enter a prime number q: "))

    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17  # public key exponent
    d = 0

    # Calculate d such that (e * d) % phi == 1
    while (e * d) % phi != 1:
        d += 1

    print(f"Public Key (e, n) = ({e}, {n})")
    print(f"Private Key (d, n) = ({d}, {n})")

    msg = input("Enter the message to be encrypted: ")

    # Encrypt the plaintext
    encrypted_text = RSA_encrypt(msg, e, n)
    print("Encrypted message:", ' '.join(map(str, encrypted_text)))

    # Decrypt the encrypted text
    decrypted_text = RSA_decrypt(encrypted_text, d, n)
    print("Decrypted message:", decrypted_text)


if __name__ == "__main__":
    main()
