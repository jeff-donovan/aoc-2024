def make_machines(contents):
    machines = []
    new_machine = True
    for line in contents.split('\n'):
        if line == '':
            new_machine = True
            continue

        if new_machine:
            new_machine = False
            machines.append({})

        machine = machines[-1]
        if 'Button A' in line:
            coefficients = line.split('Button A: ')[1].split(', ')
            x_coefficient = coefficients[0][2:]
            y_coefficient = coefficients[1][2:]
            machine['A'] = (int(x_coefficient), int(y_coefficient))

        if 'Button B' in line:
            coefficients = line.split('Button B: ')[1].split(', ')
            x_coefficient = coefficients[0][2:]
            y_coefficient = coefficients[1][2:]
            machine['B'] = (int(x_coefficient), int(y_coefficient))

        if 'Prize' in line:
            coords = line.split('Prize: ')[1].split(', ')
            x_coord = coords[0][2:]
            y_coord = coords[1][2:]
            machine['Prize'] = (int(x_coord), int(y_coord))

    return machines

def combo_cost(a, b):
    return 3 * a + b

def find_combo(machine):
    def evaluate(a, b):
        return (
            (a * machine['A'][0] + b * machine['B'][0] == machine['Prize'][0]) and
            (a * machine['A'][1] + b * machine['B'][1] == machine['Prize'][1])
        )

    for a in range(0, 101):
        for b in range(0, 101):
            if evaluate(a, b):
                return (a, b)

if __name__ == '__main__':
    with open('13/day_13_input.txt', 'r') as f:
        contents = f.read()

    machines = make_machines(contents)

    total = 0
    for machine in machines:
        combo = find_combo(machine)
        if combo is not None:
            total += combo_cost(combo[0], combo[1])
    print(total)
