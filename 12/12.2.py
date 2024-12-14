def make_garden(contents):
    return [row for row in contents.split('\n') if row]

def make_plant_plot_mapping(garden):
    plant_plot_mapping = {}
    for i in range(len(garden)):
        for j in range(len(garden[i])):
            plant_type = garden[i][j]
            if plant_type not in plant_plot_mapping:
                plant_plot_mapping[plant_type] = set([])
            plant_plot_mapping[plant_type].add((i, j))
    return plant_plot_mapping

def get_total_price(regions):
    total = 0
    for region in regions:
        total += area(region) * num_sides(region)
    return total

def area(region):
    return len(region)

def num_sides(region):
    return len(get_sides_for_region(region))

def get_sides_for_region(region):
    potential_sides = set([])
    for plot in region:
        i, j = plot
        for adjacent_plot in [
            (i - 1, j, 'up'),
            (i + 1, j, 'down'),
            (i, j - 1, 'left'),
            (i, j + 1, 'right'),
        ]:
            if (adjacent_plot[0], adjacent_plot[1]) not in region:
                potential_sides.add(adjacent_plot)

    sides = []
    cache = {}
    for plot_a in potential_sides:
        for plot_b in potential_sides:
            if (plot_a == plot_b):
                continue

            visited = []
            plot_a_i, plot_a_j, plot_a_direction = plot_a
            plot_b_i, plot_b_j, plot_b_direction = plot_b
            if is_connected_side(cache, potential_sides, visited, plot_a_i, plot_a_j, plot_a_direction, plot_b_i, plot_b_j, plot_b_direction):
                added_to_side = False
                for side in sides:
                    if (plot_a in side) or (plot_b in side):
                        side.add(plot_a)
                        side.add(plot_b)
                        added_to_side = True
                if not added_to_side:
                    sides.append(set([plot_a, plot_b]))

    for plot in potential_sides:
        is_in_side = any(plot in side for side in sides)
        if not is_in_side:
            sides.append(set([plot]))
    return sides

def is_connected_side(cache, potential_sides, visited, i1, j1, direction1, i2, j2, direction2):
    # base case 0: diff directions
    if direction1 != direction2:
        return False

    # base case 1: same coords
    if i1 == i2 and j1 == j2 and direction1 == direction2:
        return True

    # ensure cache is set up
    if (i1, j1, direction1) not in cache:
        cache[(i1, j1, direction1)] = {}
    if (i2, j2, direction2) not in cache:
        cache[(i2, j2, direction2)] = {}

    # base case 2: cached result
    if (i2, j2, direction2) in cache[(i1, j1, direction1)]:
        return cache[(i1, j1, direction1)][(i2, j2, direction2)]
    if (i1, j1, direction1) in cache[(i2, j2, direction2)]:
        return cache[(i2, j2, direction2)][(i1, j1, direction1)]

    # base case 3: already visited this point
    if (i1, j1, direction1) in visited:
        return False

    visited.append((i1, j1, direction1))

    up = (i1 - 1, j1, direction1)
    down = (i1 + 1, j1, direction1)
    left = (i1, j1 - 1, direction1)
    right = (i1, j1 + 1, direction1)
    adjacent_plots = set([up, down, left, right])

    intersection = list(adjacent_plots & potential_sides)

    result = any(is_connected_side(cache, potential_sides, visited, i, j, direction, i2, j2, direction2) for i, j, direction in intersection)
    cache[(i1, j1, direction1)][(i2, j2, direction2)] = result
    cache[(i2, j2, direction2)][(i1, j1, direction1)] = result
    return result

def get_all_regions(mapping):
    regions = []
    for plant_type in mapping:
        regions.extend(get_regions_for_plant_type(mapping[plant_type]))
    return regions

def get_regions_for_plant_type(plant_plots):
    regions = []
    cache = {}
    for plot_a in plant_plots:
        for plot_b in plant_plots:
            if (plot_a == plot_b):
                continue

            visited = []
            if is_connected(cache, plant_plots, visited, plot_a[0], plot_a[1], plot_b[0], plot_b[1]):
                added_to_region = False
                for region in regions:
                    if (plot_a in region) or (plot_b in region):
                        region.add(plot_a)
                        region.add(plot_b)
                        added_to_region = True
                if not added_to_region:
                    regions.append(set([plot_a, plot_b]))

    for plot in plant_plots:
        is_in_region = any(plot in region for region in regions)
        if not is_in_region:
            regions.append(set([plot]))
    return regions

def is_connected(cache, plant_plots, visited, i1, j1, i2, j2):
    # base case 1: same coords
    if i1 == i2 and j1 == j2:
        return True

    # ensure cache is set up
    if (i1, j1) not in cache:
        cache[(i1, j1)] = {}
    if (i2, j2) not in cache:
        cache[(i2, j2)] = {}

    # base case 2: cached result
    if (i2, j2) in cache[(i1, j1)]:
        return cache[(i1, j1)][(i2, j2)]
    if (i1, j1) in cache[(i2, j2)]:
        return cache[(i2, j2)][(i1, j1)]

    # base case 3: already visited this point
    if (i1, j1) in visited:
        return False

    visited.append((i1, j1))

    up = (i1 - 1, j1)
    down = (i1 + 1, j1)
    left = (i1, j1 - 1)
    right = (i1, j1 + 1)
    adjacent_plots = set([up, down, left, right])

    intersection = list(adjacent_plots & plant_plots)

    result = any(is_connected(cache, plant_plots, visited, i, j, i2, j2) for i, j in intersection)
    cache[(i1, j1)][(i2, j2)] = result
    cache[(i2, j2)][(i1, j1)] = result
    return result

if __name__ == '__main__':
    for expected, test_file in [
        (80, '12/day_12_test.txt'),
        (436, '12/day_12_test_2.txt'),
        (236, '12/day_12_test_e_shaped.txt'),
        (368, '12/day_12_test_ab.txt'),
        (1206, '12/day_12_test_3.txt'),
    ]:
        with open(test_file, 'r') as f:
            contents = f.read()

        garden = make_garden(contents)
        mapping = make_plant_plot_mapping(garden)
        regions = get_all_regions(mapping)

        num = get_total_price(regions)
        if num == expected:
            print('LETS GOOOOO')
        else:
            exit(f'Testing {test_file} | expected {expected}, but got {num}')

    with open('12/day_12_input.txt', 'r') as f:
        contents = f.read()

    garden = make_garden(contents)
    mapping = make_plant_plot_mapping(garden)
    regions = get_all_regions(mapping)

    num = get_total_price(regions)
    print(num)
