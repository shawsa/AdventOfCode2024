from parser import parse_input
from towels import TowelTree


with open("input.txt", "r") as f:
    input_string = f.read().strip()

towels, designs = parse_input(input_string)
tree = TowelTree.from_towels(towels)

count_matchable = sum(1 for design in designs if tree.can_match(design))

print(f"part one: {count_matchable}")


num_matches = sum(tree.count_matches(design) for design in designs)
print(f"part two: {num_matches}")
