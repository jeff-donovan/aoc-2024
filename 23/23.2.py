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

def is_lan_party(connections, combo):
    for computer in combo:
        for other_computer in combo:
            if (computer != other_computer) and computer not in connections[other_computer]:
                return False
    return True

if __name__ == '__main__':
    with open('23/day_23_test.txt', 'r') as f:
        contents = f.read()

    connections = parse_input(contents)

    print(is_lan_party(connections, set(['co', 'de', 'ta', 'ka'])))
