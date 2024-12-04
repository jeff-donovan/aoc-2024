'''
--- Day 4: Ceres Search ---
"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:


..X...
.SAMX.
.A..A.
XMAS.S
.X....
The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
Take a look at the little Elf's word search. How many times does XMAS appear?
'''

def num_xmas(matrix):
    all_x_coords = get_all_x_coords(matrix)
    return sum([num_xmas_for_x_coords(matrix, x_coords) for x_coords in all_x_coords])

def get_all_x_coords(matrix):
    all_x_coords = []
    for i, row in enumerate(matrix):
        for j, char in enumerate(row):
            if char == 'X':
                all_x_coords.append((i, j))
    return all_x_coords

def make_matrix(contents):
    return [row for row in contents.split('\n') if row]

def num_xmas_for_x_coords(matrix, x_coords):
    print()
    print('x-coords: ', x_coords)
    num = 0
    for is_backwards in [True, False]:
        if is_xmas_horizontal(matrix, x_coords, is_backwards):
            print('is_xmas_horizontal')
            num += 1

        if is_xmas_vertical(matrix, x_coords, is_backwards):
            print('is_xmas_vertical')
            num += 1

        if is_xmas_diagonal(matrix, x_coords, is_backwards):
            print('is_xmas_diagonal')
            num += 1
    return num

def is_xmas_horizontal(matrix, x_coords, is_backwards):
    i, j = x_coords

    if is_backwards:
        return (j - 3 > 0) and (
            matrix[i][j] == 'X'
            and matrix[i][j - 1] == 'M'
            and matrix[i][j - 2] == 'A'
            and matrix[i][j - 3] == 'S'
        )

    return (j + 3 < len(matrix[i])) and (
        matrix[i][j] == 'X'
        and matrix[i][j + 1] == 'M'
        and matrix[i][j + 2] == 'A'
        and matrix[i][j + 3] == 'S'
    )

def is_xmas_vertical(matrix, x_coords, is_backwards):
    i, j = x_coords

    if is_backwards:
        return (i - 3 > 0) and (
            matrix[i][j] == 'X'
            and matrix[i - 1][j] == 'M'
            and matrix[i - 2][j] == 'A'
            and matrix[i - 3][j] == 'S'
        )

    return (i + 3 < len(matrix)) and (
        matrix[i][j] == 'X'
        and matrix[i + 1][j] == 'M'
        and matrix[i + 2][j] == 'A'
        and matrix[i + 3][j] == 'S'
    )

def is_xmas_diagonal(matrix, x_coords, is_backwards):
    i, j = x_coords

    if is_backwards:
        return (i - 3 > 0 and j - 3 > 0) and (
            matrix[i][j] == 'X'
            and matrix[i - 1][j - 1] == 'M'
            and matrix[i - 2][j - 2] == 'A'
            and matrix[i - 3][j - 3] == 'S'
        )

    return (i + 3 < len(matrix) and j + 3 < len(matrix)) and (
        matrix[i][j] == 'X'
        and matrix[i + 1][j + 1] == 'M'
        and matrix[i + 2][j + 2] == 'A'
        and matrix[i + 3][j + 3] == 'S'
    )


if __name__ == '__main__':
    with open('4/day_4_test.txt', 'r') as f:
        contents = f.read()

    matrix = make_matrix(contents)
    num = num_xmas(matrix)
    print(num)
