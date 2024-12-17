from chronospatial_computer import run_program
from parser import program_info


with open("input.txt", "r") as f:
    string = f.read().strip()
initial_state, program = program_info.parse(string)
part_one_output = run_program(initial_state, program)
print("part_one:")
print(part_one_output)
