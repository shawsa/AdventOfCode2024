from chronospatial_computer import (
    run_program,
    generate_state_sequence,
    Program,
    State,
)
from parser import program_info
from assembly import generate_A


def outputs_program(initial_state: State, program: Program) -> bool:
    for state in generate_state_sequence(initial_state, program):
        if state.output != program[: len(state.output)]:
            return False
    return state.output == program


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        string = f.read().strip()
    initial_state, program = program_info.parse(string)
    print(f"part_one: {run_program(initial_state, program)}")
    print(f"part_two: {generate_A(program)}")
