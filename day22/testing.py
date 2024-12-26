from more_itertools import nth, take
from pseudorandom import SecretNumber, get_2000th
from monkey import total_price_dict

num = SecretNumber(123)

for num in take(11, num.sequence()):
    print(num)


test_nums = [1, 10, 100, 2024]

for num in test_nums:
    print(f"{num}: {get_2000th(num)}")


test_value = sum(s for s in map(get_2000th, test_nums))


totals = total_price_dict([1, 2, 3, 2024], 2001, 4)
pairs = list(totals.items())
pairs.sort(key=lambda pair: pair[1])
chages, price = pairs[-1]
