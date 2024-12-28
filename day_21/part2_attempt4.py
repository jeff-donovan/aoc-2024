import datetime
import itertools


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

def numerical_to_direction(cache, code, start=None):
    sequences = ['']
    for i in range(len(code)):
        if start is None:
            if i == 0:
                start = 'A'
            else:
                start = code[i - 1]
        end = code[i]
        paths = find_shortest_paths(cache, NUMERICAL_KEYPAD, start, end)
        new_sequences = []
        for path in paths:
            for seq in sequences:
                new_sequences.append(seq + path)
        sequences = new_sequences
    return [sequences[0]]

def directional_to_directional(cache, seq):
    cache_key = ('directional_to_directional', seq)
    if cache_key in cache:
        return cache[cache_key]

    parts = split_by_A(seq)
    if len(parts) == 1:
        cache[cache_key] = _directional_to_directional(cache, seq)
        return cache[cache_key]

    left, right = parts
    cache[cache_key] = [''.join(prod) for prod in itertools.product(*[directional_to_directional(cache, left), directional_to_directional(cache, right)])]
    return cache[cache_key]

def _directional_to_directional(cache, directional_seq):
    sequences = ['']
    for i in range(len(directional_seq)):
        if i == 0:
            start = 'A'
        else:
            start = directional_seq[i - 1]
        end = directional_seq[i]
        paths = find_shortest_paths(cache, DIRECTIONAL_KEYPAD, start, end)
        new_sequences = []
        for path in paths:
            for seq in sequences:
                new_sequences.append(seq + path)
        sequences = new_sequences
    return [sequences[0]]

def split_by_A(seq):
    a_indices = [i for i, char in enumerate(seq) if char == 'A']
    num_a_indices = len(a_indices)
    if num_a_indices == 1:
        return [seq]

    split_index = a_indices[num_a_indices // 2 - 1]
    first_half = seq[0:split_index + 1]
    second_half = seq[split_index + 1:len(seq)]
    return [first_half, second_half]

def find_shortest_paths(cache, keypad, start_char, end_char):
    cache_key = start_char + end_char
    if cache_key not in cache:
        cache[cache_key] = _find_shortest_paths(keypad, start_char, end_char)
    return cache[cache_key]

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

def calculate_complexity(code, sequences):
    return calculate_min_path_length(sequences) * int(code[:len(code) - 1])

def calculate_min_path_length(paths):
    return min([len(path) for path in paths])

# def tidy_up(sequences):
#     min_length = calculate_min_path_length(sequences)
#     return [seq for seq in sequences if len(seq) == min_length]

if __name__ == '__main__':
    with open('day_21/day_21_input.txt', 'r') as f:
        contents = f.read()

    codes = make_codes(contents)

    depth = 13
    cache = {}
    start = datetime.datetime.now()
    complexities = []
    for code in codes:
        code_char_lengths = []
        for i, char in enumerate(code):
            if i == 0:
                start_char = 'A'
            else:
                start_char = code[i - 1]
            # sequences = tidy_up(numerical_to_direction(cache, char, start_char))
            sequences = numerical_to_direction(cache, char, start_char)
            for _ in range(depth):
                new_sequences = []
                for seq in sequences:
                    new_sequences.extend(directional_to_directional(cache, seq))
                # sequences = tidy_up(new_sequences)
                sequences = new_sequences
            code_char_lengths.append(calculate_min_path_length(sequences))
        complexities.append(sum(code_char_lengths) * int(code[:len(code) - 1]))
    print(sum(complexities))
    print('took ', datetime.datetime.now() - start)
    print()
