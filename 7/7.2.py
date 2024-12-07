'''
--- Part Two ---
The engineers seem concerned; the total calibration result you gave them is nowhere close to being within safety tolerances. Just then, you spot your mistake: some well-hidden elephants are holding a third type of operator.

The concatenation operator (||) combines the digits from its left and right inputs into a single number. For example, 12 || 345 would become 12345. All operators are still evaluated left-to-right.

Now, apart from the three equations that could be made true using only addition and multiplication, the above example has three more equations that can be made true by inserting operators:

156: 15 6 can be made true through a single concatenation: 15 || 6 = 156.
7290: 6 8 6 15 can be made true using 6 * 8 || 6 * 15.
192: 17 8 14 can be made true using 17 || 8 + 14.
Adding up all six test values (the three that could be made before using only + and * plus the new three that can now be made by also using ||) produces the new total calibration result of 11387.

Using your new knowledge of elephant hiding spots, determine which equations could possibly be true. What is their total calibration result?
'''


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
            continue

        if i == len_numbers - 1:
            break

        new_combos = []
        for combo in combos:
            new_combos.append(combo + ['add',])
            new_combos.append(combo + ['multiply',])
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
