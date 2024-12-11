'''
--- Part Two ---
The Historians sure are taking a long time. To be fair, the infinite corridors are very large.

How many stones would you have after blinking a total of 75 times?
'''

from datetime import datetime


def make_stones(contents):
    return [int(string_stone) for string_stone in contents.split(' ') if string_stone]

def num_stones_for_blinks(stones, blinks):
    current = datetime.now()

    total_stones = 0
    for stone in stones:
        initial = [stone]
        for i in range(blinks):
            initial = blink(initial)
            print('blink ', i, ': ', datetime.now() - current)
            current = datetime.now()

        total_stones += len(initial)
    return total_stones

def blink(stones):
    new_stones = []
    for stone in stones:
        string_stone = str(stone)
        if stone == 0:
            new_stones.append(1)

        elif len(string_stone) % 2 == 0:
            left_stone = int(string_stone[:len(string_stone) // 2])
            right_stone = int(string_stone[len(string_stone) // 2:])
            new_stones.extend([left_stone, right_stone])

        else:
            new_stones.append(stone * 2024)

    return new_stones

if __name__ == '__main__':
    with open('11/day_11_input.txt', 'r') as f:
        contents = f.read()

    stones = make_stones(contents)

    num = num_stones_for_blinks(stones, 25)
    print(num)
