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

def get_all_inputs_for_output(gates, output):
    gate = next((gate for gate in gates if gate[-1] == output), None)

    if gate is None:
        raise Exception('oops! messed up recursion')

    # base case - we have found x/y gate
    (_, x, y, _) = gate
    if x.startswith('x') or x.startswith('y'):
        return set([x, y, output])

    return set([x, y]) | get_all_inputs_for_output(gates, x) | get_all_inputs_for_output(gates, y)

def get_xy_inputs(gates, output):
    gate = next((gate for gate in gates if gate[-1] == output), None)

    # base case - we have found x/y
    if gate is None:
        return set([output])

    (_, x, y, _) = gate
    return get_xy_inputs(gates, x) | get_xy_inputs(gates, y)

def get_xy_gates(gates, output):
    gate = next((gate for gate in gates if gate[-1] == output), None)

    if gate is None:
        raise Exception('oops! messed up recursion')

    # base case - we have found x/y gate
    (_, x, y, _) = gate
    if x.startswith('x') or x.startswith('y'):
        return set([gate])

    return get_xy_gates(gates, x) | get_xy_gates(gates, y)

def is_xy_xor_gate(gate, z_key):
    number = z_key[1:]
    (command, x, y, z) = gate
    return command == 'XOR' and x.endswith(number) and y.endswith(number)

def get_all_z_keys(gates):
    return sorted([gate[-1] for gate in gates if gate[-1].startswith('z')])

def get_all_outputs(gates):
    return sorted([gate[-1] for gate in gates])

if __name__ == '__main__':
    with open('C:/code/aoc-2024/24/day_24_edit_input.txt', 'r') as f:
        contents = f.read()

    values, gates = parse_input(contents)

    # check for any obvious z switches
    for z_key in get_all_z_keys(gates):
        inputs = get_xy_inputs(gates, z_key)
        z_index = int(z_key[1:])
        for input in inputs:
            if int(input[1:]) > z_index:
                print(z_key)

    # check for any x/y mismatches
    for (_, x, y, output) in gates:
        if (x.startswith('x') or y.startswith('x')):
            if not (x.startswith('y') or y.startswith('y')):
                print(output)
            if x[1:] != y[1:]:
                print(output)

    # sort z, number of inputs to check for a pattern
    print(sorted([(z_key, len(get_xy_inputs(gates, z_key))) for z_key in get_all_z_keys(gates)]))
    print()

    # sort outputs, number of inputs to check for a pattern
    print(sorted([(output, len(get_xy_inputs(gates, output))) for output in get_all_outputs(gates)], key=lambda x: x[1]))
    print()

    pattern = []
    for z_key in get_all_z_keys(gates):
        z_num = len(get_xy_inputs(gates, z_key))
        gate = next((gate for gate in gates if gate[-1] == z_key), None)
        (command, x, y, z) = gate
        x_num = len(get_xy_inputs(gates, x))
        y_num = len(get_xy_inputs(gates, y))
        if x_num > y_num:
            pattern.append(((z_key, z_num), (x, x_num), (y, y_num)))
        elif x_num == y_num:
            x_tup, y_tup = sorted([(x, x_num), (y, y_num)])
            pattern.append(((z_key, z_num), x_tup, y_tup))
        else:  # y_num > x_num
            pattern.append(((z_key, z_num), (y, y_num), (x, x_num)))
    pprint.pprint(pattern)
    print()

    # check for num of each x/y pair
    xy_pairs = {}
    for (_, x, y, _) in gates:
        if (x.startswith('x') or y.startswith('x')):
            x_key = x if x.startswith('x') else y
            y_key = y if y.startswith('y') else x
            if (x_key, y_key) not in xy_pairs:
                xy_pairs[(x_key, y_key)] = 0
            xy_pairs[(x_key, y_key)] += 1
    pprint.pprint(sorted(xy_pairs.items()))
    print()

    for z_key in get_all_z_keys(gates):
        print(f'{z_key}: ', any([is_xy_xor_gate(gate, z_key) for gate in get_xy_gates(gates, z_key)]))
    print()

    # grab all outputs not used in z keys
    outputs = set(get_all_outputs(gates))
    outputs_used = set([])
    for z_key in get_all_z_keys(gates):
        outputs_used = outputs_used | get_all_inputs_for_output(gates, z_key)
    print(sorted([output for output in outputs if output not in outputs_used]))
    print()

    # different approach to outputs not used in z keys
    outputs = set(get_all_outputs(gates))
    z_variables = set([])
    for (_, x, y, z) in gates:
        if z.startswith('z'):
            z_variables.add(x)
            z_variables.add(y)
            z_variables.add(z)
    print(sorted([output for output in outputs if output not in z_variables]))
    print()

    # check if each z command is XOR
    z_commands = []
    for (command, x, y, z) in gates:
        if z.startswith('z') and command != 'XOR':
            z_commands.append((z, command))
    pprint.pprint(sorted(z_commands))
    print()
