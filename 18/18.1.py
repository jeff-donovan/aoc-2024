def make_map_object(contents, max_x_y, num_bytes):
    map_object = {
        'map': [],
        'start': (0, 0),
        'end': (max_x_y, max_x_y),
        'scores': {}
    }

    for _ in range(max_x_y + 1):
        map_row = []
        for _ in range(max_x_y + 1):
            map_row.append('.')
        map_object['map'].append(map_row)

    for byte, line in enumerate(contents.split('\n')):
        if byte >= num_bytes:
            break
        if line:
            x, y = line.split(',')
            i, j = int(y), int(x)  # x/y maps to j/i indexes when accessing list elements
            map_object['map'][i][j] = '#'

    return map_object

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

if __name__ == '__main__':
    with open('18/day_18_input.txt', 'r') as f:
        contents = f.read()

    max_x_y = 70
    num_bytes = 1024
    map_object = make_map_object(contents, max_x_y, num_bytes)
    print_map(map_object['map'])

    travel(map_object)

    end_i, end_j = map_object['end']
    print(map_object['scores'][(end_i, end_j)])
