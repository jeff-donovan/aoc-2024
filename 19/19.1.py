def make_towels_and_designs(contents):
    towels_contents, designs_contents = contents.split('\n\n')

    towels = [t for t in towels_contents.split(', ') if t]
    designs = [d for d in designs_contents.split('\n') if d]

    return towels, designs

def is_design_possible(towels, towel, remaining_design):
    # base case - all we have left is an exact towel match
    if towel == remaining_design:
        return True

    # base case - the towel doesn't exist *at the start* of the design
    if not remaining_design.startswith(towel):
        return False

    # at this point we know the towel starts off the remaining design so we can truncate and check what's left
    next_remaining_design = remaining_design[len(towel):]
    return any([is_design_possible(towels, t, next_remaining_design) for t in towels])

if __name__ == '__main__':
    with open('19/day_19_test.txt', 'r') as f:
        contents = f.read()

    towels, designs = make_towels_and_designs(contents)
    print(sum([is_design_possible(towels, '', d) for d in designs]))
