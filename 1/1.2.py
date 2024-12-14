def calculate_similarity_score(left, right):
    score = 0
    for left_element in left:
        score += left_element * num_times_in_list(left_element, right)
    return score

def num_times_in_list(number, right_list):
    num_times = 0
    for element in right_list:
        if number == element:
            num_times += 1
    return num_times

def build_lists(contents):
    left = []
    right = []

    for line in contents.split('\n'):
        if line:
            le, re = line.split()
            left.append(int(le))
            right.append(int(re))

    return left, right


if __name__ == '__main__':
    with open('1/day_1_input.txt', 'r') as f:
        contents = f.read()

    left, right = build_lists(contents)
    score = calculate_similarity_score(left, right)
    print(score)
