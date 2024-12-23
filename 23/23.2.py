import datetime


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

def largest_lan_party_for_group(cache, connections, group):
    key = cache_key(group)
    if key in cache:
        return cache[key]

    if is_lan_party(connections, group):
        cache[key] = group
        return group

    largest_lan_party = set([])
    for computer in group:
        new_group = set(group)
        new_group.remove(computer)
        new_lan_party = largest_lan_party_for_group(cache, connections, new_group)
        if len(new_lan_party) > len(largest_lan_party):
            largest_lan_party = new_lan_party

    cache[key] = largest_lan_party
    return largest_lan_party

def cache_key(combo_set):
    return tuple(sorted(combo_set))

if __name__ == '__main__':
    with open('23/day_23_input.txt', 'r') as f:
        contents = f.read()

    start = datetime.datetime.now()

    connections = parse_input(contents)

    cache = {}
    largest_lan_party = set([])
    for computer in connections:
        group = set(list(connections[computer]) + [computer])
        new_lan_party = largest_lan_party_for_group(cache, connections, group)
        if len(new_lan_party) > len(largest_lan_party):
            largest_lan_party = new_lan_party
    print(','.join(sorted(list(largest_lan_party))))
    print('finished in ', datetime.datetime.now() - start)
