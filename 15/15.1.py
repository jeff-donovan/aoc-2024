def make_map_and_moves(contents):
    map_contents, move_contents = contents.split('\n\n')
    map = []
    for line in map_contents.split('\n'):
        if line:
            map_row = []
            for char in line:
                map_row.append(char)
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
    return move(map, i, j, next_i, next_j, direction)

def move(map, current_i, current_j, next_i, next_j, direction):
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
    move(map, next_i, next_j, next_next_i, next_next_j, direction)

    if is_empty_space(map, next_i, next_j):
        current_object = map[current_i][current_j]
        map[next_i][next_j] = current_object
        map[current_i][current_j] = '.'
        return

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

def is_box(map, i, j):
    return is_in_map(map, i, j) and map[i][j] == 'O'

def is_wall(map, i, j):
    return is_in_map(map, i, j) and map[i][j] == '#'

def is_empty_space(map, i, j):
    return is_in_map(map, i, j) and map[i][j] == '.'

def is_in_map(map, i, j):
    return (0 <= i < len(map)) and (0 <= j < len(map[i]))

def get_all_boxes(map):
    boxes = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if is_box(map, i, j):
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

    num = sum([get_box_gps_coordinate(box) for box in get_all_boxes(map)])
    print(num)
