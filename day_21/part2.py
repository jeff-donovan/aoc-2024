import copy
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
    return min([len(path) for path in paths])

def find_all_sequences(cache, code, depth):
    sequences = numerical_to_direction(code)

    for current_depth in range(depth):
        new_sequences = []
        for seq in sequences:
            new_paths = directional_to_directional_using_group_by_A(cache, seq)
            new_sequences.extend(new_paths)

        sequences = tidy_up(new_sequences)

        combo_lengths = {}
        for combo in sequences:
            if len(combo) not in combo_lengths:
                combo_lengths[len(combo)] = 0
            combo_lengths[len(combo)] += 1
        # print(f'depth {current_depth} - ', combo_lengths)

    # pprint.pprint(cache)

    return sequences

def find_shortest_sequences(cache, code, depth):
    sequences = tidy_up(numerical_to_direction(code))

    for _ in range(depth):
        new_sequences = [directional_to_directional_shortest(cache, seq) for seq in sequences]
        sequences = tidy_up(new_sequences)

    return sequences

def directional_to_directional_shortest(cache, seq):
    next_seq = []
    for a_seq in group_by_A(seq):
        next_seq.extend(shortest_d_to_d(cache, a_seq))
    return next_seq

def directional_to_directional_using_group_by_A(cache, seq):
    # TODO: figure out where to add to the cache - think we need to make sure that we re-use calculations (especially in the "winner" method) otherwise we'll go nuts
    directional_to_directional_split = [directional_to_directional(a_seq) for a_seq in group_by_A(seq)]
    combos = [[]]
    for split in directional_to_directional_split:
        new_combos = []
        for path in split:
            for combo in combos:
                new_combo = copy.deepcopy(combo)
                new_combo.extend(path)
                new_combos.append(new_combo)
        combos = new_combos
    return combos

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

def tidy_up(sequences):
    min_length = calculate_min_path_length(sequences)
    return [seq for seq in sequences if len(seq) == min_length]

def shortest_d_to_d(cache, seq):
    # pprint.pprint(cache)
    cache_key = tuple(seq)
    if cache_key in cache:
        return cache[cache_key]

    next_sequences = tidy_up(directional_to_directional_using_group_by_A(cache, seq))

    seq_lengths = [{0: [sequence]} for sequence in next_sequences]
    depth = 0
    while _get_winner_index(seq_lengths) is None:
        if depth >= 1:
            break
        max_level = max([max(seq_tree.keys()) for seq_tree in seq_lengths if len(seq_tree.keys()) > 0])
        # print('max_level: ', max_level)
        _remove_losers(seq_lengths, max_level)
        # _tidy_up_winners(seq_lengths, max_level)  # TODO: might not need this
        for i, seq_tree in enumerate(seq_lengths):
            if max_level not in seq_tree:
                continue
            # print(f'{i} @ {max_level} = {calculate_min_path_length(seq_tree[max_level])}')
            new_sequences = []
            for seq in seq_tree[max_level]:
                new_paths = directional_to_directional_using_group_by_A(cache, seq)
                new_sequences.extend(new_paths)

            seq_tree[max_level + 1] = tidy_up(new_sequences)
        depth += 1
    winner_index = _get_winner_index(seq_lengths)
    if winner_index is None:
        # print('hi jeff! winner is NONE')
        max_level = max([max(seq_tree.keys()) for seq_tree in seq_lengths if len(seq_tree.keys()) > 0])
        _remove_losers(seq_lengths, max_level)
        winner_index = next((i for i, seq_tree in enumerate(seq_lengths) if len(seq_tree.keys()) > 0))
    cache[cache_key] = next_sequences[winner_index]
    return cache[cache_key]

def _remove_losers(seq_lengths, max_level):
    shortest_path_length = None
    for sequence_tree in seq_lengths:
        if max_level not in sequence_tree:
            continue

        min_length = calculate_min_path_length(sequence_tree[max_level])
        if shortest_path_length is None or min_length < shortest_path_length:
            shortest_path_length = min_length

    for i, sequence_tree in enumerate(seq_lengths):
        if max_level not in sequence_tree:
            seq_lengths[i] = {}

        min_length = calculate_min_path_length(sequence_tree[max_level])
        if min_length > shortest_path_length:
            seq_lengths[i] = {}

def _tidy_up_winners(seq_lengths, max_level):
    shortest_path_length = None
    for sequence_tree in seq_lengths:
        if max_level not in sequence_tree:
            continue

        sequence_tree[max_level] = tidy_up(sequence_tree[max_level])

def _get_winner_index(seq_lengths):
    max_level = max([max(seq_tree.keys()) for seq_tree in seq_lengths if len(seq_tree.keys()) > 0])
    shortest_path_length = None
    sequences_with_shortest_path = []
    for i, sequence_tree in enumerate(seq_lengths):
        if max_level not in sequence_tree:
            continue

        min_length = calculate_min_path_length(sequence_tree[max_level])
        if shortest_path_length is None:
            shortest_path_length = min_length

        if min_length == shortest_path_length:
            sequences_with_shortest_path.append(i)

        if min_length < shortest_path_length:
            shortest_path_length = min_length
            sequences_with_shortest_path = [i]

    if len(sequences_with_shortest_path) == 1:
        return sequences_with_shortest_path[0]

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
    with open('day_21/day_21_input.txt', 'r') as f:
        contents = f.read()

    codes = make_codes(contents)

    start = datetime.datetime.now()
    depth = 15
    cache = {}

    print(sum([calculate_complexity(code, find_shortest_sequences(cache, code, depth)) for code in codes]))
    # print(find_shortest_sequences(cache, '029A', 1))
    print('took ', datetime.datetime.now() - start)
