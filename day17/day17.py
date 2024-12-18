from chronospatial_computer import (
    run_program,
    generate_state_sequence,
    Program,
    State,
)
from dataclasses import asdict
from parser import program_info
from tqdm import tqdm


def outputs_program(initial_state: State, program: Program) -> bool:
    for state in generate_state_sequence(initial_state, program):
        if state.output != program[: len(state.output)]:
            return False
    return state.output == program


def search_for_A(
    template_state: State, program: Program, candidates=range(1_000_000)
) -> int | None:
    for A in tqdm(candidates):
        my_dict = asdict(template_state)
        my_dict["A"] = A
        state = State(**my_dict)
        if outputs_program(state, program):
            return state
    return None


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        string = f.read().strip()
    initial_state, program = program_info.parse(string)
    part_one_output = run_program(initial_state, program)
    print("part_one:")
    print(part_one_output)
    print("searching for part two")
    print("part_two:")
    print(search_for_A(initial_state, program, candidates=range(10**7, 10**8)))
