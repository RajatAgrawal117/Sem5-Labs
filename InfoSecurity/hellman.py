def mod_exp(base, exp, mod):
    """Function to perform modular exponentiation.
       It returns (base^exp) % mod.
    """
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:  # If exp is odd, multiply base with result
            result = (result * base) % mod
        exp = exp >> 1  # exp = exp // 2
        base = (base * base) % mod  # base = base^2 % mod
    return result


# Public parameters P and G
P = 23  # prime number
G = 9   # primitive root of P

# Private keys for Alice and Bob
a = 4   # Alice's private key
b = 3   # Bob's private key

# Step 3: Calculate public values
# Alice's public key: x = (G^a) % P
x = mod_exp(G, a, P)
print("Alice's public key (x):", x)

# Bob's public key: y = (G^b) % P
y = mod_exp(G, b, P)
print("Bob's public key (y):", y)

# Step 6: Calculate the shared secret key
# Alice computes: ka = (y^a) % P
ka = mod_exp(y, a, P)
print("Alice's computed shared secret (ka):", ka)

# Bob computes: kb = (x^b) % P
kb = mod_exp(x, b, P)
print("Bob's computed shared secret (kb):", kb)

# Step 7: Both shared secrets should be the same
if ka == kb:
    print("Shared secret successfully established! Shared Secret:", ka)
else:
    print("Something went wrong. Secrets do not match.")
