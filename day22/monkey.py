from collections import defaultdict
from itertools import pairwise, tee, islice
from more_itertools import windowed, take
from tqdm import tqdm
from typing import Generator

from pseudorandom import secrets


def differences(seq: Generator[int, None, None]) -> Generator[int, None, None]:
    for num1, num2 in pairwise(seq):
        yield num2 - num1


def consecutive_changes(
    seq: Generator[int, None, None],
    window_width: int,
) -> Generator[tuple[int], None, None]:
    return windowed(differences(seq), 4)


def prices(initial_secret: int) -> Generator[int, None, None]:
    for num in secrets(initial_secret):
        yield num % 10


def price_and_changes(
    initial_secret: int, num_secrets, window_width: int
) -> Generator[tuple[int, tuple[int]], None, None]:
    my_prices = take(num_secrets, prices(initial_secret))
    prices1, prices2 = tee(my_prices)
    yield from zip(
        islice(prices1, window_width, None, 1),
        consecutive_changes(prices2, window_width),
    )


def first_price_dict(
    initial_secret: int,
    num_secrets,
    window_width: int,
) -> dict[tuple[int], int]:
    first_prices = {}
    for price, changes in price_and_changes(initial_secret, num_secrets, window_width):
        if changes in first_prices.keys():
            continue
        first_prices[changes] = price
    return first_prices


def total_price_dict(
    initial_secrets: list[int],
    num_secrets: int,
    window_width: int,
) -> dict[tuple[int], int]:
    totals = defaultdict(int)
    for inital_secret in tqdm(initial_secrets):
        my_dict = first_price_dict(inital_secret, num_secrets, window_width)
        for key, value in my_dict.items():
            totals[key] += value
    return totals
