import numpy as np
from day4 import count_matches, count_crosses

TEST_INPUT_STR = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

TEST_INPUT = np.array([list(line) for line in TEST_INPUT_STR.split("\n")])


assert count_matches(TEST_INPUT, "XMAS") == 18
assert count_crosses(TEST_INPUT) == 9
