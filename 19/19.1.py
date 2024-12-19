def make_towels_and_designs(contents):
    towels_contents, designs_contents = contents.split('\n\n')

    towels = [t for t in towels_contents.split(', ') if t]
    designs = [d for d in designs_contents.split('\n') if d]

    return towels, designs

def is_design_possible(cache, towels, remaining_design):
    if remaining_design in cache:
        return cache[remaining_design]

    # base case - all we have left is an exact towel match
    for towel in towels:
        if towel == remaining_design:
            cache[remaining_design] = True
            return True

    # base case - no towel exists *at the start* of the design
    remaining_designs_to_check = set([])
    for towel in towels:
        if remaining_design.startswith(towel):
            next_remaining_design = remaining_design[len(towel):]
            remaining_designs_to_check.add(next_remaining_design)

    if len(remaining_designs_to_check) == 0:
        cache[remaining_design] = False
        return False

    # at this point we know a towel starts off the remaining design so we can check the truncated designs
    cache[remaining_design] = any([is_design_possible(cache, towels, next_remaining_design) for next_remaining_design in remaining_designs_to_check])
    return cache[remaining_design]

if __name__ == '__main__':
    with open('19/day_19_input.txt', 'r') as f:
        contents = f.read()

    towels, designs = make_towels_and_designs(contents)
    cache = {}
    print(sum([is_design_possible(cache, towels, d) for d in designs]))
