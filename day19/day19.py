from parser import parse_input


with open("input.txt", "r") as f:
    input_string = f.read().strip()

towels, designs = parse_input(input_string)

count_matchable = sum(1 for design in designs if towels.can_match(design))

print(f"part one: {count_matchable}")
