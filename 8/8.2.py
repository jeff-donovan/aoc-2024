def make_map(contents):
    return [line for line in contents.split('\n') if line]

def num_unique_antinode_locations(map):
    antinode_locations = set([])
    frequencies = get_frequencies(map)
    for frequency in frequencies:
        print('FREQUENCY: ', frequency)
        antenna_pairs = get_antenna_pairs(map, frequency)
        for antenna_pair in antenna_pairs:
            print(antenna_pair)
            antinodes = calculate_antinode_coords_for_antenna_pair(map, antenna_pair)
            for antinode in antinodes:
                if is_on_map(map, antinode):
                    antinode_locations.add(antinode)
        print()
    return len(antinode_locations)

def get_frequencies(map):
    frequencies = set([])
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] != '.':
                frequencies.add(map[i][j])
    return frequencies

def get_antenna_pairs(map, frequency):
    antennas = get_all_antennas_for_frequency(map, frequency)
    pairs = set([])
    for a in antennas:
        for b in antennas:
            if a != b and (b, a) not in pairs:
                pairs.add((a, b))
    return pairs

def get_all_antennas_for_frequency(map, frequency):
    antennas = set([])
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == frequency:
                antennas.add((i, j))
    return antennas

def calculate_antinode_coords_for_antenna_pair(map, antenna_pair):
    a, b = antenna_pair
    i_diff = b[0] - a[0]
    j_diff = b[1] - a[1]

    antinodes = set([a, b])
    for magnitude in range(max(len(map), len(map[0]))):
        new_a = (a[0] - magnitude * i_diff, a[1] - magnitude * j_diff)
        new_b = (b[0] + magnitude * i_diff, b[1] + magnitude * j_diff)
        antinodes.add(new_a)
        antinodes.add(new_b)
    return antinodes

def is_on_map(map, antinode):
    i, j = antinode
    return (0 <= i < len(map)) and (0 <= j < len(map[i]))


if __name__ == '__main__':
    with open('8/day_8_input.txt', 'r') as f:
        contents = f.read()

    map = make_map(contents)
    num = num_unique_antinode_locations(map)
    print(num)
