from collections import defaultdict
from functools import partial
from itertools import combinations, filterfalse
from typing import Callable


def load_input(file_name: str):
    with open(file_name, "r") as f:
        lines = f.readlines()
    after_dict = defaultdict(list)
    updates = []
    seq = iter(lines)
    for line in seq:
        if line == "\n":
            break
        before, after = map(int, line.split("|"))
        after_dict[before].append(after)
    for line in seq:
        updates.append(list(map(int, line.split(","))))

    return after_dict, updates


Update = list[int]
RuleDict = dict[int, [list[int]]]


def order_filter(after_dict: RuleDict) -> Callable[[Update], bool]:
    def correct_order(update: Update) -> bool:
        return all(
            before not in after_dict[after] for before, after in combinations(update, 2)
        )

    return correct_order


def get_middle(update: list[int]) -> int:
    assert len(update) % 2 == 1
    return update[len(update) // 2]


def sum_middle_correct(updates: list[Update], after_dict: RuleDict) -> int:
    correct_updates = filter(order_filter(after_dict), updates)
    middles = map(get_middle, correct_updates)
    return sum(middles)


class OrderedPage:
    def __init__(self, num: int, after_dict: RuleDict):
        self.num = num
        self.rules = after_dict

    def __lt__(self, other_page) -> bool:
        return self.num not in self.rules[other_page.num]


def ordering(after_dict: RuleDict) -> Callable[[int], OrderedPage]:
    def ordered_page(num: int) -> OrderedPage:
        return OrderedPage(num, after_dict)

    return ordered_page


def sort_update(update: Update, after_dict: RuleDict) -> Update:
    return sorted(update, key=ordering(after_dict))


def sum_middle_fixed(updates: list[Update], after_dict: RuleDict) -> int:
    incorrect_updates = filterfalse(order_filter(after_dict), updates)
    sorter = partial(sort_update, after_dict=after_dict)
    fixed_updates = map(sorter, incorrect_updates)
    middles = map(get_middle, fixed_updates)
    return sum(middles)


if __name__ == "__main__":
    after_dict, updates = load_input("input.txt")
    print(f"part one: {sum_middle_correct(updates, after_dict)}")
    print(f"part two: {sum_middle_fixed(updates, after_dict)}")
