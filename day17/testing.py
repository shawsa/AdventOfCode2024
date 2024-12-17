from chronospatial_computer import (
    generate_state_sequence,
    run_program,
)
from parser import program_info


test_string = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

initial_state, program = program_info.parse(test_string)

for state in generate_state_sequence(initial_state, program):
    print(state)


print(run_program(initial_state, program))
