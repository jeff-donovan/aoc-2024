import pprint


def make_robots(contents):
    robots = []
    for line in contents.split('\n'):
        if line:
            robot_data = line.split(' ')
            position_string = robot_data[0][2:].split(',')
            velocity_string = robot_data[1][2:].split(',')
            robots.append({
                'position': (int(position_string[0]), int(position_string[1])),
                'velocity': (int(velocity_string[0]), int(velocity_string[1])),
            })
    pprint.pprint(robots)
    return robots

def positions_after_seconds(space_size, robots, num_seconds):
    positions = []
    for robot in robots:
        robot_position = get_robot_position(space_size, robot['position'], robot['velocity'], num_seconds)
        positions.append(robot_position)
    return positions

def get_robot_position(space_size, initial_position, velocity, num_seconds):
    width, height = space_size
    x = (initial_position[0] + num_seconds * velocity[0]) % width
    y = (initial_position[1] + num_seconds * velocity[1]) % height
    return (x, y)

def draw_space(space_size, positions):
    width, height = space_size
    space = []
    for _ in range(height):
        row = []
        for _ in range(width):
            row.append('.')
        space.append(row)

    for j, i in positions:
        if space[i][j] == '.':
            space[i][j] = '0'
        space[i][j] = str(int(space[i][j]) + 1)

    for row in space:
        print(''.join(row))

if __name__ == '__main__':
    with open('14/day_14_input.txt', 'r') as f:
        contents = f.read()

    # # test
    # space_size = (11, 7)

    # input
    space_size = (101, 103)

    robots = make_robots(contents)
    seconds_elapsed = 7857
    while True:
        seconds_elapsed += 1
        positions = positions_after_seconds(space_size, robots, seconds_elapsed)
        draw_space(space_size, positions)
        print()

        if input(f'{seconds_elapsed} | Do You Want To Continue? ') == 'n':
            break
        # if seconds_elapsed == 100:
        #     break
    print(seconds_elapsed)
