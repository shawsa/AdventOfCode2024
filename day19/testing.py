from parser import parse_input
from towels import StripePattern

test_input = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""


towels, designs = parse_input(test_input)
for design in designs:
    print(design, towels.can_match(design))
