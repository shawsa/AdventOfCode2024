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
        return StripePattern(self.stripes[index])

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

    def __hash__(self) -> int:
        return hash(self.stripes)


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

    def __getitem__(self, index) -> Towel:
        return self.towels[index]

    def __repr__(self) -> str:
        return f'TowelSet[{", ".join(str(towel) for towel in self.towels)}]'

    def pattern_matches(
        self, target: StripePattern
    ) -> Generator[list[Towel], None, None]:
        """For the target pattern, return all possible ways to create the pattern

        This is too slow. Maybe I can make some sort of forest of towels to make
        searching the paths faster.
        """

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


class RootTowel(Towel):
    def __init__(self):
        super().__init__(tuple())

    def partial_match(self, target: Towel) -> bool:
        return True


# forward declaration
class TowelTree:
    pass


class TowelTree:
    def __init__(self, root: Towel = RootTowel(), children: list[TowelTree] = None):
        if children is None:
            children = list()
        self.root = root
        self.children = children
        self._initialize_count_cache()

    def _initialize_count_cache(self) -> None:
        self.count_cache = {}

    def _to_lines(self, indent) -> Generator[str, None, None]:
        if isinstance(self.root, RootTowel):
            yield "TowelTree:"
        else:
            yield str(self.root)
        for child in self.children:
            for line in child._to_lines(indent):
                yield indent + line

    def __str__(self) -> str:
        return "\n".join(self._to_lines("  "))

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def is_decendant_of(self, towel: Towel) -> bool:
        if isinstance(self, RootTowel):
            return False
        return towel.partial_match(self.root)

    def is_ancestor_of(self, towel: Towel) -> bool:
        if isinstance(self, RootTowel):
            return True
        return self.root.partial_match(towel)

    def add(self, target: Towel) -> bool:
        """Add the target towel to the tree and return True if successful."""
        if self.is_decendant_of(target):
            new_tree = TowelTree(self.root, self.children)
            self.root = target
            self.children = [new_tree]
            return True
        elif self.is_ancestor_of(target):
            is_grandchild = False
            for child in self.children:
                if child.add(target):
                    is_grandchild = True
                    break
            if not is_grandchild:
                self.children.append(TowelTree(target))
            return True
        else:
            return False

    @classmethod
    def from_towels(cls, towels: list[Towel]):
        tree = TowelTree()
        for towel in towels:
            tree.add(towel)
        tree.sort()
        tree._initialize_count_cache()
        return tree

    def sort(self):
        self.children.sort(key=lambda tt: str(tt.root))
        for child in self.children:
            child.sort()

    def partial_matches(
        self, pattern: StripePattern
    ) -> Generator[tuple[Towel, StripePattern], None, None]:
        if self.root.partial_match(pattern):
            if not isinstance(self.root, RootTowel):
                next_pattern = pattern[len(self.root) :]
                yield self.root, next_pattern
            for child in self.children:
                yield from child.partial_matches(pattern)

    def pattern_matches(
        self, target: StripePattern
    ) -> Generator[list[Towel], None, None]:
        for match, remaining in self.partial_matches(target):
            if len(remaining) == 0:
                yield [match]
            else:
                for remaining_match in self.pattern_matches(remaining):
                    yield [match] + remaining_match

    def can_match(self, target: StripePattern) -> bool:
        try:
            next(self.pattern_matches(target))
            return True
        except StopIteration:
            return False

    def count_matches(self, pattern: StripePattern) -> int:
        if pattern in self.count_cache.keys():
            return self.count_cache[pattern]
        matches = 0
        for match, remaining in self.partial_matches(pattern):
            if len(remaining) == 0:
                matches += 1
            else:
                matches += self.count_matches(remaining)
        self.count_cache[pattern] = matches
        return matches
