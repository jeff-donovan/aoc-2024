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

def setup(values, gates, expected_fn):
    x_values = get_all_x(values)
    y_values = get_all_y(values)

    expected_result = expected_fn(x_values, y_values)

    print('x_values: ', x_values)
    print('y_values: ', y_values)
    print('expected_result: ', expected_result)

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

def find_remaining_pairs_to_swap(initial_values, initial_gates, expected, locked, available, num_pairs, checked=None, swap_pairs=None):
    # we want to pass around the same checked to all function calls
    if checked is None:
        checked = set([])

    if swap_pairs is None:
        swap_pairs = []

    # exit if we've already checked that this is false (from a different pair ordering)
    checked_key = sort_for_checked(swap_pairs)
    if checked_key in checked:
        return

    copied_values = copy.deepcopy(initial_values)
    copied_gates = copy.deepcopy(initial_gates)
    copied_locked = copy.deepcopy(locked)
    copied_available = copy.deepcopy(available)
    copied_swap_pairs = copy.deepcopy(swap_pairs)

    for pair in copied_swap_pairs:
        copied_gates = swap_outputs(copied_gates, pair)
        for output in pair:
            copied_locked.add(output)
            if output in copied_available:
                copied_available.remove(output)
    try:
        apply_all_gates(copied_values, copied_gates)
    except:
        checked.add(checked_key)
        return  # this path doesn't lead anywhere

    z_bin = as_binary_string(get_all_z(copied_values))

    # base case - we're done
    if len(copied_swap_pairs) == num_pairs:
        if expected == z_bin:
            return copied_swap_pairs
        else:
            checked.add(checked_key)
            return

    # base case - we don't have any other keys to check - this path was incorrect
    if len(copied_available) == 0:
        checked.add(checked_key)
        return

    # check each z until we find one we need to fix
    z_to_fix = None
    z_values = [(zkey, val) for zkey, val in get_all_z(copied_values, reverse=False) if zkey in copied_available]
    for zkey, zval in z_values:
        expected_index = int(zkey[1:])
        if zval == expected[expected_index]:
            add_output_recursively_to_locked(copied_gates, copied_locked, copied_available, zkey)
        else:
            z_to_fix = zkey
            break

    # base case - we've already supposedly fixed this z
    if z_to_fix in locked:
        checked.add(checked_key)
        return

    possible_swaps = get_possible_output_swaps(copied_gates, z_to_fix)
    for remaining_output in possible_swaps:
        if remaining_output in copied_available:
            new_pair = tuple(sorted((z_to_fix, remaining_output)))
            pairs = find_remaining_pairs_to_swap(initial_values, initial_gates, expected, copied_locked, copied_available, num_pairs, checked, copied_swap_pairs + [new_pair])
            if pairs is not None and len(pairs) == num_pairs:
                # TODO: check result before returning
                return pairs

def get_possible_output_swaps(gates, output):
    gate = next((gate for gate in gates if gate[-1] == output), None)
    if gate is None:
        return set([])

    swaps = set([])
    (command, x, y, z) = gate

    number = None
    if z.startswith('z'):
        number = z[1:]
    x_number = None
    y_number = None
    if number is not None:
        x_number = 'x' + number
        y_number = 'y' + number

    for possible_swap_gate in gates:
        # consider same x/y
        (swap_command, swap_x, swap_y, swap_z) = possible_swap_gate
        if (x == swap_x) or (x == swap_y):
            if z != swap_z:
                swaps.add(swap_z)

        if (y == swap_x) or (y == swap_y):
            if z != swap_z:
                swaps.add(swap_z)

        # consider x00/y00 inputs when output is z00
        if (x_number == swap_x) or (x_number == swap_y):
            if z != swap_z:
                swaps.add(swap_z)

        if (y_number == swap_x) or (y_number == swap_y):
            if z != swap_z:
                swaps.add(swap_z)

    return swaps

def sort_for_checked(pairs):
    final = []
    for pair in pairs:
        sorted_pair = tuple(sorted(pair))
        final.append(sorted_pair)
    return tuple(sorted(final))

def add_output_recursively_to_locked(gates, locked, available, output):
    if output in locked:
        return

    locked.add(output)
    available.remove(output)
    for (_, x, y, z) in gates:
        if z == output:
            add_output_recursively_to_locked(gates, locked, available, x)
            add_output_recursively_to_locked(gates, locked, available, y)

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

def binary_addition(x_values, y_values):
    return bin(as_decimal(x_values) + as_decimal(y_values))[2:]

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
    with open('C:/code/aoc-2024/24/day_24_test_part2.txt', 'r') as f:
        contents = f.read()

    num_pairs = 2
    system_function = bitwise_and

    values, gates = parse_input(contents)
    print(get_possible_output_swaps(gates, 'z05'))
    expected, locked, available = setup(values, gates, system_function)

    pairs = find_remaining_pairs_to_swap(values, gates, expected, locked, available, num_pairs)
    print(pairs)
    outputs = []
    for pair in pairs:
        outputs.extend(list(pair))
    print(','.join(sorted(outputs)))

    # TODO:
    # - i don't actually check if the updated system works for all X/Y values
    # - i say that because running it for the test produces two answers: z00,z01,z02,z05 and z00,z01,z04,z05
