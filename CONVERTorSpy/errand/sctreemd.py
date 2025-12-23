import sys

def string_to_bits(input_string):
    # Convert each character to its binary representation and format to 8 bits
    return [format(ord(char), '08b') for char in input_string]

def xor_bits(bits1, bits2):
    # XOR each corresponding bit of the two lists of binary strings
    return ''.join(format(int(b1, 2) ^ int(b2, 2), '08b') for b1, b2 in zip(bits1, bits2))

def bits_to_ascii(bits):
    # Convert a string of 8-bit binary numbers back to ASCII characters
    ascii_string = ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))
    return ascii_string

def bits_to_bytes_to_ascii(bits):
    # Convert the binary string to bytes and then to ASCII
    byte_array = bytearray(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    #ascii_string = byte_array.decode('ascii', errors='ignore')
    return byte_array

def bytes_to_ascii(byte_sequence):
    # Convert the bytes object to an ASCII string
    ascii_string = byte_sequence.decode('ascii', errors='ignore')
    return ascii_string

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

    # XOR the biti
    sctreemd = xor_bits(bits_to_bytes_to_ascii(bits1), bits_to_bytes_to_ascii(bits2))

    # Convert XORed bytes to ASCII
    sctreemd_ascii = bytes_to_ascii(sctreemd)


    # Print the XOR result in ASCII
    print(f"XOR result (sctreemd in ASCII): {sctreemd_ascii}")
    print(string1)
    print(string2)

