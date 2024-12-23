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

def largest_lan_party_for_group(connections, group):
    if is_lan_party(connections, group):
        return group

    largest_lan_party = set([])
    for computer in group:
        new_group = set(group)
        new_group.remove(computer)
        new_lan_party = largest_lan_party_for_group(connections, new_group)
        if len(new_lan_party) > len(largest_lan_party):
            largest_lan_party = new_lan_party
    return largest_lan_party

if __name__ == '__main__':
    with open('23/day_23_input.txt', 'r') as f:
        contents = f.read()

    connections = parse_input(contents)
    # sorted_connections = dict(sorted(connections.items(), key=lambda item: len(item[1])))

    largest_lan_party = set([])
    for computer in connections:
        group = set(list(connections[computer]) + [computer])
        new_lan_party = largest_lan_party_for_group(connections, group)
        if len(new_lan_party) > len(largest_lan_party):
            largest_lan_party = new_lan_party
            print('new largest lan party: ', largest_lan_party)
    print(','.join(sorted(list(largest_lan_party))))
