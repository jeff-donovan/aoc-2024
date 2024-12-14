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
        total += area(region) * perimeter(region)
    return total

def area(region):
    return len(region)

def perimeter(region):
    total = 0
    for i, j in region:
        up = (i - 1, j)
        down = (i + 1, j)
        left = (i, j - 1)
        right = (i, j + 1)
        for adjacent_plot in [up, down, left, right]:
            if adjacent_plot not in region:
                total += 1
    return total

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
    with open('12/day_12_input.txt', 'r') as f:
        contents = f.read()

    garden = make_garden(contents)
    print('GARDEN DONE')

    mapping = make_plant_plot_mapping(garden)
    print('MAPPING DONE')

    regions = get_all_regions(mapping)
    print('REGIONS DONE')

    num = get_total_price(regions)
    print(num)
