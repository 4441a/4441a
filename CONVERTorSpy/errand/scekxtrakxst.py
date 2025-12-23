def string_to_bits(s):
    """Convert a string to a list of bits."""
    byte_array = s.encode('utf-8')
    bit_list = []
    for byte in byte_array:
        bits = bin(byte)[2:].zfill(8)  # Convert byte to 8-bit binary representation
        bit_list.extend(bits)
    return bit_list

def print_bits(bits):
    """Print bits as a string."""
    print(''.join(bits))

def xor_bits(bits1, bits2):
    """Perform XOR between two lists of bits."""
    return [str(int(b1) ^ int(b2)) for b1, b2 in zip(bits1, bits2)]

def main():
    # Read input strings
    str1 = input("Enter the first string (or press Enter to skip): ")
    str2 = input("Enter the second string (or press Enter to skip): ")

    if str1:
        bits1 = string_to_bits(str1)
    else:
        bits1 = []

    if str2:
        bits2 = string_to_bits(str2)
    else:
        bits2 = []

    # Print byte representations
    print("Bytes of first string:", str1.encode('utf-8'))
    print("Bytes of second string:", str2.encode('utf-8'))

    # Print bit representations
    print("Bits of first string:")
    print_bits(bits1)

    print("Bits of second string:")
    print_bits(bits2)

    # Concatenate bit lists
    combined_bits = bits1 + bits2
    length = len(combined_bits)
    half_length = length // 2

    # Split into halves
    first_half = combined_bits[:half_length]
    second_half = combined_bits[half_length:]

    # Handle cases where halves are not of equal length
    if len(first_half) == len(second_half):
        result_bits = xor_bits(first_half, second_half)
        print("XOR result:")
        print_bits(result_bits)
    else:
        # Extract extra bit if needed
        if len(first_half) > len(second_half):
            zr = first_half[-1]
            first_half = first_half[:-1]
        else:
            zr = second_half[-1]
            second_half = second_half[:-1]

        print("Remaining bit (zr):", zr)
        
        # XOR the adjusted halves
        result_bits = xor_bits(first_half, second_half)
        print("XOR result:")
        print_bits(result_bits)

if __name__ == "__main__":
    main()

