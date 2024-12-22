def parse_input(contents):
    secret_numbers = []
    for line in contents.split('\n'):
        if line:
            secret_numbers.append(int(line))
    return secret_numbers

def calculate_secret_number(secret):
    first_result = prune(mix(secret * 64, secret))
    second_result = prune(mix(first_result // 32, first_result))
    return prune(mix(second_result * 2048, second_result))

def mix(a, b):
    return bitwise_xor(a, b)

def bitwise_xor(a, b):
    return a ^ b

def prune(secret):
    return secret % 16777216

if __name__ == '__main__':
    with open('22/day_22_input.txt', 'r') as f:
        contents = f.read()

    secret_numbers = parse_input(contents)
    for i in range(2000):
        secret_numbers = [calculate_secret_number(n) for n in secret_numbers]
    print(sum(secret_numbers))
