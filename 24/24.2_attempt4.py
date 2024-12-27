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

def get_xy_inputs(gates, output):
    gate = next((gate for gate in gates if gate[-1] == output), None)

    # base case - we have found x/y
    if gate is None:
        return set([output])

    (_, x, y, _) = gate
    return get_xy_inputs(gates, x) | get_xy_inputs(gates, y)

def get_all_z_keys(gates):
    return sorted([gate[-1] for gate in gates if gate[-1].startswith('z')])

if __name__ == '__main__':
    with open('C:/code/aoc-2024/24/day_24_input.txt', 'r') as f:
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
