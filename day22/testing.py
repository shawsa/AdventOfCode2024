from more_itertools import nth, take

from pseudorandom import SecretNumber, get_2000th

num = SecretNumber(123)

for num in take(11, num.sequence()):
    print(num)


test_nums = [1, 10, 100, 2024]

for num in test_nums:
    print(f"{num}: {get_2000th(num)}")


test_value = sum(s.value for s in map(get_2000th, test_nums))
