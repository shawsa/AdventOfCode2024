from keypad import NumericKeypad, RobotArm, Chain, button_sequence_to_str

NumericKeypad().shortest_paths("A", 4)

arm = RobotArm(NumericKeypad())
for seq in arm.input_strings("A", "029A"):
    print(seq)


codes =
    """029A
980A
179A
456A
379A""".split("\n")

chain = Chain(3)
sum(chain.complexity(code) for code in codes)
