'''
--- Day 6: Guard Gallivant ---
The Historians use their fancy device again, this time to whisk you all away to the North Pole prototype suit manufacturing lab... in the year 1518! It turns out that having direct access to history is very convenient for a group of historians.

You still have to be careful of time paradoxes, and so it will be important to avoid anyone from 1518 while The Historians search for the Chief. Unfortunately, a single guard is patrolling this part of the lab.

Maybe you can work out where the guard will go ahead of time so that The Historians can search safely?

You start by making a map (your puzzle input) of the situation. For example:

....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
The map shows the current position of the guard with ^ (to indicate the guard is currently facing up from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

If there is something directly in front of you, turn right 90 degrees.
Otherwise, take a step forward.
Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:

....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:

....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...
This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..
By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..
In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?
'''

import pprint


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
    with open('6/day_6_test.txt', 'r') as f:
        contents = f.read()

    matrix = make_matrix(contents)
    num = get_num_positions_visited(matrix)
    print(num)
