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

def get_route(map_object):
    map = map_object['map']
    route = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if is_on_route(map, i, j):
                route.append((i, j))

    scores = map_object['scores']
    return sorted(route, key=lambda point: scores[point])

def is_on_route(map, i, j):
    return is_empty_tile(map, i, j) or is_start(map, i, j) or is_end(map, i, j)

def is_start(map, i, j):
    return is_in_map(map, i, j) and map[i][j] == 'S'

def is_end(map, i, j):
    return is_in_map(map, i, j) and map[i][j] == 'E'

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
                row.append('  #')
            else:
                score_string = str(scores[(i, j)])
                if len(score_string) == 3:
                    row.append(score_string)
                if len(score_string) == 2:
                    row.append(' ' + score_string)
                if len(score_string) == 1:
                    row.append('  ' + score_string)
        print(''.join(row))

def num_cheats(scores, route, max_distance, min_picoseconds):
    total = 0
    for start in route:
        for end in route:
            if is_valid_cheat(scores, start, end, max_distance, min_picoseconds):
                total += 1
    return total

def is_valid_cheat(scores, start, end, max_distance, min_picoseconds):
    distance = calculate_distance(start, end)
    return distance <= max_distance and calculate_cheat_code_score(scores, start, end, distance) >= min_picoseconds

def calculate_distance(start, end):
    return abs(end[0] - start[0]) + abs(end[1] - start[1])

def calculate_cheat_code_score(scores, start, end, distance):
    return scores[end] - scores[start] - distance

if __name__ == '__main__':
    with open('20/day_20_input.txt', 'r') as f:
        contents = f.read()

    map_object = make_map_object(contents)
    print_map(map_object['map'])
    print()
    set_scores(map_object)
    print_map_with_scores(map_object['map'], map_object['scores'])
    print()

    # constants to be updated for test vs. input
    max_distance = 20
    min_picoseconds = 100

    route = get_route(map_object)

    print(num_cheats(map_object['scores'], route, max_distance, min_picoseconds))
