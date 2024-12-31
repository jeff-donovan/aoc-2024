import datetime
import pprint


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

def pre_compute_group_by_A_paths(numericalPaths, directionalPaths):
    group_by_A_sequences = set([])
    for sequences in numericalPaths.values():
        group_by_A_sequences = group_by_A_sequences.union(set(sequences))
    for sequences in directionalPaths.values():
        group_by_A_sequences = group_by_A_sequences.union(set(sequences))
    return {seq: _directional_to_directional(directionalPaths, seq) for seq in group_by_A_sequences}

def _directional_to_directional(directionalPaths, directional_seq):
    sequences = ['']
    for i in range(len(directional_seq)):
        if i == 0:
            start = 'A'
        else:
            start = directional_seq[i - 1]
        end = directional_seq[i]
        paths = directionalPaths[(start, end)]  # leverage pre-computed paths
        new_sequences = []
        for path in paths:
            for seq in sequences:
                new_sequences.append(seq + path)
        sequences = new_sequences
    return tidy_up(sequences)  # TODO: maybe we shouldn't tidy

def tidy_up(sequences):
    min_length = calculate_min_path_length(sequences)
    return [seq for seq in sequences if len(seq) == min_length]

def pre_compute_keypad_paths(keypad):
    paths = {}
    for start in keypad.keys():
        for end in keypad.keys():
            paths[(start, end)] = _find_shortest_paths(keypad, start, end)
    return paths

def _find_shortest_paths(keypad, start_char, end_char, visited=None):
    if visited is None:
        visited = []

    if start_char in visited:
        return []

    if start_char == end_char:
        return ['A']

    paths = []
    for direction, next_start_char in keypad[start_char].items():
        next_paths = [direction + path for path in _find_shortest_paths(keypad, next_start_char, end_char, visited + [start_char])]
        paths += next_paths

    return [path for path in paths if len(path) == calculate_min_path_length(paths)]

def calculate_min_path_length(paths):
    return min([len(path) for path in paths])

if __name__ == '__main__':
    with open('day_21/day_21_input.txt', 'r') as f:
        contents = f.read()

    start = datetime.datetime.now()
    codes = make_codes(contents)
    numericalPaths = pre_compute_keypad_paths(NUMERICAL_KEYPAD)
    pprint.pprint(numericalPaths)
    print()
    directionalPaths = pre_compute_keypad_paths(DIRECTIONAL_KEYPAD)
    pprint.pprint(directionalPaths)
    print()
    groupByAPaths = pre_compute_group_by_A_paths(numericalPaths, directionalPaths)
    pprint.pprint(groupByAPaths)
    print()
    print('took ', datetime.datetime.now() - start)
