def make_map_object(contents):
    map_object = {
        'map': [],
        'start': (),
        'end': (),
        'scores': {}
    }

    for line in contents.split('\n'):
        if line:
            map_row = []
            for char in line:
                map_row.append(char)
            map_object['map'].append(map_row)

    map_object['start'] = find_start(map_object['map'])
    map_object['end'] = find_end(map_object['map'])

    return map_object

# visited should be *set* of all (i, j, direction) combos
# and then have a mapping where we store the "score" of a point/direction. if we get there with a lower score then we update the score. eventually we must get to the final point and have the lowest score.

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

def travel(map_object):
    i, j = map_object['start']
    direction = 'right'
    score = 0

    point_directions_to_travel = [(i, j, direction, score)]
    while point_directions_to_travel:
        i, j, direction, score = point_directions_to_travel.pop()

        is_new_route = False
        if (i, j, direction) not in map_object['scores']:
            is_new_route = True
            map_object['scores'][(i, j, direction)] = score

        # base case - we have reached the end
        if (i, j) == map_object['end']:
            if score < map_object['scores'][(i, j, direction)]:
                map_object['scores'][(i, j, direction)] = score
            continue

        # base case - we have previously found a better route
        if score > map_object['scores'][(i, j, direction)]:
            continue

        # base case - we have already calculated this route
        if not is_new_route and score == map_object['scores'][(i, j, direction)]:
            continue

        # now we know this is definitely a new route
        map_object['scores'][(i, j, direction)] = score

        if can_move_forward(map_object['map'], i, j, direction):
            next_i, next_j = get_next_coords(i, j, direction)
            point_directions_to_travel.append((next_i, next_j, direction, score + 1))

        for next_direction in [turn_clockwise(direction), turn_counterclockwise(direction)]:
            point_directions_to_travel.append((i, j, next_direction, score + 1000))

def can_move_forward(map, i, j, direction):
    next_i, next_j = get_next_coords(i, j, direction)
    return not is_wall(map, next_i, next_j)

def get_next_coords(i, j, direction):
    if direction == 'up':
        return (i - 1, j)
    if direction == 'down':
        return (i + 1, j)
    if direction == 'left':
        return (i, j - 1)
    if direction == 'right':
        return (i, j + 1)
    

def turn_clockwise(current_direction):
    if current_direction == 'right':
        return 'down'
    if current_direction == 'down':
        return 'left'
    if current_direction == 'left':
        return 'up'
    if current_direction == 'up':
        return 'right'

def turn_counterclockwise(current_direction):
    if current_direction == 'right':
        return 'up'
    if current_direction == 'up':
        return 'left'
    if current_direction == 'left':
        return 'down'
    if current_direction == 'down':
        return 'right'

def is_wall(map, i, j):
    return is_in_map(map, i, j) and map[i][j] == '#'

def is_empty_tile(map, i, j):
    return is_in_map(map, i, j) and map[i][j] == '.'

def is_in_map(map, i, j):
    return (0 <= i < len(map)) and (0 <= j < len(map[i]))

def print_map(map):
    for row in map:
        print(''.join(row))

if __name__ == '__main__':
    with open('16/day_16_input.txt', 'r') as f:
        contents = f.read()

    map_object = make_map_object(contents)
    print_map(map_object['map'])

    travel(map_object)

    end_i, end_j = map_object['end']
    scores = []
    for end_direction in ['up', 'down', 'right', 'left']:
        if (end_i, end_j, end_direction) in map_object['scores']:
            scores.append(map_object['scores'][(end_i, end_j, end_direction)])
    print(min(scores))
