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

if __name__ == '__main__':
    with open('C:/code/aoc-2024/24/day_24_test_part2.txt', 'r') as f:
        contents = f.read()

    values, gates = parse_input(contents)
