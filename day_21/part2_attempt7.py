import copy
import datetime
import itertools
import math
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

def find_shortest_path_length_for_code(cache, numerical_paths, code, max_depth):
    depth_0 = numerical_to_direction(numerical_paths, code)
    return min(path_length(cache, seq, max_depth) for seq in depth_0)

def path_length(cache, seq, max_depth):
    if max_depth == 0:
        return len(seq)

    string_depth = math.ceil(max_depth / 2)
    parts = split_by_A(seq)
    for _ in range(string_depth):
        parts = (next_string(cache, s) for s in parts)

    remaining_depth = max_depth - string_depth
    return sum(path_length(cache, s, remaining_depth) for p in parts for s in split_by_A(p))

def find_shortest_path_length_recursive(directional_paths, group_by_A_paths, seq, current_depth, max_depth):
    if current_depth == max_depth:
        return len(seq)

    total = 0
    for s in group_by_A(seq):
        next_sequences = directional_to_directional(directional_paths, group_by_A_paths, s)
        total += min(find_shortest_path_length_recursive(directional_paths, group_by_A_paths, ns, current_depth + 1, max_depth) for ns in next_sequences)

    return total

def next_string(cache, seq):
    if seq in cache:
        return cache[seq]

    left, right = split_by_A(seq)
    cache[seq] = next_string(cache, left) + next_string(cache, right)
    return cache[seq]

def split_by_A(seq):
    a_indices = [i for i, char in enumerate(seq) if char == 'A']
    num_a_indices = len(a_indices)
    if num_a_indices < 2:
        return [seq]

    split_index = a_indices[num_a_indices // 2 - 1]
    first_half = seq[0:split_index + 1]
    second_half = seq[split_index + 1:len(seq)]
    return [first_half, second_half]

def group_by_A(seq):
    a_indices = [i for i, char in enumerate(seq) if char == 'A']
    new_sequences = []
    start = 0
    for a_index in a_indices:
        new_sequences.append(seq[start : a_index + 1])
        start = a_index + 1
    return new_sequences

def pre_compute_group_by_A_winners(directional_paths, group_by_A_paths):
    max_depth = 1
    winners = {}
    for a_seq, depth_0 in group_by_A_paths.items():
        shortest_path_lengths = [find_shortest_path_length_recursive(directional_paths, group_by_A_paths, seq, 0, max_depth) for seq in depth_0]
        winners[a_seq] = next(seq for i, seq in enumerate(depth_0) if shortest_path_lengths[i] == min(shortest_path_lengths))
    return winners

def pre_compute_group_by_A_paths(numerical_paths, directional_paths):
    group_by_A_sequences = set([])
    for sequences in numerical_paths.values():
        group_by_A_sequences = group_by_A_sequences.union(set(sequences))
    for sequences in directional_paths.values():
        group_by_A_sequences = group_by_A_sequences.union(set(sequences))
    return {seq: directional_to_directional(directional_paths, {}, seq) for seq in group_by_A_sequences}

def directional_to_directional(directional_paths, group_by_A_paths, directional_seq):
    if directional_seq in group_by_A_paths:
        return group_by_A_paths[directional_seq]

    sequences = ['']
    for i in range(len(directional_seq)):
        if i == 0:
            start = 'A'
        else:
            start = directional_seq[i - 1]
        end = directional_seq[i]
        paths = directional_paths[(start, end)]  # leverage pre-computed paths
        new_sequences = []
        for path in paths:
            for seq in sequences:
                new_sequences.append(seq + path)
        sequences = new_sequences
    return tidy_up(sequences)  # TODO: maybe we shouldn't tidy

def numerical_to_direction(numerical_paths, code):
    sequences = ['']
    for i in range(len(code)):
        if i == 0:
            start = 'A'
        else:
            start = code[i - 1]
        end = code[i]
        paths = numerical_paths[(start, end)]
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

def calculate_complexity(code, min_path_length):
    return min_path_length * int(code[:len(code) - 1])

if __name__ == '__main__':
    with open('day_21/day_21_input.txt', 'r') as f:
        contents = f.read()

    start = datetime.datetime.now()
    codes = make_codes(contents)
    numerical_paths = pre_compute_keypad_paths(NUMERICAL_KEYPAD)
    directional_paths = pre_compute_keypad_paths(DIRECTIONAL_KEYPAD)
    group_by_A_paths = pre_compute_group_by_A_paths(numerical_paths, directional_paths)
    group_by_A_winners = pre_compute_group_by_A_winners(directional_paths, group_by_A_paths)

    depth = 13
    cache = copy.deepcopy(group_by_A_winners)

    print(sum([calculate_complexity(code, find_shortest_path_length_for_code(cache, numerical_paths, code, depth)) for code in codes]))

    print('took ', datetime.datetime.now() - start)
