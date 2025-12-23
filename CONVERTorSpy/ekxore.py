import sys

class InputData:
    def __init__(self, original_input):
        self.original_input = original_input
        self.data_type = self.determine_data_type()
        self.string_value = str(self.determine_value())
        self.bitField = self.get_bit_field()
        self.hexField = hex(int(self.bitField, 2))[2:]  # Convert binary to hex, removing the "0x" prefix
        
        if self.data_type == 'float':
            self.float_value, self.left_side_length, self.right_side_length = self.get_float_details()
        elif self.data_type == 'bool':
            self.boolean_value = self.get_boolean_value()
        elif self.data_type == 'int':
            self.int_value, self.is_signed, self.set_size = self.get_integer_details()

    def determine_data_type(self):
        if self.original_input.startswith('%'):
            return 'float'
        elif self.original_input.startswith('&'):
            return 'bool'
        elif self.original_input.startswith('(') and self.original_input.endswith(')'):
            return 'int'
        return 'string'

    def determine_value(self):
        if self.data_type == 'float':
            return float(self.original_input[1:])
        elif self.data_type == 'bool':
            return self.original_input[1:].lower() == 'true'
        elif self.data_type == 'int':
            return self.original_input[1:-1]  # Strip the parentheses
        return self.original_input  # For strings, return as is

    def get_float_details(self):
        float_value = float(self.original_input[1:])
        left_side, right_side = self.original_input[1:].split('.')
        return float_value, len(left_side), len(right_side)

    def get_boolean_value(self):
        return self.original_input[1:].lower() == 'true'

    def get_integer_details(self):
        values = self.original_input[1:-1].split()
        int_values = list(map(int, values))
        set_size = len(int_values)
        is_signed = any(v < 0 for v in int_values)
        return int_values if set_size > 1 else int_values[0], is_signed, set_size

    def get_bit_field(self):
        if self.data_type == 'string':
            return ''.join(format(ord(char), '08b') for char in self.original_input)
        elif self.data_type == 'float':
            # Convert float to its IEEE 754 binary representation
            float_bits = ''.join(format(ord(c), '08b') for c in float(self.original_input[1:]).hex())
            return float_bits
        elif self.data_type == 'bool':
            return format(1 if self.boolean_value else 0, '08b')
        elif self.data_type == 'int':
            int_value = self.determine_value()
            if isinstance(int_value, list):
                return ''.join(format(v, '08b') for v in int_value)
            return format(int_value, '08b')

    def __repr__(self):
        attrs = [f"Original Input: {self.original_input}", f"Data Type: {self.data_type}", f"String: {self.string_value}",
                 f"Bit Field: {self.bitField}", f"Hex Field: {self.hexField}"]
        
        if self.data_type == 'float':
            attrs.extend([f"Float Value: {self.float_value}", f"Left Side Length: {self.left_side_length}", f"Right Side Length: {self.right_side_length}"])
        elif self.data_type == 'bool':
            attrs.append(f"Boolean Value: {self.boolean_value}")
        elif self.data_type == 'int':
            attrs.extend([f"Int Value: {self.int_value}", f"Is Signed: {self.is_signed}", f"Set Size: {self.set_size}"])
        
        return '\n  '.join(attrs)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 244:
        print("Usage: python3 string_to_bits.py <input1> <input2> ... <input243>")
        sys.exit(1)

    # Process all input strings into InputData objects
    inputs = [InputData(arg) for arg in sys.argv[1:]]

    # Print results for each input
    print("")
    for i, input_obj in enumerate(inputs):
        print(f"Input {i+1}:")
        print(f"  {input_obj}")
        print("")
