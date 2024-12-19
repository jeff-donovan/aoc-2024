import copy


def make_map_object(contents, max_x_y):
    map_object = {
        'map': [],
        'bytes': [],
        'start': (0, 0),
        'end': (max_x_y, max_x_y),
        'scores': {}
    }

    for _ in range(max_x_y + 1):
        map_row = []
        for _ in range(max_x_y + 1):
            map_row.append('.')
        map_object['map'].append(map_row)

    for line in contents.split('\n'):
        if line:
            x, y = line.split(',')
            i, j = int(y), int(x)  # x/y maps to j/i indexes when accessing list elements
            map_object['bytes'].append((i, j))

    return map_object

def add_bytes_to_map(map_object, num_bytes):
    for i, j in map_object['bytes'][0:num_bytes]:
        map_object['map'][i][j] = '#'

def travel(map_object):
    i, j = map_object['start']

    points_to_travel = [(i, j, 0)]
    while points_to_travel:
        i, j, score = points_to_travel.pop()

        is_new_route = False
        if (i, j) not in map_object['scores']:
            is_new_route = True
            map_object['scores'][(i, j)] = score

        # base case - we have reached the end
        if (i, j) == map_object['end']:
            if score < map_object['scores'][(i, j)]:
                map_object['scores'][(i, j)] = score
            continue

        # base case - we have previously found a better route
        if score > map_object['scores'][(i, j)]:
            continue

        # base case - we have already calculated this route
        if not is_new_route and score == map_object['scores'][(i, j)]:
            continue

        # now we know this is definitely a new route
        map_object['scores'][(i, j)] = score

        for next_i, next_j in get_next_coords(i, j):
            if is_empty_tile(map_object['map'], next_i, next_j):
                points_to_travel.append((next_i, next_j, score + 1))

def get_next_coords(i, j):
    return [
        (i - 1, j),  # up
        (i + 1, j),  # down
        (i, j - 1),  # left
        (i, j + 1),  # right
    ]
    
def is_empty_tile(map, i, j):
    return is_in_map(map, i, j) and map[i][j] == '.'

def is_in_map(map, i, j):
    return (0 <= i < len(map)) and (0 <= j < len(map[i]))

def print_map(map):
    for row in map:
        print(''.join(row))

def binary_search(initial_map_object):
    low = 0
    high = len(initial_map_object['bytes']) - 1

    while low < high:
        bytes_index = low + (high - low) // 2
        map_object = copy.deepcopy(initial_map_object)
        add_bytes_to_map(map_object, bytes_index)
        travel(map_object)
        end_i, end_j = map_object['end']

        try:
            print(f'bytes_index: {bytes_index} | {map_object["scores"][(end_i, end_j)]}')
            # if we find a valid path, we know byte is later in the list
            low = bytes_index + 1
        except:
            # if we're here then we _could be_ at the correct index
            high = bytes_index - 1

    # low must equal high, which means we've found the index
    print('low: ', low)
    print('high: ', high)
    return low

if __name__ == '__main__':
    with open('18/day_18_input.txt', 'r') as f:
        contents = f.read()

    max_x_y = 70
    initial_map_object = make_map_object(contents, max_x_y)
    bytes_index = binary_search(initial_map_object)
    print('SOLUTION BYTES INDEX! ', bytes_index)
    i, j = initial_map_object['bytes'][bytes_index]
    print('SOLUTION! ', (j, i))

    # sanity check
    for num_bytes in [bytes_index - 1, bytes_index, bytes_index + 1]:
        map_object = copy.deepcopy(initial_map_object)
        add_bytes_to_map(map_object, num_bytes)
        travel(map_object)
        end_i, end_j = map_object['end']

        print()
        if (end_i, end_j) in map_object["scores"]:
            print('SUCCESS: ', (num_bytes))
        else:
            print('FAIL: ', num_bytes)

        success_i, success_j = map_object['bytes'][num_bytes]
        print('coordinate: ', map_object['bytes'][num_bytes])
        print('character: ', map_object['map'][success_i][success_j])
