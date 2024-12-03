'''
--- Part Two ---
As you scan through the corrupted memory, you notice that some of the conditional statements are also still intact. If you handle some of the uncorrupted conditional statements in the program, you might be able to get an even more accurate result.

There are two new instructions you'll need to handle:

The do() instruction enables future mul instructions.
The don't() instruction disables future mul instructions.
Only the most recent do() or don't() instruction applies. At the beginning of the program, mul instructions are enabled.

For example:

xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
This corrupted memory is similar to the example from before, but this time the mul(5,5) and mul(11,8) instructions are disabled because there is a don't() instruction before them. The other mul instructions function normally, including the one at the end that gets re-enabled by a do() instruction.

This time, the sum of the results is 48 (2*4 + 8*5).

Handle the new instructions; what do you get if you add up all of the results of just the enabled multiplications?
'''

import re


def find_all_substrings(contents):
    dos = find_all_do_indexes(contents)
    donts = find_all_donts_indexes(contents)
    return []

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
    with open('3/day_3_test_2.txt', 'r') as f:
        contents = f.read()

    substrings = find_all_substrings(contents)

    mul_sum = 0
    for substring in substrings:
        pairs = get_mul_pairs_as_strings(substring)
        for pair in pairs:
            mul_sum += int(pair[0]) * int(pair[1])
    print(mul_sum)
