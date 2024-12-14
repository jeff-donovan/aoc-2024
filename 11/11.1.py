def make_stones(contents):
    return [int(string_stone) for string_stone in contents.split(' ') if string_stone]

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
    for i in range(25):
        stones = blink(stones)
        print(stones)

    num = len(stones)
    print(num)
