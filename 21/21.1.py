import pprint


def make_codes(contents):
    return [[char for char in line] for line in contents.split('\n') if line]

if __name__ == '__main__':
    with open('21/day_21_input.txt', 'r') as f:
        contents = f.read()

    codes = make_codes(contents)
    pprint.pprint(codes)
