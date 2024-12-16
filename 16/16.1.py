def make_map(contents):
    map = []
    for line in contents.split('\n'):
        if line:
            map_row = []
            for char in line:
                map_row.append(char)
            map.append(map_row)
    return map

# visited should be *set* of all (i, j, direction) combos
# and then have a mapping where we store the "score" of a point/direction. if we get there with a lower score then we update the score. eventually we must get to the final point and have the lowest score.

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

def is_empty_space(map, i, j):
    return is_in_map(map, i, j) and map[i][j] == '.'

def is_in_map(map, i, j):
    return (0 <= i < len(map)) and (0 <= j < len(map[i]))

def print_map(map):
    for row in map:
        print(''.join(row))

if __name__ == '__main__':
    with open('16/day_16_test_1.txt', 'r') as f:
        contents = f.read()

    map = make_map(contents)
    print_map(map)
