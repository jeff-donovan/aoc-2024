import re


def find_all_substrings(contents):
    dos = find_all_do_indexes(contents)
    donts = find_all_donts_indexes(contents)

    substrings = []
    substring = ''
    enabled = True
    for i, char in enumerate(contents):
        if enabled and (i not in donts):
            substring += char
            continue

        if not enabled and i in dos:
            enabled = True
            substring += char
            continue

        if enabled and i in donts:
            substrings.append(substring)
            substring = ''
            enabled = False
            continue

    if enabled:
        substrings.append(substring)

    return substrings

def find_all_donts_indexes(contents):
    pattern = re.escape("don't()")
    return [match.start() for match in re.finditer(pattern, contents)]

def find_all_do_indexes(contents):
    pattern = re.escape('do()')
    return [match.start() for match in re.finditer(pattern, contents)]


def get_mul_pairs_as_strings(contents):
    pattern = re.escape('mul(') + '[-+]?[0-9]+' + re.escape(',') + '[-+]?[0-9]+' + re.escape(')')
    mul_strings = [match for match in re.findall(pattern, contents)]
    return [re.findall('[-+]?[0-9]+', mul_string) for mul_string in mul_strings]


if __name__ == '__main__':
    with open('3/day_3_input.txt', 'r') as f:
        contents = f.read()

    substrings = find_all_substrings(contents)

    mul_sum = 0
    for substring in substrings:
        pairs = get_mul_pairs_as_strings(substring)
        for pair in pairs:
            mul_sum += int(pair[0]) * int(pair[1])
    print(mul_sum)
