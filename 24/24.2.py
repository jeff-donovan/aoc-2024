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

def apply_all_gates(values, gates):
    i = 0
    while len(gates) > 0:
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

def get_all_x(values):
    return sorted([(key, val) for key, val in values.items() if key.startswith('x')], key=lambda x: x[0], reverse=True)

def get_all_y(values):
    return sorted([(key, val) for key, val in values.items() if key.startswith('y')], key=lambda y: y[0], reverse=True)

def get_all_z(values):
    return sorted([(key, val) for key, val in values.items() if key.startswith('z')], key=lambda z: z[0], reverse=True)

def get_output_swap_combos(gates, num_swap_pairs):
    # first - get all pairs
    pairs = set([])
    for i in gates:
        for j in gates:
            i_output = i[3]
            j_output = j[3]
            if i_output != j_output:
                pairs.add(tuple(sorted([i_output, j_output])))

    combos = list(itertools.combinations(pairs, num_swap_pairs))
    print('combos: ', combos)

    # since itertools.combinations() does not care if z00 is used across multiple pairs within a combo, we have to remove invalid combos where this occurs
    final = []
    for combo in combos:
        if is_valid_combo(combo):
            final.append(combo)
    return final

def is_valid_combo(combo):
    outputs = set([])
    for pair in combo:
        if pair[0] in outputs or pair[1] in outputs:
            return False
        outputs.add(pair[0])
        outputs.add(pair[1])
    return True

def is_valid_addition(values):
    x_vals = get_all_x(values)
    y_vals = get_all_y(values)
    z_vals = get_all_z(values)
    print(f'{as_binary_string(x_vals)} + {as_binary_string(y_vals)} = {as_binary_string(z_vals)}')
    print(f'{as_decimal(x_vals)} + {as_decimal(y_vals)} = {as_decimal(z_vals)}')
    print('(as_decimal(x_vals) + as_decimal(y_vals)): ', (as_decimal(x_vals) + as_decimal(y_vals)))
    print('as_decimal(z_vals): ', as_decimal(z_vals))
    return binary_addition(as_binary_string(x_vals), as_binary_string(y_vals)) == as_binary_string(z_vals)

def binary_addition(x_val, y_val):
    return bin(int(x_val, 2) + int(y_val, 2))[2:]

def swap_outputs(gates, combo):
    for pair in combo:
        for i, (command, x, y, output) in enumerate(gates):
            if output not in pair:
                continue
            if output == pair[0]:
                swapped_gate = (command, x, y, pair[1])
            else:
                swapped_gate = (command, x, y, pair[0])
            gates[i] = swapped_gate
    return gates

if __name__ == '__main__':
    with open('24/day_24_test_part2.txt', 'r') as f:
        contents = f.read()

    values, gates = parse_input(contents)

    num_swap_pairs = 2
    swap_combos = get_output_swap_combos(gates, num_swap_pairs)
    print('swap_combos: ', swap_combos)
    for combo in swap_combos:
        print()
        print('combo: ', combo)
        combo_values = copy.deepcopy(values)
        combo_gates = swap_outputs(copy.deepcopy(gates), combo)
        print('combo_values: ', combo_values)
        print('gates: ', gates)
        print('combo_gates: ', combo_gates)
        apply_all_gates(combo_values, combo_gates)
        print('values after: ', combo_values)
        if is_valid_addition(combo_values):
            outputs = []
            for pair in combo:
                outputs.append(pair[0])
                outputs.append(pair[1])
            print(','.join(sorted(outputs)))
            break
