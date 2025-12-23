import sys
import struct

class InputData:
    def __init__(self, original_input):
        self.original_input = original_input
        self.data_type = self.determine_data_type()
        self.string_value = str(self.determine_value())
        self.bitField = self.get_bit_field()
        self.hexField = self.get_hex_field()
        
        if self.data_type == 'float':
            self.float_value, self.left_side_length, self.right_side_length = self.get_float_details()
        elif self.data_type == 'expression':
            self.boolean_value, self.error = self.evaluate_expression()
        elif self.data_type == 'int':
            self.int_value, self.is_signed, self.set_size = self.get_integer_details()
        else:
            self.boolean_value = None  # Ensure boolean_value is initialized to avoid AttributeError
            self.error = None

    def determine_data_type(self):
        if self.original_input.startswith("'") and self.original_input.endswith("'"):
            return 'expression'
        elif self.original_input.startswith('%'):
            return 'float'
        elif self.original_input.startswith('(') and self.original_input.endswith(')'):
            return 'int'
        return 'string'

    def determine_value(self):
        if self.data_type == 'float':
            return float(self.original_input[1:])
        elif self.data_type == 'expression':
            return self.evaluate_expression()
        elif self.data_type == 'int':
            return self.original_input[1:-1]  # Strip the parentheses
        return self.original_input  # For strings, return as is

    def get_float_details(self):
        float_value = float(self.original_input[1:])
        left_side, right_side = self.original_input[1:].split('.')
        return float_value, len(left_side), len(right_side)

    def evaluate_expression(self):
        expression = self.original_input[1:-1]
        expression = expression.replace(' AND ', ' and ')
        expression = expression.replace(' OR ', ' or ')
        expression = expression.replace('XOR', ' != ')
        expression = expression.replace('^', ' != ')
        expression = expression.replace('!', ' not ')
        expression = expression.replace('0', 'False')
        expression = expression.replace('1', 'True')
        try:
            result = eval(expression)
            if not isinstance(result, bool):
                raise ValueError("Expression did not evaluate to a boolean value.")
            return result, None
        except Exception as e:
            return None, str(e)

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
            packed = struct.pack('>f', float(self.original_input[1:]))
            return ''.join(format(byte, '08b') for byte in packed)
        elif self.data_type == 'expression':
            if self.boolean_value is None:
                return ''
            return format(1 if self.boolean_value else 0, '08b')
        elif self.data_type == 'int':
            int_value = self.determine_value()
            if isinstance(int_value, list):
                return ''.join(format(v, '08b') for v in int_value)
            return format(int_value, '08b')

    def get_hex_field(self):
        if self.data_type == 'float':
            packed = struct.pack('>f', float(self.original_input[1:]))
            return packed.hex()
        elif self.data_type == 'string':
            return ''.join(format(ord(char), '02x') for char in self.original_input)
        elif self.data_type == 'int':
            int_value = self.determine_value()
            if isinstance(int_value, list):
                return ' '.join(format(v, 'x') for v in int_value)
            return format(int_value, 'x')
        elif self.data_type == 'expression':
            if self.boolean_value is None:
                return ''
            return format(1 if self.boolean_value else 0, 'x')
        return ''

    def __repr__(self):
        attrs = [f"Original Input: {self.original_input}", f"Data Type: {self.data_type}", f"String: {self.string_value}",
                 f"Bit Field: {self.bitField}", f"Hex Field: {self.hexField}"]
        
        if self.data_type == 'float':
            attrs.extend([f"Float Value: {self.float_value}", f"Left Side Length: {self.left_side_length}", f"Right Side Length: {self.right_side_length}"])
        elif self.data_type == 'expression':
            attrs.append(f"Boolean Value: {self.boolean_value}")
            if self.error:
                attrs.append(f"Error: {self.error}")
        elif self.data_type == 'int':
            attrs.extend([f"Int Value: {self.int_value}", f"Is Signed: {self.is_signed}", f"Set Size: {self.set_size}"])
        
        return '\n  '.join(attrs)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 244:
        print("Usage: python3 script.py <input1> <input2> ... <input243>")
        sys.exit(1)

    # Process all input strings into InputData objects
    inputs = [InputData(arg) for arg in sys.argv[1:]]

    # Print results for each input
    print("")
    for i, input_obj in enumerate(inputs):
        print(f"Input {i+1}:")
        print(f"  {input_obj}")
        print("")
