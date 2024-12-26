from pseudorandom import get_2000th


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        nums = [int(line) for line in f.readlines()]

    part_one_value = sum(s.value for s in map(get_2000th, nums))
    print(f"part one: {part_one_value}")
