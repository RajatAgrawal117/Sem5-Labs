# Digital Signature using RSA with Decryption (Verification)

# Helper functions for RSA algorithm implementation
def modular_exponentiation(base, exp, mod):
    """Perform modular exponentiation (base^exp) % mod"""
    result = 1
    while exp > 0:
        if exp % 2 == 1:  # If exp is odd, multiply result with the base
            result = (result * base) % mod
        base = (base * base) % mod  # Square the base
        exp //= 2  # Divide the exponent by 2
    return result

def gcd_extended(a, b):
    """Extended GCD algorithm to compute modular inverse"""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    """Compute modular inverse of a under modulo m"""
    gcd, x, _ = gcd_extended(a, m)
    if gcd != 1:
        return None  # Inverse doesn't exist if gcd is not 1
    return x % m

# Simulate SHA-1 hash function (basic simulation for simplicity)
def simple_hash(message):
    """Basic hash function for message"""
    hash_val = 0
    for char in message:
        hash_val = (hash_val * 31 + ord(char)) % 253  # Small modulo for demonstration
    return hash_val

# RSA key generation
def generate_keys(p, q):
    """Generate public and private keys"""
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 17  # Public exponent (should be relatively prime with phi_n)
    d = mod_inverse(e, phi_n)
    if d is None:
        raise ValueError("Modular inverse for public exponent e does not exist")
    return (e, n), (d, n)  # (public_key, private_key)

# Digital signature functions
def sign_message(private_key, message_hash):
    """Sign the message by encrypting the hash using the private key"""
    d, n = private_key
    return modular_exponentiation(message_hash, d, n)

def verify_signature(public_key, signature, message_hash):
    """Verify the signature by decrypting it using the public key and comparing with hash"""
    e, n = public_key
    decrypted_hash = modular_exponentiation(signature, e, n)
    return decrypted_hash == message_hash

# Decrypt a message (reverse RSA encryption)
def decrypt_message(private_key, ciphertext):
    """Decrypt a message using the private key"""
    d, n = private_key
    return modular_exponentiation(ciphertext, d, n)

# Main flow for the digital signature and decryption
def main():
    # Step 1: Key generation for Sender (A)
    p, q = 61, 53  # Example small prime numbers (should be larger in real RSA)
    public_key_A, private_key_A = generate_keys(p, q)

    # Step 2: Sender A creates a message and calculates its hash
    message = "Hello, this is a test message!"
    message_hash = simple_hash(message)
    print(f"Message Hash (MD1): {message_hash}")

    # Step 3: Sender A signs the message using its private key
    signature = sign_message(private_key_A, message_hash)
    print(f"Digital Signature: {signature}")

    # Step 4: Sender A encrypts the message (optional, simulating encrypted communication)
    encrypted_message = sign_message(public_key_A, simple_hash(message))  # Using public key to encrypt
    print(f"Encrypted Message (Simulated): {encrypted_message}")

    # Sender A sends the message and signature to Receiver B
    received_message = message  # B receives the original message
    received_signature = signature  # B receives the signature
    received_encrypted_message = encrypted_message  # B receives encrypted message

    # Step 5: Receiver B calculates the hash of the received message
    received_message_hash = simple_hash(received_message)
    print(f"Received Message Hash (MD2): {received_message_hash}")

    # Step 6: Receiver B verifies the signature using A's public key
    is_valid_signature = verify_signature(public_key_A, received_signature, received_message_hash)
    
    if is_valid_signature:
        print("Signature verified successfully! The message is authentic and unaltered.")
    else:
        print("Signature verification failed! The message may have been altered.")
    
    # Step 7: Receiver B decrypts the encrypted message (if any)
    decrypted_message_hash = decrypt_message(private_key_A, received_encrypted_message)
    print(f"Decrypted Message Hash: {decrypted_message_hash}")
    
    # Verifying decryption (optional, for encrypted message verification)
    if decrypted_message_hash == simple_hash(received_message):
        print("Decryption successful! The encrypted message is correct.")
    else:
        print("Decryption failed! The encrypted message is incorrect.")

# Run the main function
if __name__ == "__main__":
    main()
