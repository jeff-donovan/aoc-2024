def make_mapping(contents):
    mapping = []
    for line in contents.split('\n'):
        if line:
            test_value, numbers = line.split(': ')
            mapping.append((int(test_value), [int(n) for n in numbers.split(' ')]))
    return mapping

def make_operator_combos(len_numbers):
    combos = []
    for i in range(len_numbers):
        if i == 0:
            combos.append(['add',])
            combos.append(['multiply',])
            combos.append(['concat',])
            continue

        if i == len_numbers - 1:
            break

        new_combos = []
        for combo in combos:
            new_combos.append(combo + ['add',])
            new_combos.append(combo + ['multiply',])
            new_combos.append(combo + ['concat',])
        combos = new_combos

    return combos

def calculate_combo_total(numbers, operator_combo):
    total = numbers[0]
    for i in range(len(operator_combo)):
        operator = operator_combo[i]
        number = numbers[i + 1]
        if operator == 'add':
            total += number
        if operator == 'multiply':
            total = total * number
        if operator == 'concat':
            total = int(str(total) + str(number))
    return total

def can_numbers_produce_test_value(test_value, numbers):
    combos = make_operator_combos(len(numbers))
    for combo in combos:
        if test_value == calculate_combo_total(numbers, combo):
            return True
    return False

def get_total_calibration(mapping):
    num = 0
    for test_value, numbers in mapping:
        if can_numbers_produce_test_value(test_value, numbers):
            num += test_value
    return num


if __name__ == '__main__':
    with open('7/day_7_input.txt', 'r') as f:
        contents = f.read()

    mapping = make_mapping(contents)
    num = get_total_calibration(mapping)
    print(num)
