import struct

def hex_to_float(hex_string):
    # Convert the hexadecimal string to an integer
    int_value = int(hex_string, 16)
    
    # Check the length of the hex string to determine whether it's 32-bit or 64-bit
    if len(hex_string) == 8:  # 32-bit float
        # Pack the integer into bytes as a 32-bit float (IEEE 754 single-precision)
        packed = struct.pack('>I', int_value)
        # Unpack the bytes as a float
        float_value = struct.unpack('>f', packed)[0]
    elif len(hex_string) == 16:  # 64-bit double
        # Pack the integer into bytes as a 64-bit float (IEEE 754 double-precision)
        packed = struct.pack('>Q', int_value)
        # Unpack the bytes as a double
        float_value = struct.unpack('>d', packed)[0]
    else:
        raise ValueError("Invalid hex string length for IEEE 754 float conversion.")
    
    return float_value

if __name__ == "__main__":
    # Example input: hexadecimal string
    hex_string = input("Enter a hexadecimal string: ")

    try:
        # Convert hex to float
        float_value = hex_to_float(hex_string)
        print(f"The float value is: {float_value}")
    except ValueError as e:
        print(f"Error: {e}")
