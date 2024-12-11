'''
--- Part Two ---
The Historians sure are taking a long time. To be fair, the infinite corridors are very large.

How many stones would you have after blinking a total of 75 times?
'''

from datetime import datetime


def make_stones(contents):
    return [int(string_stone) for string_stone in contents.split(' ') if string_stone]

def num_stones_for_blinks(stones, blinks):
    total_stones = 0
    for stone in stones:
        total_stones += recursive_blink_for_stone(stone, blinks)

    return total_stones

def recursive_blink_for_stone(stone, level):
    if level == 0:
        return 1

    if stone == 0:
        return recursive_blink_for_stone(1, level - 1)

    string_stone = str(stone)
    if len(string_stone) % 2 == 0:
        left_stone = int(string_stone[:len(string_stone) // 2])
        right_stone = int(string_stone[len(string_stone) // 2:])
        return recursive_blink_for_stone(left_stone, level - 1) + recursive_blink_for_stone(right_stone, level - 1)

    return recursive_blink_for_stone(stone * 2024, level - 1)

if __name__ == '__main__':
    with open('11/day_11_input.txt', 'r') as f:
        contents = f.read()

    stones = make_stones(contents)

    start = datetime.now()
    num = num_stones_for_blinks(stones, 40)
    print(datetime.now() - start)
    print(num)
