from datetime import datetime


def make_stones(contents):
    return [int(string_stone) for string_stone in contents.split(' ') if string_stone]

def num_stones_for_blinks(stones, blinks):
    cache = {}
    total_stones = 0
    for stone in stones:
        total_stones += recursive_blink_for_stone(cache, stone, blinks)

    return total_stones

def recursive_blink_for_stone(cache, stone, level):
    if level == 0:
        return 1

    if (stone, level) in cache:
        return cache[(stone, level)]

    string_stone = str(stone)

    if stone == 0:
        cache[(0, level)] = recursive_blink_for_stone(cache, 1, level - 1)

    elif len(string_stone) % 2 == 0:
        left_stone = int(string_stone[:len(string_stone) // 2])
        right_stone = int(string_stone[len(string_stone) // 2:])
        cache[(stone, level)] = recursive_blink_for_stone(cache, left_stone, level - 1) + recursive_blink_for_stone(cache, right_stone, level - 1)

    else:
        cache[(stone, level)] = recursive_blink_for_stone(cache, stone * 2024, level - 1)

    return cache[(stone, level)]

if __name__ == '__main__':
    with open('11/day_11_input.txt', 'r') as f:
        contents = f.read()

    stones = make_stones(contents)

    start = datetime.now()
    num = num_stones_for_blinks(stones, 75)
    print(datetime.now() - start)
    print(num)
