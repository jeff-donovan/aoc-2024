import re


def get_mul_pairs_as_strings(contents):
    pattern = re.escape('mul(') + '[-+]?[0-9]+' + re.escape(',') + '[-+]?[0-9]+' + re.escape(')')
    mul_strings = [match for match in re.findall(pattern, contents)]
    return [re.findall('[-+]?[0-9]+', mul_string) for mul_string in mul_strings]


if __name__ == '__main__':
    with open('3/day_3_input.txt', 'r') as f:
        contents = f.read()

    pairs = get_mul_pairs_as_strings(contents)
    mul_sum = 0
    for pair in pairs:
        mul_sum += int(pair[0]) * int(pair[1])
    print(mul_sum)
