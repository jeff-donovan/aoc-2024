def make_map_and_moves(contents):
    map_contents, move_contents = contents.split('\n\n')
    map = []
    for line in map_contents.split('\n'):
        if line:
            map_row = []
            for char in line:
                if char == '@':
                    map_row.append('@')
                    map_row.append('.')

                if char == 'O':
                    map_row.append('[')
                    map_row.append(']')

                if char == '#':
                    map_row.append('#')
                    map_row.append('#')

                if char == '.':
                    map_row.append('.')
                    map_row.append('.')

            map.append(map_row)

    moves = []
    for line in move_contents.split('\n'):
        if line:
            for char in line:
                moves.append(char)

    return map, moves

def attempt_move(map, direction):
    i, j = get_robot_coords(map)
    next_i, next_j = get_next_coords(i, j, direction)
    if is_direction_vertical(direction):
        return move_vertical(map, i, j, next_i, next_j, direction)
    return move_horizontal(map, i, j, next_i, next_j, direction)

def move_horizontal(map, current_i, current_j, next_i, next_j, direction):
    if not is_in_map(map, next_i, next_j):
        return

    if is_wall(map, next_i, next_j):
        return

    if is_empty_space(map, next_i, next_j):
        current_object = map[current_i][current_j]
        map[next_i][next_j] = current_object
        map[current_i][current_j] = '.'
        return

    next_next_i, next_next_j = get_next_coords(next_i, next_j, direction)
    move_horizontal(map, next_i, next_j, next_next_i, next_next_j, direction)

    if is_empty_space(map, next_i, next_j):
        current_object = map[current_i][current_j]
        map[next_i][next_j] = current_object
        map[current_i][current_j] = '.'
        return

def move_vertical(map, current_i, current_j, next_i, next_j, direction):
    if not can_move_vertical(map, next_i, next_j, direction):
        return

    if is_empty_space(map, next_i, next_j):
        current_object = map[current_i][current_j]
        map[next_i][next_j] = current_object
        map[current_i][current_j] = '.'
        return

    # otherwise it's a box!
    next_box_coords = get_box_coords(map, next_i, next_j)
    next_next_box_coords = [get_next_coords(i, j, direction) for i, j in next_box_coords]
    move_vertical(map, next_box_coords[0][0], next_box_coords[0][1], next_next_box_coords[0][0], next_next_box_coords[0][1], direction)
    move_vertical(map, next_box_coords[1][0], next_box_coords[1][1], next_next_box_coords[1][0], next_next_box_coords[1][1], direction)

    if is_empty_space(map, next_i, next_j):
        current_object = map[current_i][current_j]
        map[next_i][next_j] = current_object
        map[current_i][current_j] = '.'
        return

def can_move_vertical(map, next_i, next_j, direction):
    if not is_in_map(map, next_i, next_j):
        return False

    if is_wall(map, next_i, next_j):
        return False

    if is_empty_space(map, next_i, next_j):
        return True

    # otherwise it's a box!
    next_box_coords = [get_next_coords(i, j, direction) for i, j in get_box_coords(map, next_i, next_j)]
    return (
        can_move_vertical(map, next_box_coords[0][0], next_box_coords[0][1], direction)
        and
        can_move_vertical(map, next_box_coords[1][0], next_box_coords[1][1], direction)
    )

def is_direction_horizontal(direction):
    return direction in ('<', '>')

def is_direction_vertical(direction):
    return direction in ('^', 'v')

def get_box_coords(map, i, j):
    if is_left_box(map, i, j):
        return [(i, j), (i, j + 1)]
    return [(i, j), (i, j - 1)]

def get_next_coords(i, j, direction):
    if direction == '^':
        return (i - 1, j)
    if direction == 'v':
        return (i + 1, j)
    if direction == '<':
        return (i, j - 1)
    if direction == '>':
        return (i, j + 1)

def get_robot_coords(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if is_robot(map, i, j):
                return (i, j)

def is_robot(map, i, j):
    return is_in_map(map, i, j) and map[i][j] == '@'

def is_left_box(map, i, j):
    return is_in_map(map, i, j) and map[i][j] == '['

def is_right_box(map, i, j):
    return is_in_map(map, i, j) and map[i][j] == ']'

def is_wall(map, i, j):
    return is_in_map(map, i, j) and map[i][j] == '#'

def is_empty_space(map, i, j):
    return is_in_map(map, i, j) and map[i][j] == '.'

def is_in_map(map, i, j):
    return (0 <= i < len(map)) and (0 <= j < len(map[i]))

def get_all_left_boxes(map):
    boxes = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if is_left_box(map, i, j):
                boxes.append((i, j))
    return boxes

def get_box_gps_coordinate(box):
    i, j = box
    return 100 * i + j

def print_map(map):
    for row in map:
        print(''.join(row))

if __name__ == '__main__':
    with open('15/day_15_input.txt', 'r') as f:
        contents = f.read()

    map, moves = make_map_and_moves(contents)
    # print('INITIAL MAP:')
    # print_map(map)
    for direction in moves:
        # print(direction)
        # if input('Do You Want To Continue? ') == 'n':
        #     break
        attempt_move(map, direction)
        # print_map(map)
    # print_map(map)

    num = sum([get_box_gps_coordinate(box) for box in get_all_left_boxes(map)])
    print(num)
