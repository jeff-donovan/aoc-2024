import copy
import itertools
import pprint


def parse_input(contents):
    values_content, gates_content = contents.split('\n\n')

    values = {}
    for line in values_content.split('\n'):
        if line:
            k, v = line.split(': ')
            values[k] = int(v)

    gates = []
    for gate in gates_content.split('\n'):
        if gate:
            command_data, z = gate.split(' -> ')
            x, command, y = command_data.split(' ')
            gates.append((command, x, y, z))

    return values, gates

def is_z_valid_for_all_value_combos(value_combos, gates, system_function, z_key):
    for values in value_combos:
        try:
            applied_values, _ = apply_all_gates(values, gates)
            if not is_z_valid(applied_values, system_function, z_key):
                return False
        except:
            return False
    return True

def is_z_valid(values, system_function, z_key):
    expected = get_expected(values, system_function)
    z_index = int(z_key[1:])
    return expected[::-1][z_index] == str(values[z_key])

def get_expected(values, system_function):
    x_decimal = get_x_as_decimal(values)
    y_decimal = get_y_as_decimal(values)
    return system_function(x_decimal, y_decimal)

def apply_all_gates(values, gates):
    i = 0
    while len(gates) > 0:
        if i >= len(gates):
            raise Exception('not this time!')

        command, x, y, z = gates[i]
        success = apply_gate(values, command, x, y, z)
        if not success:
            i += 1
            continue
        else:
            print('success')

        gates.pop(i)
        i = 0

    return values, values

def apply_gate(values, command, x, y, z):
    print('inside apply_gate')
    if z in values:
        return True

    x_val = values.get(x)
    y_val = values.get(y)

    if x_val is None or y_val is None:
        return False

    if command == 'AND':
        values[z] = gate_and(x_val, y_val)

    if command == 'OR':
        values[z] = gate_or(x_val, y_val)

    if command == 'XOR':
        values[z] = gate_xor(x_val, y_val)

    return True

def gate_and(x_val, y_val):
    if x_val == 1 and y_val == 1:
        return 1
    return 0

def gate_or(x_val, y_val):
    if x_val == 1 or y_val == 1:
        return 1
    return 0

def gate_xor(x_val, y_val):
    if x_val != y_val:
        return 1
    return 0

def get_all_values_combos(values):
    x_keys = get_all_x_keys(values)
    y_keys = get_all_y_keys(values)
    keys = x_keys + y_keys

    result = []
    for values_combo in itertools.product([0, 1], repeat=len(keys)):
        combo = {}
        for i in range(len(keys)):
            combo[keys[i]] = values_combo[i]
        result.append(combo)

    return result

def get_z_as_decimal(values):
    return int(get_z_as_binary_string(values), 2)

def get_z_as_binary_string(values):
    z_keys = get_all_z_keys(values)
    z_values = [values[key] for key in z_keys]
    return as_binary_string(z_values)

def get_y_as_decimal(values):
    return int(get_y_as_binary_string(values), 2)

def get_y_as_binary_string(values):
    y_keys = get_all_y_keys(values)
    y_values = [values[key] for key in y_keys]
    return as_binary_string(y_values)

def get_x_as_decimal(values):
    return int(get_x_as_binary_string(values), 2)

def get_x_as_binary_string(values):
    x_keys = get_all_x_keys(values)
    x_values = [values[key] for key in x_keys]
    return as_binary_string(x_values)

def as_binary_string(values_list):
    return ''.join([str(val) for val in values_list])

def get_all_x_keys(values):
    return sorted([key for key in values.keys() if key.startswith('x')])

def get_all_y_keys(values):
    return sorted([key for key in values.keys() if key.startswith('y')])

def get_all_z_keys(values):
    return sorted([key for key in values.keys() if key.startswith('z')])

def bitwise_and(x_decimal, y_decimal):
    return bin(x_decimal & y_decimal)[2:]

def binary_addition(x_decimal, y_decimal):
    return bin(x_decimal + y_decimal)[2:]

if __name__ == '__main__':
    with open('C:/code/aoc-2024/24/day_24_edit_input.txt', 'r') as f:
        contents = f.read()

    values, gates = parse_input(contents)
    apply_all_gates(values, gates)
    pprint.pprint(values)

    x_dec = get_x_as_decimal(values)
    y_dec = get_y_as_decimal(values)
    z_bin = get_z_as_binary_string(values)

    print('x + y = ', binary_addition(x_dec, y_dec))
    print('z = ', z_bin)
