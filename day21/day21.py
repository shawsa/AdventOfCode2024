from keypad import Chain

with open("input.txt", "r") as f:
    codes = f.read().strip().split("\n")

chain = Chain(3)
print(f"part one: {sum(chain.complexity(code) for code in codes)}")
