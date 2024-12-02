from itertools import pairwise

Report = list[int]


def load_reports() -> list[Report]:
    with open("input.txt") as f:
        lines = f.readlines()

    return [[int(val) for val in line.split(" ")] for line in lines]


def is_decreasing(report: Report) -> bool:
    return all(a > b for a, b in pairwise(report))


def is_increasing(report: Report) -> bool:
    return all(a < b for a, b in pairwise(report))


def small_difference(report: Report) -> bool:
    return all(1 <= abs(a - b) <= 3 for a, b in pairwise(report))


def is_safe(report: Report):
    return small_difference(report) and (is_increasing(report) or is_decreasing(report))


def part_one(reports: list[Report]) -> int:
    num_safe = sum(is_safe(report) for report in reports)
    return num_safe


if __name__ == "__main__":
    reports = load_reports()
    num_safe = part_one(reports)
    print(f"{num_safe=}")
