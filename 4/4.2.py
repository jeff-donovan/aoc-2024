'''
--- Part Two ---
The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

M.S
.A.
M.S
Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?
'''

def num_xmas(matrix):
    all_a_coords = get_all_a_coords(matrix)
    return sum([1 for a_coords in all_a_coords if is_xmas(matrix, a_coords)])

def get_all_a_coords(matrix):
    all_a_coords = []
    for i, row in enumerate(matrix):
        for j, char in enumerate(row):
            if char == 'A':
                all_a_coords.append((i, j))
    return all_a_coords

def make_matrix(contents):
    return [row for row in contents.split('\n') if row]

def is_xmas(matrix, a_coords):
    return (
        (is_mas_diagonal_down(matrix, a_coords) or is_sam_diagonal_down(matrix, a_coords)) and
        (is_mas_diagonal_up(matrix, a_coords) or is_sam_diagonal_up(matrix, a_coords))
    )

def is_mas_diagonal_down(matrix, a_coords):
    pass

def is_sam_diagonal_down(matrix, a_coords):
    pass

def is_mas_diagonal_up(matrix, a_coords):
    pass

def is_sam_diagonal_up(matrix, a_coords):
    pass

# def num_xmas_diagonal(matrix, x_coords, is_backwards):
#     i, j = x_coords

#     num = 0

#     # down and to the right
#     if (i + 3 < len(matrix) and j + 3 < len(matrix)) and (
#         matrix[i][j] == 'X'
#         and matrix[i + 1][j + 1] == 'M'
#         and matrix[i + 2][j + 2] == 'A'
#         and matrix[i + 3][j + 3] == 'S'
#     ):
#         num += 1

#     # down and to the left
#     if (i + 3 < len(matrix) and j - 3 >= 0) and (
#         matrix[i][j] == 'X'
#         and matrix[i + 1][j - 1] == 'M'
#         and matrix[i + 2][j - 2] == 'A'
#         and matrix[i + 3][j - 3] == 'S'
#     ):
#         num += 1

#     # up and to the left
#     if (i - 3 >= 0 and j - 3 >= 0) and (
#         matrix[i][j] == 'X'
#         and matrix[i - 1][j - 1] == 'M'
#         and matrix[i - 2][j - 2] == 'A'
#         and matrix[i - 3][j - 3] == 'S'
#     ):
#         num += 1

#     # up and to the right
#     if (i - 3 >= 0 and j + 3 < len(matrix)) and (
#         matrix[i][j] == 'X'
#         and matrix[i - 1][j + 1] == 'M'
#         and matrix[i - 2][j + 2] == 'A'
#         and matrix[i - 3][j + 3] == 'S'
#     ):
#         num += 1

#     return num


if __name__ == '__main__':
    with open('4/day_4_test.txt', 'r') as f:
        contents = f.read()

    matrix = make_matrix(contents)
    num = num_xmas(matrix)
    print(num)
