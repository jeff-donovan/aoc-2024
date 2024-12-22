# store all secret numbers for each initial secret number
# calculate "price" - the secret number (modulo 10) AT the 4th price change
# store all price changes
# AS you are storing price changes... track all possible 4-change sequences
# (AND the index/second where the sequence happened within the 2000 secret number set)
# 

def parse_input(contents):
    secret_numbers = []
    for line in contents.split('\n'):
        if line:
            secret_numbers.append([int(line)])
    return secret_numbers

def calculate_secret_number(secret):
    first_result = prune(mix(secret * 64, secret))
    second_result = prune(mix(first_result // 32, first_result))
    return prune(mix(second_result * 2048, second_result))

def calculate_all_prices(secret_num_sequence):
    return [n % 10 for n in secret_num_sequence]

def mix(a, b):
    return bitwise_xor(a, b)

def bitwise_xor(a, b):
    return a ^ b

def prune(secret):
    return secret % 16777216

if __name__ == '__main__':
    with open('22/day_22_test.txt', 'r') as f:
        contents = f.read()

    secret_numbers = parse_input(contents)
    for i in range(2000):
        for n, secret_num_sequence in enumerate(secret_numbers):
            secret_num_sequence.append(calculate_secret_number(secret_num_sequence[-1]))
            secret_numbers[n] = secret_num_sequence

    price_sequences = [calculate_all_prices(seq) for seq in secret_numbers]
