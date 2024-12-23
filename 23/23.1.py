def parse_input(contents):
    connections = {}
    for line in contents.split('\n'):
        if line:
            a, b = line.split('-')
            if a not in connections:
                connections[a] = set([])
            if b not in connections:
                connections[b] = set([])
            connections[a].add(b)
            connections[b].add(a)
    return connections

def t_in_combo(combo):
    return combo[0].startswith('t') or combo[1].startswith('t') or combo[2].startswith('t')

if __name__ == '__main__':
    with open('23/day_23_input.txt', 'r') as f:
        contents = f.read()

    connections = parse_input(contents)

    multi = set([])
    for a in connections:
        for b in connections:
            for c in connections:
                a_to_b = b in connections[a]
                b_to_c = c in connections[b]
                c_to_a = a in connections[c]
                if a_to_b and b_to_c and c_to_a:
                    combo = sorted([a, b, c])
                    multi.add((combo[0], combo[1], combo[2]))
    print(sum([1 for combo in multi if t_in_combo(combo)]))
