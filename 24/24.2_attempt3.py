import copy
import itertools


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
    copied_gates = copy.deepcopy(gates)
    copied_values = copy.deepcopy(values)
    i = 0
    while len(copied_gates) > 0:
        if i >= len(copied_gates):
            raise Exception('not this time!')

        command, x, y, z = copied_gates[i]
        success = apply_gate(copied_values, command, x, y, z)
        if not success:
            i += 1
            continue

        copied_gates.pop(i)
        i = 0

    return copied_values, copied_gates

def apply_gate(values, command, x, y, z):
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

def get_all_z_keys(gates):
    return sorted([gate[-1] for gate in gates if gate[-1].startswith('z')])

def bitwise_and(x_decimal, y_decimal):
    return bin(x_decimal & y_decimal)[2:]

def binary_addition(x_decimal, y_decimal):
    return bin(x_decimal + y_decimal)[2:]

if __name__ == '__main__':
    with open('C:/code/aoc-2024/24/day_24_input.txt', 'r') as f:
        contents = f.read()

    system_function = binary_addition

    values, gates = parse_input(contents)
    print(len(get_all_values_combos(values)))
    # value_combos = get_all_values_combos(values)

    # z_keys = get_all_z_keys(gates)
    # for z_key in z_keys:
    #     print(f'{z_key}: ', is_z_valid_for_all_value_combos(value_combos, gates, system_function, z_key))
