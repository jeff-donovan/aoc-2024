'''
--- Part Two ---
While The Historians begin working around the guard's patrol route, you borrow their fancy device and step outside the lab. From the safety of a supply closet, you time travel through the last few months and record the nightly status of the lab's guard post on the walls of the closet.

Returning after what seems like only a few seconds to The Historians, they explain that the guard's patrol area is simply too large for them to safely search the lab without getting caught.

Fortunately, they are pretty sure that adding a single new obstruction won't cause a time paradox. They'd like to place the new obstruction in such a way that the guard will get stuck in a loop, making the rest of the lab safe to search.

To have the lowest chance of creating a time paradox, The Historians would like to know all of the possible positions for such an obstruction. The new obstruction can't be placed at the guard's starting position - the guard is there right now and would notice.

In the above example, there are only 6 different positions where a new obstruction would cause the guard to get stuck in a loop. The diagrams of these six situations use O to mark the new obstruction, | to show a position where the guard moves up/down, - to show a position where the guard moves left/right, and + to show a position where the guard moves both up/down and left/right.

Option one, put a printing press next to the guard's starting position:

....#.....
....+---+#
....|...|.
..#.|...|.
....|..#|.
....|...|.
.#.O^---+.
........#.
#.........
......#...
Option two, put a stack of failed suit prototypes in the bottom right quadrant of the mapped area:


....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
......O.#.
#.........
......#...
Option three, put a crate of chimney-squeeze prototype fabric next to the standing desk in the bottom right quadrant:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----+O#.
#+----+...
......#...
Option four, put an alchemical retroencabulator near the bottom left corner:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
..|...|.#.
#O+---+...
......#...
Option five, put the alchemical retroencabulator a bit to the right instead:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
....|.|.#.
#..O+-+...
......#...
Option six, put a tank of sovereign glue right next to the tank of universal solvent:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----++#.
#+----++..
......#O..
It doesn't really matter what you choose to use as an obstacle so long as you and The Historians can put it into position without the guard noticing. The important thing is having enough options that you can find one that minimizes time paradoxes, and in this example, there are 6 different positions you could choose.

You need to get the guard stuck in a loop by adding a single new obstruction. How many different positions could you choose for this obstruction?
'''


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
