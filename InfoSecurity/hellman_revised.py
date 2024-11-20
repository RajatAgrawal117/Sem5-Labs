import hashlib


def generate_key_hash(key):
    """Generates a SHA-256 hash of the given key."""
    key_str = str(key).encode()
    return hashlib.sha256(key_str).hexdigest()


def generate_public_key(g, private_key, p):
    """Generates a public key using modular exponentiation."""
    return pow(g, private_key, p)


def calculate_shared_secret(other_public_key, private_key, p):
    """Calculates the shared secret key."""
    return pow(other_public_key, private_key, p)


p = int(input("Enter a prime number (P): "))
g = int(input("Enter a generator for P (G): "))

# Input private keys for sender and receiver
sender_private_key = int(input("Enter the sender's private key: "))
receiver_private_key = int(input("Enter the receiver's private key: "))

# Generate public keys
sender_public_key = generate_public_key(g, sender_private_key, p)
receiver_public_key = generate_public_key(g, receiver_private_key, p)

# Create hashes for each public key for integrity verification
sender_hash = generate_key_hash(sender_public_key)
receiver_hash = generate_key_hash(receiver_public_key)

# Display public parameters, private keys, public keys, and their hashes
print(f"\nPublic parameters: (P = {p}, G = {g})")
print(f"Sender's private key: {sender_private_key}")
print(f"Receiver's private key: {receiver_private_key}")
print(f"Sender's public key: {sender_public_key} (Hash: {sender_hash})")
print(f"Receiver's public key: {receiver_public_key} (Hash: {receiver_hash})")

# Exchange and verify hashes to ensure public keys' integrity
print("\nVerifying public key integrity...")
if (generate_key_hash(receiver_public_key) == receiver_hash and
        generate_key_hash(sender_public_key) == sender_hash):
    print("Public keys verified successfully.")

    # Calculate shared secrets
    sender_shared_secret = calculate_shared_secret(
        receiver_public_key, sender_private_key, p)
    receiver_shared_secret = calculate_shared_secret(
        sender_public_key, receiver_private_key, p)

    # Display the shared secrets for both parties (should match)
    print(f"\nShared secret for Sender: {sender_shared_secret}")
    print(f"Shared secret for Receiver: {receiver_shared_secret}")

    # Confirm if shared secrets match
    if sender_shared_secret == receiver_shared_secret:
        print("Shared secret established successfully.")
    else:
        print("Error: Shared secrets do not match.")
else:
    print("Error: Key verification failed. Public keys may have been tampered with.")
