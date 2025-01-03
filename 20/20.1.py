import pprint


def make_map_object(contents):
    map_object = {
        'map': [],
        'start': (),
        'end': (),
        'scores': {}
    }

    for line in contents.split('\n'):
        if line:
            row = []
            for char in line:
                row.append(char)
            map_object['map'].append(row)

    map_object['start'] = find_start(map_object['map'])
    map_object['end'] = find_end(map_object['map'])

    return map_object

def find_start(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 'S':
                return (i, j)

def find_end(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 'E':
                return (i, j)

def set_scores(map_object):
    i, j = map_object['start']
    score = 0

    while True:
        if (i, j) not in map_object['scores']:
            map_object['scores'][(i, j)] = score
        if (i, j) == map_object['end']:
            break
        i, j = next_coord(map_object, i, j)
        score += 1

def next_coord(map_object, i, j):
    possible_next_coords = [
        (i - 1, j),  # up
        (i + 1, j),  # down
        (i, j - 1),  # left
        (i, j + 1),  # right
    ]

    for next_i, next_j in possible_next_coords:
        can_visit = is_empty_tile(map_object['map'], next_i, next_j) or map_object['end'] == (next_i, next_j)
        if can_visit and has_not_been_visited(map_object['scores'], next_i, next_j):
            return (next_i, next_j)

def has_not_been_visited(scores, i, j):
    return (i, j) not in scores

def is_start_or_end(map, i, j):
    return is_start(map, i, j) or is_end(map, i, j)

def is_start(map, i, j):
    return is_in_map(map, i, j) and map[i][j] == 'S'

def is_end(map, i, j):
    return is_in_map(map, i, j) and map[i][j] == 'E'

def is_wall(map, i, j):
    return is_in_map(map, i, j) and map[i][j] == '#'

def is_empty_tile(map, i, j):
    return is_in_map(map, i, j) and map[i][j] == '.'

def is_in_map(map, i, j):
    return (0 <= i < len(map)) and (0 <= j < len(map[i]))

def print_map(map):
    for row in map:
        print(''.join(row))

def print_map_with_scores(map, scores):
    for i in range(len(map)):
        row = []
        for j in range(len(map[i])):
            if map[i][j] == '#':
                row.append('#')
            else:
                row.append(str(scores[(i, j)]))
        print(''.join(row))

def group_by_cheat_code_score(cheat_coords_with_scores):
    mapping = {}
    for coord, score in cheat_coords_with_scores:
        if score not in mapping:
            mapping[score] = set([])
        mapping[score].add(coord)
    return mapping

def get_all_valid_cheat_coords(map_object):
    map = map_object['map']
    scores = map_object['scores']
    walls = get_all_walls(map)
    walls_with_cheat_codes = []
    for wall in walls:
        cheat_code_score = get_cheat_coord_score(map, scores, wall[0], wall[1])
        if cheat_code_score is not None and cheat_code_score > 0:
            walls_with_cheat_codes.append((wall, cheat_code_score))
    return walls_with_cheat_codes

def get_cheat_coord_score(map, scores, i, j):
    vertical = get_vertical_coords(map, i, j)
    horizontal = get_horizontal_coords(map, i, j)

    if all([is_empty_tile(map, coord[0], coord[1]) or is_start_or_end(map, coord[0], coord[1]) for coord in vertical]):
        return get_diff(scores, vertical[0], vertical[1]) - 2

    if all([is_empty_tile(map, coord[0], coord[1]) or is_start_or_end(map, coord[0], coord[1]) for coord in horizontal]):
        return get_diff(scores, horizontal[0], horizontal[1]) - 2

def get_diff(scores, coord1, coord2):
    return abs(scores[coord1] - scores[coord2])

def get_vertical_coords(map, i, j):
    return [
        (i - 1, j),  # up
        (i + 1, j),  # down
    ]

def get_horizontal_coords(map, i, j):
    return [
        (i, j - 1),  # left
        (i, j + 1),  # right
    ]

def get_all_walls(map):
    walls = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if is_wall(map, i, j):
                walls.append((i, j))
    return walls

if __name__ == '__main__':
    with open('20/day_20_input.txt', 'r') as f:
        contents = f.read()

    map_object = make_map_object(contents)
    print_map(map_object['map'])
    print()
    set_scores(map_object)
    print_map_with_scores(map_object['map'], map_object['scores'])
    # pprint.pprint(sorted(get_all_valid_cheat_coords(map_object), key=lambda x: x[1]))
    cheat_coords_with_scores = get_all_valid_cheat_coords(map_object)
    grouped = group_by_cheat_code_score(cheat_coords_with_scores)
    pprint.pprint({score: len(grouped[score]) for score in grouped})

    print(sum([len(grouped[score]) for score in grouped if score >= 100]))
