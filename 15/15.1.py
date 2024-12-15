def make_map_and_moves(contents):
    map = []
    moves = []
    return map, moves

def attempt_move(map, move):
    pass

def can_move(map, next_i, next_j, direction):
    if not is_in_map(map, next_i, next_j):
        return False

    if is_wall(map, next_i, next_j):
        return False

    if is_empty_space(map, next_i, next_j):
        return True

    next_i, next_j = get_next_coords(i, j, direction)
    return can_move(map, next_i, next_j, direction)

def get_next_coords(i, j, direction):
    if direction == '^':
        return (i - 1, j)
    if direction == 'v':
        return (i + 1, j)
    if direction == '<':
        return (i, j - 1)
    if direction == '>':
        return (i, j + 1)

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

def get_box_gps_coordinate(i, j):
    return 100 * i + j

if __name__ == '__main__':
    with open('15/day_15_test.txt', 'r') as f:
        contents = f.read()

    map, moves = make_map_and_moves(contents)
    for move in moves:
        attempt_move(map, move)

    num = sum([get_box_gps_coordinate(box) for box in get_all_boxes(map)])
    print(num)
