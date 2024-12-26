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

def get_all_x_keys(values):
    return sorted([key for key in values.keys() if key.startswith('x')])

def get_all_y_keys(values):
    return sorted([key for key in values.keys() if key.startswith('y')])

if __name__ == '__main__':
    with open('C:/code/aoc-2024/24/day_24_test_part2.txt', 'r') as f:
        contents = f.read()

    values, gates = parse_input(contents)
    print(len(get_all_values_combos(values)))
