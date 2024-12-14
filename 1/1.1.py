def sum_pair_diffs(left, right):
    sum = 0
    for i in range(len(left)):
        sum += abs(left[i] - right[i])
    return sum

def build_sorted_lists(contents):
    left = []
    right = []

    for line in contents.split('\n'):
        if line:
            le, re = line.split()
            left.append(int(le))
            right.append(int(re))

    left.sort()
    right.sort()

    return left, right


if __name__ == '__main__':
    with open('1/day_1_input.txt', 'r') as f:
        contents = f.read()

    left, right = build_sorted_lists(contents)
    sum = sum_pair_diffs(left, right)
    print(sum)
