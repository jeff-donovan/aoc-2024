def get_num_positions_to_obstruct(matrix):
    initial_position = get_initial_position(matrix)
    initial_obstacles = get_obstacles(matrix)

    num_positions = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if ((i, j) != initial_position) and ((i, j) not in initial_obstacles):
                new_obstacles = initial_obstacles.copy()
                new_obstacles.add((i, j))
                if is_loop_route(matrix, new_obstacles):
                    num_positions += 1

    return num_positions

def is_loop_route(matrix, obstacles):
    print('inside is_loop_route')
    direction_i, direction_j = (-1, 0)  # up
    current_i, current_j = get_initial_position(matrix)

    route = set([])  # tuples - (i, j, direction_i, direction_j)
    while is_on_map(matrix, current_i, current_j):
        position_direction = (current_i, current_j, direction_i, direction_j)
        if position_direction in route:
            return True

        route.add(position_direction)

        # traverse the map
        next_i = current_i + direction_i
        next_j = current_j + direction_j

        while is_obstacle(obstacles, next_i, next_j):
            direction_i, direction_j = change_direction(direction_i, direction_j)
            next_i = current_i + direction_i
            next_j = current_j + direction_j

        current_i = next_i
        current_j = next_j

    return False

def is_safe(matrix, obstacles, i, j):
    return is_on_map(matrix, i, j) and not is_obstacle(obstacles, i, j)

def is_obstacle(obstacles, i, j):
    return (i, j) in obstacles

def is_on_map(matrix, i, j):
    return (0 <= i < len(matrix)) and (0 <= j < len(matrix[i]))

def get_obstacles(matrix):
    obstacles = set([])
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == '#':
                obstacles.add((i, j))
    return obstacles

def get_initial_position(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == '^':
                return (i, j)

def make_matrix(contents):
    return [row for row in contents.split('\n') if row]

def change_direction(old_direction_i, old_direction_j):
    if old_direction_i == 1:  # down
        return (0, -1)  # go left

    if old_direction_i == -1:  # up
        return (0, 1)  # go right

    if old_direction_j == 1:  # right
        return (1, 0)  # go down

    if old_direction_j == -1:  # left
        return (-1, 0)  # go up


if __name__ == '__main__':
    with open('6/day_6_input.txt', 'r') as f:
        contents = f.read()

    matrix = make_matrix(contents)
    num = get_num_positions_to_obstruct(matrix)
    print(num)
