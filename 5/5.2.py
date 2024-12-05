'''
--- Part Two ---
While the Elves get to work printing the correctly-ordered updates, you have a little time to fix the rest of them.

For each of the incorrectly-ordered updates, use the page ordering rules to put the page numbers in the right order. For the above example, here are the three incorrectly-ordered updates and their correct orderings:

75,97,47,61,53 becomes 97,75,47,61,53.
61,13,29 becomes 61,29,13.
97,13,75,29,47 becomes 97,75,47,29,13.
After taking only the incorrectly-ordered updates and ordering them correctly, their middle page numbers are 47, 29, and 47. Adding these together produces 123.

Find the updates which are not in the correct order. What do you get if you add up the middle page numbers after correctly ordering just those updates?
'''

import functools
import math
import pprint


def sort_update(rules, update):
    return sorted(update, key=functools.cmp_to_key(lambda x, y: cmp(rules, x, y)))

def cmp(rules, x, y):
    if y in rules[x]['is_before']:
        return -1
    if y in rules[x]['is_after']:
        return 1

    if x in rules[y]['is_before']:
        return 1
    if x in rules[y]['is_after']:
        return -1

    return 0


def make_rules_dictionary(contents):
    rules = {}
    for row in contents.split('\n'):
        if '|' in row:
            before, after = row.split('|')
            before = int(before)
            after = int(after)

            if before not in rules:
                rules[before] = {'is_before': set(), 'is_after': set()}
            rules[before]['is_before'].add(after)

            if after not in rules:
                rules[after] = {'is_before': set(), 'is_after': set()}
            rules[after]['is_after'].add(before)

    return rules

def make_updates_list(contents):
    updates = []
    for row in contents.split('\n'):
        if ',' in row:
            update_as_strings = row.split(',')
            update = [int(page_number) for page_number in update_as_strings]
            print(update)
            updates.append(update)

    return updates

def is_update_valid(rules, update):
    for page_number_index, page_number in enumerate(update):
        if not is_page_number_valid(rules, update, page_number_index, page_number):
            return False
    return True

def is_page_number_valid(rules, update, page_number_index, page_number):
    page_rules = rules[page_number]
    for i in range(0, page_number_index):
        compare_number = update[i]
        if compare_number in page_rules['is_before']:
            return False
    for i in range(page_number_index + 1, len(update)):
        compare_number = update[i]
        if compare_number in page_rules['is_after']:
            return False
    return True

def get_middle_page_number(update):
    middle_index = math.floor(len(update) / 2.0)
    return update[middle_index]


if __name__ == '__main__':
    with open('5/day_5_input.txt', 'r') as f:
        contents = f.read()

    rules = make_rules_dictionary(contents)
    # pprint.pprint(rules)

    sorted_invalid_updates = [sort_update(rules, update) for update in make_updates_list(contents) if not is_update_valid(rules, update)]
    num = sum([get_middle_page_number(update) for update in sorted_invalid_updates])
    print(num)
