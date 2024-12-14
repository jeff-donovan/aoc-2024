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
    pprint.pprint(positions)
    return positions

def get_robot_position(space_size, initial_position, velocity, num_seconds):
    width, height = space_size
    x = (initial_position[0] + num_seconds * velocity[0]) % width
    y = (initial_position[1] + num_seconds * velocity[1]) % height
    return (x, y)

def group_by_quadrant(space_size, positions):
    dividers = (space_size[0] // 2, space_size[1] // 2)
    quadrant_1 = [pos for pos in positions if pos[0] < dividers[0] and pos[1] < dividers[1]]
    quadrant_2 = [pos for pos in positions if pos[0] > dividers[0] and pos[1] > dividers[1]]
    quadrant_3 = [pos for pos in positions if pos[0] < dividers[0] and pos[1] > dividers[1]]
    quadrant_4 = [pos for pos in positions if pos[0] > dividers[0] and pos[1] < dividers[1]]
    return [quadrant_1, quadrant_2, quadrant_3, quadrant_4]

def safety_factor(quadrants):
    total = 1
    for quad in quadrants:
        total = total * len(quad)
    return total

if __name__ == '__main__':
    with open('14/day_14_input.txt', 'r') as f:
        contents = f.read()

    # # test
    # space_size = (11, 7)

    # input
    space_size = (101, 103)

    robots = make_robots(contents)
    positions = positions_after_seconds(space_size, robots, 100)
    quadrants = group_by_quadrant(space_size, positions)
    num = safety_factor(quadrants)
    print(num)
