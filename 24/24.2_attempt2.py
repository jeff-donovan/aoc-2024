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

def setup(values, gates):
    x_values = get_all_x(values)
    y_values = get_all_y(values)

    # TODO: update to addition when using input
    expected_result = bitwise_and(x_values, y_values)

    locked = set([])
    for xkey, _ in x_values:
        locked.add(xkey)
    for ykey, _ in y_values:
        locked.add(ykey)

    available = set([])
    for (_, _, _, output) in gates:
        if output not in locked:
            available.add(output)

    return (expected_result, locked, available)

def find_remaining_pairs_to_swap(initial_values, initial_gates, expected, locked, available, num_pairs, swap_pairs=None):
    if swap_pairs is None:
        swap_pairs = []

    copied_values = copy.deepcopy(initial_values)
    copied_gates = copy.deepcopy(initial_gates)
    copied_locked = copy.deepcopy(locked)
    copied_available = copy.deepcopy(available)
    copied_swap_pairs = copy.deepcopy(swap_pairs)

    for pair in copied_swap_pairs:
        copied_gates = swap_outputs(copied_gates, pair)
        for output in pair:
            copied_locked.add(output)
            copied_available.remove(output)
    apply_all_gates(copied_values, copied_gates)

    z_bin = as_binary_string(get_all_z(copied_values))

    # base case - we're done
    if len(copied_swap_pairs) == num_pairs:
        if expected == z_bin:
            return copied_swap_pairs
        else:
            return

    # check each z until we find one we need to fix
    z_to_fix = None
    z_values = sorted([(zkey, val) for zkey, val in get_all_z(copied_values) if zkey in available])
    print(z_values)

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

        gates.pop(i)
        i = 0

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

def binary_addition(x_val, y_val):
    return bin(int(x_val, 2) + int(y_val, 2))[2:]

def swap_outputs(gates, combo):
    for i, (command, x, y, output) in enumerate(gates):
        if output not in combo:
            continue
        if output == combo[0]:
            swapped_gate = (command, x, y, combo[1])
        else:
            swapped_gate = (command, x, y, combo[0])
        gates[i] = swapped_gate
    return gates

if __name__ == '__main__':
    with open('24/day_24_test_part2.txt', 'r') as f:
        contents = f.read()

    num_pairs = 2

    values, gates = parse_input(contents)
    expected, locked, available = setup(values, gates)

    find_remaining_pairs_to_swap(values, gates, expected, locked, available, num_pairs)
