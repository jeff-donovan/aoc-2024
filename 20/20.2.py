import pprint


def make_map_object(contents):
    map_object = {
        'map': [],
        'start': (),
        'end': (),
        'scores': {},
        'cheat_scores': {},
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

def cheat_code_travel(map_object, cheat_coord):
    i, j = cheat_coord
    if len(get_adjacent_empty_tiles(map_object['map'], i, j)) == 0:
        return

    if cheat_coord not in map_object['cheat_scores']:
        map_object['cheat_scores'][cheat_coord] = {}

    points_to_travel = [(i, j, 1)]
    while points_to_travel:
        i, j, distance_traveled = points_to_travel.pop()

        # if is_wall(): keep going (as long as distance_traveled does not become 21)
        # if is_empty_tile() or start or end: calculate score, DONE

        if is_wall(map_object['map'], i, j) and distance_traveled < 20:
            for next_i, next_j in get_next_coords(i, j):
                if is_in_map(map_object['map'], next_i, next_j):
                    points_to_travel.append((next_i, next_j, distance_traveled + 1))

        if is_empty_tile(map_object['map'], i, j) or is_start_or_end(map_object['map'], i, j):
            if (i, j) not in map_object['cheat_scores'][cheat_coord]:
                map_object['cheat_scores'][cheat_coord][(i, j)] = 0

            current_cheat_score = map_object['cheat_scores'][cheat_coord][(i, j)]
            new_cheat_score = calculate_cheat_code_score(map_object['map'], map_object['scores'], cheat_coord, i, j, distance_traveled)
            if new_cheat_score > current_cheat_score:
                map_object['cheat_scores'][cheat_coord][(i, j)] = new_cheat_score

def get_next_coords(i, j):
    return [
        (i - 1, j),  # up
        (i + 1, j),  # down
        (i, j - 1),  # left
        (i, j + 1),  # right
    ]

def get_all_connecting_empty_tiles_and_distances(map, cheat_coord):
    i, j = cheat_coord

    distances = {}
    points_to_travel = [i, j, 0]
    while points_to_travel:
        i, j, distance = points_to_travel.pop()

        is_new_route = False
        if (i, j) not in distances:
            is_new_route = True
            distances[(i, j)] = distance

        # base case - we have reached an empty or start/end
        if is_empty_tile(map, i, j) or is_start_or_end(map, i, j):
            if distance < distances[(i, j)]:
                distances[(i, j)] = distance
            continue

        # base case - we have previously found a better route
        if distance > distances[(i, j)]:
            continue

        # base case - we have already calculated this route
        if not is_new_route and distance == distances[(i, j)]:
            continue

        # definitely a new route
        distances[(i, j)] = distance

        for next_i, next_j in get_next_coords(i, j):
            if is_in_map(map, next_i, next_j) and distance:
                points_to_travel.append((next_i, next_j, distance + 1))

    return {coord: distances[coord] for coord in distances if (is_empty_tile(map, coord[0], coord[1]) or is_start_or_end(map, coord[0], coord[1]))}

def group_by_cheat_code_score(cheat_coords_with_scores):
    mapping = {}
    for start, end, score in cheat_coords_with_scores:
        if score not in mapping:
            mapping[score] = set([])
        mapping[score].add((start, end))
    return mapping

def get_all_valid_cheat_coords(map_object):
    for wall in get_all_walls(map_object['map']):
        cheat_code_travel(map_object, wall)

    cheat_codes = []
    for cheat_start in map_object['cheat_scores']:
        for cheat_end in map_object['cheat_scores'][cheat_start]:
            cheat_code_score = map_object['cheat_scores'][cheat_start][cheat_end]
            cheat_codes.append((cheat_start, cheat_end, cheat_code_score))
    return cheat_codes

def calculate_cheat_code_score(map, scores, cheat_coord, i, j, distance_traveled):
    best_score = 0
    for start in get_adjacent_empty_tiles(map, cheat_coord[0], cheat_coord[1]):
        score = get_diff(scores, start, (i, j)) - distance_traveled
        if score > best_score:
            best_score = score
    return best_score

def get_adjacent_empty_tiles(map, i, j):
    adjacent_empty = []
    for next_i, next_j in get_next_coords(i, j):
        if is_empty_tile(map, next_i, next_j) or is_start_or_end(map, next_i, next_j):  # TODO: consider only including start, not end
            adjacent_empty.append((next_i, next_j))
    return adjacent_empty

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
    with open('20/day_20_test.txt', 'r') as f:
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

    # print(sum([len(grouped[score]) for score in grouped if score >= 100]))
