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

if __name__ == '__main__':
    with open('24/day_24_test_part2.txt', 'r') as f:
        contents = f.read()

    values, gates = parse_input(contents)
    print('values: ', values)
    print('gates: ', gates)

    apply_all_gates(values, gates)
    print('values after: ', values)

    x_vals = get_all_x(values)
    y_vals = get_all_y(values)
    z_vals = get_all_z(values)
    print('x: ', as_decimal(x_vals))
    print('y: ', as_decimal(y_vals))
    print('z: ', as_decimal(z_vals))
