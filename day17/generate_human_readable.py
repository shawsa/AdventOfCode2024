from parser import program_info
from chronospatial_computer import generate_human_readable
with open("input.txt", "r") as f:
    string = f.read().strip()
initial_state, program = program_info.parse(string)

print(generate_human_readable(program))
