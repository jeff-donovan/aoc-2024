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
def find_all_sequences(code):
    seq_num_to_dir = numerical_to_direction(code)

    seq_dir_to_dir = []
    min_length = None
    for seq in seq_num_to_dir:
        new_paths = directional_to_directional(seq)
        first_path_length = len(new_paths[0])
        if min_length is None or first_path_length < min_length:
            min_length = first_path_length

        for path in new_paths:
            if len(path) <= min_length:
                seq_dir_to_dir.append(path)
    # seq_dir_to_dir = [path for path in seq_dir_to_dir if len(path) == calculate_min_path_length(seq_dir_to_dir)]

    final_seq = []
    min_length = None
    for seq in seq_dir_to_dir:
        # final_seq.extend(directional_to_directional(seq))
        new_paths = directional_to_directional(seq)
        first_path_length = len(new_paths[0])
        if min_length is None or first_path_length < min_length:
            min_length = first_path_length

        for path in new_paths:
            if len(path) <= min_length:
                final_seq.append(path)
    # final_seq = [path for path in final_seq if len(path) == calculate_min_path_length(final_seq)]

    return final_seq

def find_a_shortest_sequence(code):
    seq_num_to_dir = numerical_to_direction(code)

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
    with open('21/day_21_input.txt', 'r') as f:
        contents = f.read()

    codes = make_codes(contents)

    start = datetime.datetime.now()
    print(sum([calculate_complexity(code, find_all_sequences(code)) for code in codes]))
    print('took ', datetime.datetime.now() - start)

    # print(numerical_to_direction('029A'))
    # for result in numerical_to_direction('029A'):

    #     print(f'{len(result)}: ', result)

    # for result in directional_to_directional(['<', 'A', '^', 'A', '^', '^', '>', 'A', 'v', 'v', 'v', 'A']):
    # for result in directional_to_directional(['<', 'A', '^', 'A', '^', '>', '^', 'A', 'v', 'v', 'v', 'A']):
    # for result in directional_to_directional(['<', 'A', '^', 'A', '>', '^', '^', 'A', 'v', 'v', 'v', 'A']):
    # # for result in [first_result, second_result, third_result]:
    #     print(f'{len(result)}: ', result)
    #     print()