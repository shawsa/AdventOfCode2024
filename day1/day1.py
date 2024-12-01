from collections import defaultdict


def load_and_sort() -> list[str]:
    with open("input.txt", "r") as f:
        lines = f.readlines()
    string_pairs = [line.split("   ") for line in lines]
    int_pairs = [[int(num) for num in pair] for pair in string_pairs]
    left_list, right_list = zip(*int_pairs)
    return sorted(left_list), sorted(right_list)


def part_one() -> int:
    left_list, right_list = load_and_sort()
    total_distance = sum(
        abs(left - right) for left, right in zip(left_list, right_list)
    )
    return total_distance


def part_two() -> int:
    "O(n * M) method since it has a nested loop. Slow in theory."
    left_list, right_list = load_and_sort()
    total = 0
    for target in left_list:
        count = sum(num == target for num in right_list)
        total += target * count
    return total


def part_two_fast() -> int:
    "O(n + m)"
    left_list, right_list = load_and_sort()
    counts = defaultdict(lambda: 0)
    for num in right_list:
        counts[num] += 1
    total = 0
    for target in left_list:
        total += target * counts[target]
    return total


if __name__ == "__main__":
    print(f"part one solution: {part_one()}")
    assert part_two() == part_two_fast()
    print(f"part two solution: {part_two()}")
