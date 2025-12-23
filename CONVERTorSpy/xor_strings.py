import sys

def string_to_bits(input_string):
    # Convert each character to its binary representation and format to 8 bits
    return [format(ord(char), '08b') for char in input_string]

def xor_bits(bitString_a, bitString_b):
    # XOR each corresponding bit of the two lists of binary strings
    return ''.join(format(int(b1, 2) ^ int(b2, 2), '08b') for b1, b2 in zip(bitString_a, bitString_b))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 string_to_bits.py <string1> <string2>")
        sys.exit(1)

    string1 = sys.argv[1]
    string2 = sys.argv[2]

    if len(string1) != len(string2):
        print("Error: Strings must be of the same length.")
        sys.exit(1)

    # Convert strings to lists of bit strings
    bitString_a = string_to_bits(string1)
    bitString_b = string_to_bits(string2)

    # XOR the bits
    ekxored = xor_bits(bitString_a, bitString_b)
    ekxed = int(ekxored, 2)
    # Print the results
    print("")
    print(f"string a in bits: {' '.join(bitString_a)}")
    print(f"string b in bits: {' '.join(bitString_b)}")
    print(f"XOR result      : {ekxored}")
    print(f"HEX of ekxored  : {ekxed}")

    print("")
