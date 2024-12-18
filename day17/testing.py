from chronospatial_computer import (
    generate_state_sequence,
    run_program,
    State,
)
from day17 import (
    outputs_program,
    search_for_A,
)
from parser import program_info


test_string = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

initial_state, program = program_info.parse(test_string)

state = search_for_A(initial_state, program)
print(state)


outputs_program(initial_state, program)

for state in generate_state_sequence(initial_state, program):
    print(state)


print(run_program(initial_state, program))
