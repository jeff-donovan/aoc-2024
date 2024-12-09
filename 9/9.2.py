'''
--- Part Two ---
Upon completion, two things immediately become clear. First, the disk definitely has a lot more contiguous free space, just like the amphipod hoped. Second, the computer is running much more slowly! Maybe introducing all of that file system fragmentation was a bad idea?

The eager amphipod already has a new plan: rather than move individual blocks, he'd like to try compacting the files on his disk by moving whole files instead.

This time, attempt to move whole files to the leftmost span of free space blocks that could fit the file. Attempt to move each file exactly once in order of decreasing file ID number starting with the file with the highest file ID number. If there is no span of free space to the left of a file that is large enough to fit the file, the file does not move.

The first example from above now proceeds differently:

00...111...2...333.44.5555.6666.777.888899
0099.111...2...333.44.5555.6666.777.8888..
0099.1117772...333.44.5555.6666.....8888..
0099.111777244.333....5555.6666.....8888..
00992111777.44.333....5555.6666.....8888..
The process of updating the filesystem checksum is the same; now, this example's checksum would be 2858.

Start over, now compacting the amphipod's hard drive using this new method instead. What is the resulting filesystem checksum?
'''


def convert_disk_map_to_blocks(contents):
    blocks = []
    for i, char in enumerate(contents):
        if char != '\n':
            if i % 2 == 0:  # file
                file_id = i // 2
                for _ in range(int(char)):
                    blocks.append(file_id)
            else:  # free space
                for _ in range(int(char)):
                    blocks.append('.')
    return blocks

def compact_entire_filesystem(contents):
    blocks = convert_disk_map_to_blocks(contents)
    for file_id in reversed(range(get_largest_file_id(blocks) + 1)):
        blocks = attempt_to_move_file(contents, blocks, file_id)
    return blocks

def get_largest_file_id(blocks):
    for i in reversed(range(len(blocks))):
        if blocks[i] != '.':
            return int(blocks[i])

def attempt_to_move_file(contents, blocks, file_id):
    file_size = get_file_size(contents, file_id)
    file_index = blocks.index(file_id)
    free_space_index = get_free_space_index_for_file_size(blocks, file_size)

    # cant find free space big enough
    if free_space_index == -1:
        return blocks

    # big enough free space is to the right
    if free_space_index > file_index:
        return blocks

    return switch_file_with_free_space(blocks, file_id, free_space_index)

def get_file_size(contents, file_id):
    return int(contents[file_id * 2])

def get_free_space_index_for_file_size(blocks, file_size):
    blocks_as_string = ''
    for block in blocks:
        if block == '.':
            blocks_as_string += '.'
        else:
            blocks_as_string += 'N'
    return blocks_as_string.find('.' * file_size)

def switch_file_with_free_space(blocks, file_id, free_space_index):
    is_switching = False
    current_free_space_index = free_space_index
    for i in reversed(range(len(blocks))):
        char = blocks[i]
        if is_switching and char != file_id:
            return blocks

        if char == file_id:
            is_switching = True
            blocks[current_free_space_index] = char
            blocks[i] = '.'
            current_free_space_index += 1

    return blocks

def calculate_checksum(blocks):
    sum = 0
    for i, char in enumerate(blocks):
        if char != '.':
            sum += i * char
    return sum

if __name__ == '__main__':
    with open('9/day_9_test.txt', 'r') as f:
        contents = f.read()

    blocks = compact_entire_filesystem(contents)
    num = calculate_checksum(blocks)
    print(num)
