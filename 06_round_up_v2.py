import math


def round_up(amount, var_round_to):
    return int(math.ceil(amount / var_round_to)) * var_round_to


price = round_up(4.50, 2)
print(price)
