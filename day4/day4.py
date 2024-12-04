import numpy as np
from itertools import product, chain
from typing import Generator


def load_input():
    with open("input.txt", "r") as f:
        lines = f.readlines()
    return np.array([[c for c in line[:-1]] for line in lines])


def all_horizontal(mat: np.ndarray[str], word_len) -> Generator[str, None, None]:
    rows, cols = mat.shape
    for row, col in product(range(rows), range(cols - word_len + 1)):
        yield "".join(mat[row, col + k] for k in range(word_len))


def all_vertical(mat: np.ndarray[str], word_len) -> Generator[str, None, None]:
    yield from all_horizontal(mat.T, word_len)


def all_forward_diagonal(mat: np.ndarray[str], word_len) -> Generator[str, None, None]:
    rows, cols = mat.shape
    for row, col in product(range(rows - word_len + 1), range(cols - word_len + 1)):
        yield "".join(mat[row + k, col + k] for k in range(word_len))


def all_backward_diagonal(mat: np.ndarray[str], word_len) -> Generator[str, None, None]:
    yield from all_forward_diagonal(mat[:, ::-1], word_len)


def also_reversed(seq: Generator[str, None, None]) -> Generator[str, None, None]:
    for word in seq:
        yield word
        yield word[::-1]


def all_possible_words(mat: np.ndarray[str], word_len) -> Generator[str, None, None]:
    return also_reversed(
        chain(
            all_horizontal(mat, word_len),
            all_vertical(mat, word_len),
            all_forward_diagonal(mat, word_len),
            all_backward_diagonal(mat, word_len),
        )
    )


def count_matches(mat: np.ndarray[str], target: str) -> int:
    return sum(word == target for word in all_possible_words(mat, len(target)))


X_mask = np.array(
    [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1],
    ],
    dtype=bool,
)
TARGETS = tuple(
    "".join((np.array(list(text.replace("\n", ""))).reshape(3, 3)[X_mask]))
    for text in [
        """
M.S
.A.
M.S""",
        """
S.S
.A.
M.M""",
        """
S.M
.A.
S.M""",
        """
M.M
.A.
S.S""",
    ]
)


def get_crosses(mat: np.ndarray[str]) -> Generator[str, None, None]:
    rows, cols = mat.shape
    for row, col in product(range(rows - 2), range(cols - 2)):
        yield mat[row : row + 3, col : col + 3]


def is_match(cross: np.ndarray[str]) -> bool:
    return "".join(cross[X_mask]) in TARGETS


def count_crosses(mat: np.ndarray[str]) -> int:
    return sum(is_match(cross) for cross in get_crosses(mat))


if __name__ == "__main__":
    word_search = load_input()
    target = "XMAS"
    print(f"part one: {count_matches(word_search, target)}")
    print(f"part two: {count_crosses(word_search)}")
