import datetime


NUMERICAL_KEYPAD = {
    'A': {
        '^': '3',
        '<': '0',
    },
    '0': {
        '^': '2',
        '>': 'A',
    },
    '1': {
        '^': '4',
        '>': '2',
    },
    '2': {
        '^': '5',
        'v': '0',
        '<': '1',
        '>': '3',
    },
    '3': {
        '^': '6',
        'v': 'A',
        '<': '2',
    },
    '4': {
        '^': '7',
        'v': '1',
        '>': '5',
    },
    '5': {
        '^': '8',
        'v': '2',
        '<': '4',
        '>': '6',
    },
    '6': {
        '^': '9',
        'v': '3',
        '<': '5',
    },
    '7': {
        'v': '4',
        '>': '8',
    },
    '8': {
        'v': '5',
        '<': '7',
        '>': '9',
    },
    '9': {
        'v': '6',
        '<': '8',
    },
}

DIRECTIONAL_KEYPAD = {
    'A': {
        '<': '^',
        'v': '>'
    },
    '^': {
        '>': 'A',
        'v': 'v',
    },
    '<': {
        '>': 'v',
    },
    '>': {
        '<': 'v',
        '^': 'A'
    },
    'v': {
        '<': '<',
        '>': '>',
        '^': '^',
    },
}

def make_codes(contents):
    return [line for line in contents.split('\n') if line]

def find_shortest_paths(keypad, start_char, end_char, visited=None):
    if visited is None:
        visited = []

    if start_char in visited:
        return []

    if start_char == end_char:
        return [['A']]

    paths = []
    for direction, next_start_char in keypad[start_char].items():
        next_paths = [[direction] + path for path in find_shortest_paths(keypad, next_start_char, end_char, visited + [start_char])]
        paths += next_paths

    return [path for path in paths if len(path) == calculate_min_path_length(paths)]

def calculate_min_path_length(paths):
    if len(paths) == 0:
        return 0
    return min([len(path) for path in paths])

# update algorithm logic to keep track of min sequence length at each depth
# only fan out for sequences with the min sequence length
def find_all_sequences(code, depth):
    sequences = numerical_to_direction(code)

    for _ in range(depth):
        new_sequences = []
        for seq in sequences:
            new_paths = directional_transformation(seq)
            new_sequences.extend(new_paths)

        sequences = tidy_up(new_sequences)

    return sequences

def group_by_A(seq):
    a_indices = [i for i, char in enumerate(seq) if char == 'A']
    new_sequences = []
    start = 0
    for a_index in a_indices:
        new_sequences.append(seq[start : a_index + 1])
        start = a_index + 1
    return new_sequences

def numerical_to_direction(code):
    sequences = [[]]
    for i in range(len(code)):
        if i == 0:
            start = 'A'
        else:
            start = code[i - 1]
        end = code[i]
        paths = find_shortest_paths(NUMERICAL_KEYPAD, start, end)
        new_sequences = []
        for path in paths:
            for seq in sequences:
                new_sequences.append(seq + path)
        sequences = new_sequences
    return sequences

def directional_transformation(seq):
    # for group in group_by_A(seq):
    #     print(directional_to_directional(group))
    possible_sequences = directional_to_directional(seq)
    print(len(possible_sequences[0]))
    # return tidy_up(possible_sequences)

def combine(a, b):
    combos = []
    for a_elem in a:
        for b_elem in b:
            combos.append(a_elem + b_elem)
    return combos

def tidy_up(sequences):
    min_length = calculate_min_path_length(sequences)
    return [seq for seq in sequences if len(seq) == min_length]

def directional_to_directional(directional_seq):
    sequences = [[]]
    for i in range(len(directional_seq)):
        if i == 0:
            start = 'A'
        else:
            start = directional_seq[i - 1]
        end = directional_seq[i]
        paths = find_shortest_paths(DIRECTIONAL_KEYPAD, start, end)
        new_sequences = []
        for path in paths:
            for seq in sequences:
                new_sequences.append(seq + path)
        sequences = new_sequences
    return sequences

def calculate_complexity(code, sequences):
    return calculate_min_path_length(sequences) * int(code[:len(code) - 1])

if __name__ == '__main__':
    with open('21/day_21_test.txt', 'r') as f:
        contents = f.read()

    codes = make_codes(contents)

    # numerical_transform = ['<', 'A', '^', 'A', '>', '^', '^', 'A', 'v', 'v', 'v', 'A']
    # final = []
    # for group in group_by_A(['<', 'A', '^', 'A', '>', '^', '^', 'A', 'v', 'v', 'v', 'A']):
    #     first_dir_transform = directional_transformation(group)
    #     second_dir_transform = directional_transformation(first_dir_transform)
    #     final.extend(second_dir_transform)
    # print(len(final), final)

    # for group in group_by_A(['<', 'A', '^', 'A', '>', '^', '^', 'A', 'v', 'v', 'v', 'A']):
    #     print(f'group {group} -> {directional_to_directional(group)[0]}')

    # jeff = []
    # [jeff.extend(directional_to_directional(group)[0]) for group in group_by_A(['<', 'A', '^', 'A', '>', '^', '^', 'A', 'v', 'v', 'v', 'A'])]
    # print(f'{len(jeff)} - {jeff}')

    # jeff2 = []
    # [jeff2.extend(directional_to_directional(group)[0]) for group in group_by_A(jeff)]
    # print(f'{len(jeff2)} - {jeff2}')

    start = datetime.datetime.now()
    depth = 1
    print(sum([calculate_complexity(code, find_all_sequences(code, depth)) for code in codes]))
    print('took ', datetime.datetime.now() - start)
    # code = '029A'
    # for depth in range(10):
    #     print(f'{depth} - ', calculate_min_path_length(find_all_sequences(code, depth)))
    #     print('took ', datetime.datetime.now() - start)
    #     print()

# IDEAS:
#  - find all repeated subsequences within a sequence
#    - somehow group these together to minimize re-calculations
#    - build the next depth
#  - **CHECK THIS ONE OUT TOMORROW** rather than find repeated subsequences, use the 'A' to split the sequence up
#  - is this a math problem where we don't need to generate all combos, and instead can calculate size of smallest combo with a formula?
