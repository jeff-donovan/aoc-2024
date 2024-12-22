import pprint


NUMERICAL_KEYPAD = {
    'A': {
        'up': '3',
        'left': '0',
    },
    '0': {
        'up': '2',
        'right': 'A',
    },
    '1': {
        'up': '4',
        'right': '2',
    },
    '2': {
        'up': '5',
        'down': '0',
        'left': '1',
        'right': '3',
    },
    '3': {
        'up': '6',
        'down': 'A',
        'left': '2',
    },
    '4': {
        'up': '7',
        'down': '1',
        'right': '5',
    },
    '5': {
        'up': '8',
        'down': '2',
        'left': '4',
        'right': '6',
    },
    '6': {
        'up': '9',
        'down': '3',
        'left': '5',
    },
    '7': {
        'down': '4',
        'right': '8',
    },
    '8': {
        'down': '5',
        'left': '7',
        'right': '9',
    },
    '9': {
        'down': '6',
        'left': '8',
    },
}

DIRECTIONAL_KEYPAD = {
    'A': {
        'left': '^',
        'down': '>'
    },
    '^': {
        'right': 'A',
        'down': 'v',
    },
    '<': {
        'right': 'v',
    },
    '>': {
        'left': 'v',
        'up': 'A'
    },
    'v': {
        'left': '<',
        'right': '>',
        'up': '^',
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
        return []

    for direction, destination in keypad[start_char].items():
        if destination == end_char:
            return [[direction]]

    paths = []
    for direction, next_start_char in keypad[start_char].items():
        next_paths = [[direction] + path for path in find_shortest_paths(keypad, next_start_char, end_char, visited + [start_char])]
        paths += next_paths

    return [path for path in paths if len(path) == calculate_min_path_length(paths)]

def calculate_min_path_length(paths):
    if len(paths) == 0:
        return 0
    return min([len(path) for path in paths])

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
