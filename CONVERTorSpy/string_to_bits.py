# import sys
# 
# def string_to_bits(input_string):
#     # Convert each character to its binary representation and format to 8 bits
#     return ' '.join(format(ord(char), '08b') for char in input_string)
# 
# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("Usage: python3 string_to_bits.py <string1> <string2>")
#         sys.exit(1)
# 
#     string1 = sys.argv[1]
#     string2 = sys.argv[2]
# 
#     bits1 = string_to_bits(string1)
#     bits2 = string_to_bits(string2)
# 
#     print(f"String 1 in bits: {bits1}")
#     print(f"String 2 in bits: {bits2}")
import sys

def string_to_bits(input_string):
    # Convert each character to its binary representation and format to 8 bits
    return [format(ord(char), '08b') for char in input_string]

def xor_bits(bits1, bits2):
    # XOR each corresponding bit of the two lists of binary strings
    return ''.join(format(int(b1, 2) ^ int(b2, 2), '08b') for b1, b2 in zip(bits1, bits2))

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
    bits1 = string_to_bits(string1)
    bits2 = string_to_bits(string2)

    # XOR the bits
    sctreemd = xor_bits(bits1, bits2)

    # Print the results
    print(f"String 1 in bits: {' '.join(bits1)}")
    print(f"String 2 in bits: {' '.join(bits2)}")
    print(f"XOR result (sctreemd): {sctreemd}")

