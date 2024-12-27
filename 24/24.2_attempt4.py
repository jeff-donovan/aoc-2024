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
    for z_key in get_all_z_keys(gates):
        print(z_key, get_xy_inputs(gates, z_key))
