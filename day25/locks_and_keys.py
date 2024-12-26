class Key:
    def __init__(self, heights: list[int]):
        self.heights = heights

    def __repr__(self) -> str:
        return "Key(" + ", ".join(map(str, self.heights)) + ")"

    def __str__(self) -> str:
        cols = ["." * (6 - height) + "#" * (height + 1) for height in self.heights]
        rows = ["".join(row) for row in zip(*cols)]
        return "\n".join(rows)


class Lock:
    def __init__(self, heights: list[int]):
        self.heights = heights

    def __repr__(self) -> str:
        return "Lock(" + ", ".join(map(str, self.heights)) + ")"

    def __str__(self) -> str:
        cols = ["." * (6 - height) + "#" * (height + 1) for height in self.heights]
        rows = ["".join(row) for row in zip(*cols)]
        return "\n".join(reversed(rows))


def overlap(lock: Lock, key: Key) -> bool:
    return any(h1 + h2 > 5 for h1, h2 in zip(key.heights, lock.heights))
