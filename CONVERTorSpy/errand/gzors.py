import sys

def xor_strings_to_chars(str1, str2):
    # XOR each character in both strings and return the resulting characters
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(str1, str2))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 xor_strings_to_chars.py <string1> <string2>")
        sys.exit(1)

    string1 = sys.argv[1]
    string2 = sys.argv[2]

    # Ensure both strings are of the same length
    if len(string1) != len(string2):
        print("Error: Strings must be of the same length.")
        sys.exit(1)

    result = xor_strings_to_chars(string1, string2)
    print(f"XOR result: {result}")
    print(result)
