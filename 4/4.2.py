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
    i, j = a_coords

    safe_i = (0 <= i - 1) and (i + 1 < len(matrix))
    safe_j = (0 <= j - 1) and (j + 1 < len(matrix[i]))

    if not (safe_i and safe_j):
        return False

    return matrix[i - 1][j - 1] == 'M' and matrix[i + 1][j + 1] == 'S'

def is_sam_diagonal_down(matrix, a_coords):
    i, j = a_coords

    safe_i = (0 <= i - 1) and (i + 1 < len(matrix))
    safe_j = (0 <= j - 1) and (j + 1 < len(matrix[i]))

    if not (safe_i and safe_j):
        return False

    return matrix[i - 1][j - 1] == 'S' and matrix[i + 1][j + 1] == 'M'

def is_mas_diagonal_up(matrix, a_coords):
    i, j = a_coords

    safe_i = (0 <= i - 1) and (i + 1 < len(matrix))
    safe_j = (0 <= j - 1) and (j + 1 < len(matrix[i]))

    if not (safe_i and safe_j):
        return False

    return matrix[i + 1][j - 1] == 'M' and matrix[i - 1][j + 1] == 'S'

def is_sam_diagonal_up(matrix, a_coords):
    i, j = a_coords

    safe_i = (0 <= i - 1) and (i + 1 < len(matrix))
    safe_j = (0 <= j - 1) and (j + 1 < len(matrix[i]))

    if not (safe_i and safe_j):
        return False

    return matrix[i + 1][j - 1] == 'S' and matrix[i - 1][j + 1] == 'M'


if __name__ == '__main__':
    with open('4/day_4_input.txt', 'r') as f:
        contents = f.read()

    matrix = make_matrix(contents)
    num = num_xmas(matrix)
    print(num)
