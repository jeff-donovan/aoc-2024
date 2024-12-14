def get_num_positions_visited(matrix):
    obstacles = get_obstacles(matrix)

    direction = (-1, 0)  # up
    current_i, current_j = get_initial_position(matrix)

    positions_visited = set([])
    while is_on_map(matrix, current_i, current_j):
        positions_visited.add((current_i, current_j))

        # traverse the map
        next_i = current_i + direction[0]
        next_j = current_j + direction[1]

        while is_obstacle(obstacles, next_i, next_j):
            direction = change_direction(direction[0], direction[1])
            next_i = current_i + direction[0]
            next_j = current_j + direction[1]

        current_i = next_i
        current_j = next_j

    return len(positions_visited)

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
    num = get_num_positions_visited(matrix)
    print(num)
