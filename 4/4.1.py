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
    num = 0
    for is_backwards in [True, False]:
        if is_xmas_horizontal(matrix, x_coords, is_backwards):
            num += 1

        if is_xmas_vertical(matrix, x_coords, is_backwards):
            num += 1

    num += num_xmas_diagonal(matrix, x_coords, is_backwards)

    return num

def is_xmas_horizontal(matrix, x_coords, is_backwards):
    i, j = x_coords

    if is_backwards:
        return (j - 3 >= 0) and (
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
        return (i - 3 >= 0) and (
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

def num_xmas_diagonal(matrix, x_coords, is_backwards):
    i, j = x_coords

    num = 0

    # down and to the right
    if (i + 3 < len(matrix) and j + 3 < len(matrix)) and (
        matrix[i][j] == 'X'
        and matrix[i + 1][j + 1] == 'M'
        and matrix[i + 2][j + 2] == 'A'
        and matrix[i + 3][j + 3] == 'S'
    ):
        num += 1

    # down and to the left
    if (i + 3 < len(matrix) and j - 3 >= 0) and (
        matrix[i][j] == 'X'
        and matrix[i + 1][j - 1] == 'M'
        and matrix[i + 2][j - 2] == 'A'
        and matrix[i + 3][j - 3] == 'S'
    ):
        num += 1

    # up and to the left
    if (i - 3 >= 0 and j - 3 >= 0) and (
        matrix[i][j] == 'X'
        and matrix[i - 1][j - 1] == 'M'
        and matrix[i - 2][j - 2] == 'A'
        and matrix[i - 3][j - 3] == 'S'
    ):
        num += 1

    # up and to the right
    if (i - 3 >= 0 and j + 3 < len(matrix)) and (
        matrix[i][j] == 'X'
        and matrix[i - 1][j + 1] == 'M'
        and matrix[i - 2][j + 2] == 'A'
        and matrix[i - 3][j + 3] == 'S'
    ):
        num += 1

    return num


if __name__ == '__main__':
    with open('4/day_4_input.txt', 'r') as f:
        contents = f.read()

    matrix = make_matrix(contents)
    num = num_xmas(matrix)
    print(num)
