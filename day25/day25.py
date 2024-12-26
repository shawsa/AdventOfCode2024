from parser import parse_to_locks_and_keys
from locks_and_keys import overlap
from itertools import product

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        locks, keys = parse_to_locks_and_keys(f.read())

    num_fit = sum(1 for lock, key in product(locks, keys) if not overlap(lock, key))

    print(f"part one: {num_fit}")
