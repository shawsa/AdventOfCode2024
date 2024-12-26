from monkey import total_price_dict
from pseudorandom import get_2000th


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        nums = [int(line) for line in f.readlines()]

    part_one_value = sum(s for s in map(get_2000th, nums))
    print(f"part one: {part_one_value}")

    totals = total_price_dict(nums, 2001, 4)
    pairs = list(totals.items())
    pairs.sort(key=lambda pair: pair[1])
    chages, price = pairs[-1]
    print(f"part two: {price}")
