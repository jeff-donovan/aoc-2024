import datetime


def make_codes(contents):
    return [line for line in contents.split('\n') if line]

if __name__ == '__main__':
    with open('day_21/day_21_input.txt', 'r') as f:
        contents = f.read()

    start = datetime.datetime.now()
    codes = make_codes(contents)
    print('took ', datetime.datetime.now() - start)
