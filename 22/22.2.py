# DONE store all secret numbers for each initial secret number
# DONE calculate "price" - the secret number (modulo 10) AT the 4th price change
# DONE store all price changes
# DONE AS you are storing price changes... track all possible 4-change sequences

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

def calculate_price_change_combos(secret_num_sequence):
    combo_to_price = {}
    for i in range(4, len(secret_num_sequence)):
        first = secret_num_sequence[i - 3] - secret_num_sequence[i - 4]
        second = secret_num_sequence[i - 2] - secret_num_sequence[i - 3]
        third = secret_num_sequence[i - 1] - secret_num_sequence[i - 2]
        fourth = secret_num_sequence[i] - secret_num_sequence[i - 1]
        combo = (first, second, third, fourth)
        if combo not in combo_to_price:
            combo_to_price[combo] = secret_num_sequence[i]
    return combo_to_price

def mix(a, b):
    return bitwise_xor(a, b)

def bitwise_xor(a, b):
    return a ^ b

def prune(secret):
    return secret % 16777216

if __name__ == '__main__':
    with open('22/day_22_test_part2.txt', 'r') as f:
        contents = f.read()

    secret_numbers = parse_input(contents)
    print(secret_numbers)
    for i in range(2):
    # for i in range(2000):
        for n, secret_num_sequence in enumerate(secret_numbers):
            secret_num_sequence.append(calculate_secret_number(secret_num_sequence[-1]))
            secret_numbers[n] = secret_num_sequence

    print(secret_numbers)
    # print([secret_numbers[i][0] in range(len(secret_numbers))])

    # price_sequences = [calculate_all_prices(seq) for seq in secret_numbers]
    # price_change_combos = [calculate_price_change_combos(seq) for seq in secret_numbers]
    # # all_combos = set([])
    # # for combo_to_price in price_change_combos:
    # #     all_combos.update(set([combo for combo in combo_to_price]))

    # combo_bananas_mapping = {}
    # for combo_to_price in price_change_combos:
    #     for combo, price in combo_to_price.items():
    #         if combo not in combo_bananas_mapping:
    #             combo_bananas_mapping[combo] = 0
    #         combo_bananas_mapping[combo] += price

    # max_bananas = max([bananas for _, bananas in combo_bananas_mapping.items()])
    # print(max_bananas)
    # print(price_change_combos)
