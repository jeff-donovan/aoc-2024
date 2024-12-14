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

    return switch_file_with_free_space(blocks, free_space_index, file_id, file_index, file_size)

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

def switch_file_with_free_space(blocks, free_space_index, file_id, file_index, file_size):
    for i in range(file_size):
        blocks[free_space_index + i] = file_id
        blocks[file_index + i] = '.'
    return blocks

def calculate_checksum(blocks):
    sum = 0
    for i, char in enumerate(blocks):
        if char != '.':
            sum += i * char
    return sum

if __name__ == '__main__':
    with open('9/day_9_input.txt', 'r') as f:
        contents = f.read()

    blocks = compact_entire_filesystem(contents)
    num = calculate_checksum(blocks)
    print(num)
