from parser import parse_input
from towels import StripePattern, TowelTree, Towel

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
tree = TowelTree.from_towels(towels)
print(tree)
for design in designs:
    print(design, tree.can_match(design))

total = 0
for design in designs:
    total += len(list(tree.pattern_matches(design)))
print(total)

my_pattern = StripePattern.from_str("brb")
for match in tree.pattern_matches(my_pattern):
    print(match)
print(tree.count_matches(my_pattern))


print(sum(tree.count_matches(design) for design in designs))
