from enum import StrEnum
from typing import Generator


class Stripe(StrEnum):
    WHITE = "w"
    BLUE = "u"
    BLACK = "b"
    RED = "r"
    GREEN = "g"


# forward declaration
class StripePattern:
    pass


class StripePattern:
    def __init__(self, stripes: tuple[Stripe]):
        self.stripes = stripes

    @classmethod
    def from_str(cls, string: str) -> StripePattern:
        return cls(tuple(Stripe(c) for c in string))

    def __str__(self) -> str:
        return "".join(stripe.value for stripe in self.stripes)

    def __repr__(self) -> str:
        return f"StripePattern[{str(self)}]"

    def __add__(self, pattern: StripePattern) -> StripePattern:
        return StripePattern(self.stripes + pattern.stripes)

    def __iter__(self):
        return iter(self.stripes)

    def __getitem__(self, index) -> Stripe:
        return self.stripes[index]

    def __len__(self) -> int:
        return len(self.stripes)

    def __eq__(self, pattern: StripePattern) -> bool:
        return tuple(self) == tuple(pattern)

    def partial_match(self, pattern) -> bool:
        """Returns true if pattern can be truncated to self."""
        if len(self) > len(pattern):
            return False
        if self == pattern[: len(self)]:
            return True
        return False


class Towel(StripePattern):
    def __repr__(self) -> str:
        return f"Towel[{str(self)}]"


class Design(StripePattern):
    def __repr__(self) -> str:
        return f"Design[{str(self)}]"


class TowelSet:
    def __init__(self, towels: list[Towel]):
        self.towels = towels

    def __iter__(self):
        return iter(self.towels)

    def __repr__(self) -> str:
        return f'TowelSet[{", ".join(str(towel) for towel in self.towels)}]'

    def pattern_matches(
        self, target: StripePattern
    ) -> Generator[list[Towel], None, None]:
        """For the target pattern, return all possible ways to create the pattern"""

        def recur(previous_towels: list[Towel]) -> list[Towel]:
            my_pattern = sum(previous_towels, Towel(tuple()))
            if my_pattern == target:
                yield previous_towels
            else:
                if my_pattern.partial_match(target):
                    for towel in self:
                        yield from recur(previous_towels + [towel])

        yield from recur([])

    def can_match(self, target: StripePattern) -> bool:
        try:
            next(self.pattern_matches(target))
            return True
        except StopIteration:
            return False
