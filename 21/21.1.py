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
    return [[char for char in line] for line in contents.split('\n') if line]

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

if __name__ == '__main__':
    with open('21/day_21_input.txt', 'r') as f:
        contents = f.read()

    codes = make_codes(contents)
    pprint.pprint(codes)

    print('NUMERICAL_KEYPAD')
    for start_char in NUMERICAL_KEYPAD:
        for end_char in NUMERICAL_KEYPAD:
            shortest_paths = find_shortest_paths(NUMERICAL_KEYPAD, start_char, end_char)
            print(f'{start_char} to {end_char}: {shortest_paths}')

    print('DIRECTIONAL_KEYPAD')
    for start_char in DIRECTIONAL_KEYPAD:
        for end_char in DIRECTIONAL_KEYPAD:
            shortest_paths = find_shortest_paths(DIRECTIONAL_KEYPAD, start_char, end_char)
            print(f'{start_char} to {end_char}: {shortest_paths}')

    print(numerical_to_direction('029A'))
