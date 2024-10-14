def binary_addition(a, b):
    """Perform binary addition of two binary strings a and b."""
    max_len = max(len(a), len(b))
    
    # Padding the binary strings to make them equal length
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    
    result = ''
    carry = 0
    
    # Add the two binary strings
    for i in range(max_len - 1, -1, -1):
        r = carry
        r += 1 if a[i] == '1' else 0
        r += 1 if b[i] == '1' else 0
        result = ('1' if r % 2 == 1 else '0') + result
        carry = 0 if r < 2 else 1
    
    # If there's a carry at the end, add it to the result
    if carry != 0:
        result = '1' + result

    return result

def ones_complement(binary_str):
    """Return the one's complement of a binary string."""
    return ''.join('1' if bit == '0' else '0' for bit in binary_str)

def calculate_checksum(data, word_size):
    """Calculate checksum by splitting data into word_size chunks."""
    # Split the data into chunks of word_size bits
    chunks = [data[i:i+word_size] for i in range(0, len(data), word_size)]

    # Add all chunks using binary addition
    checksum = chunks[0]
    for chunk in chunks[1:]:
        checksum = binary_addition(checksum, chunk)
        
        # If the result exceeds word_size, wrap the carry around
        if len(checksum) > word_size:
            extra_bits = len(checksum) - word_size
            checksum = binary_addition(checksum[extra_bits:], checksum[:extra_bits])

    # Take one's complement of the result to get the checksum
    checksum = ones_complement(checksum.zfill(word_size))

    return checksum

# Input message and word size
message = input("Enter the message in binary: ")
word_size = int(input("Enter the word size (e.g., 8, 16): "))

# Calculate checksum
checksum = calculate_checksum(message, word_size)

# Display the results
print(f"The calculated checksum is: {checksum}")