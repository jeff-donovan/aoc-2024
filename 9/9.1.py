def convert_disk_map_to_blocks(contents):
    blocks = []
    for i, char in enumerate(contents):
        if char != '\n':
            if i % 2 == 0:  # file
                file_id = i // 2
                for _ in range(int(char)):
                    blocks.append(str(file_id))
            else:  # free space
                for _ in range(int(char)):
                    blocks.append('.')
    return blocks

def compact_entire_filesystem(blocks):
    while not is_filesystem_compacted(blocks):
        blocks = switch_end_block_with_first_free_space(blocks)
    return blocks

def is_filesystem_compacted(blocks):
    first_free_space_index = blocks.index('.')
    for char in blocks[first_free_space_index:]:
        if char != '.':
            return False
    return True

def switch_end_block_with_first_free_space(blocks):
    first_free_space_index = blocks.index('.')
    for i in reversed(range(len(blocks))):
        char = blocks[i]
        if char != '.':
            blocks[first_free_space_index] = char
            blocks[i] = '.'
            return blocks

def calculate_checksum(blocks):
    sum = 0
    for i, char in enumerate(blocks):
        if char != '.':
            sum += i * int(char)
    return sum

if __name__ == '__main__':
    with open('9/day_9_input.txt', 'r') as f:
        contents = f.read()

    blocks = convert_disk_map_to_blocks(contents)
    print(blocks)
    blocks = compact_entire_filesystem(blocks)
    num = calculate_checksum(blocks)
    print(num)
