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

def as_decimal(values):
    return int(as_binary_string(values), 2)

def as_binary_string(values):
    return ''.join([str(val) for _, val in values])

def get_all_x(values, reverse=True):
    return sorted([(key, val) for key, val in values.items() if key.startswith('x')], key=lambda x: x[0], reverse=reverse)

def get_all_y(values, reverse=True):
    return sorted([(key, val) for key, val in values.items() if key.startswith('y')], key=lambda y: y[0], reverse=reverse)

def get_all_z(values, reverse=True):
    return sorted([(key, val) for key, val in values.items() if key.startswith('z')], key=lambda z: z[0], reverse=reverse)

def get_output_swap_combos(gates, num_swap_pairs):
    # first - get all pairs
    pairs = set([])
    for i in gates:
        for j in gates:
            i_output = i[3]
            j_output = j[3]
            if i_output != j_output:
                pairs.add(tuple(sorted([i_output, j_output])))
    return itertools.combinations(pairs, num_swap_pairs)

def is_valid_combo(combo):
    outputs = set([])
    for pair in combo:
        if pair[0] in outputs or pair[1] in outputs:
            return False
        outputs.add(pair[0])
        outputs.add(pair[1])
    return True

def is_valid_addition(values, x_vals=None, y_vals=None, z_vals=None):
    if x_vals is None:
        x_vals = get_all_x(values)
    if y_vals is None:
        y_vals = get_all_y(values)
    if z_vals is None:
        z_vals = get_all_z(values)

    return binary_addition(as_binary_string(x_vals), as_binary_string(y_vals)) == as_binary_string(z_vals)

def bitwise_and(x_values, y_values):
    return bin(as_decimal(x_values) & as_decimal(y_values))[2:]

def binary_addition(x_values, y_values):
    return bin(as_decimal(x_values) + as_decimal(y_values))[2:]

if __name__ == '__main__':
    with open('C:/code/aoc-2024/24/day_24_test_part2.txt', 'r') as f:
        contents = f.read()

    values, gates = parse_input(contents)
    apply_all_gates(values, gates)
    pprint.pprint(values)

    x_dec = get_x_as_decimal(values)
    y_dec = get_y_as_decimal(values)
    z_bin = get_z_as_binary_string(values)

    print('x + y = ', bitwise_and(x_dec, y_dec))
    print('z = ', z_bin)
