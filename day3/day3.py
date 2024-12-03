import re


def load_input():
    with open("input.txt", "r") as f:
        memory = f.read()
    return memory


def find_mul_ops(memory: str) -> list[str]:
    return re.findall("mul\\([0-9]*,[0-9]*\\)", memory)


def eval_mul_op(op: str) -> int:
    args = [int(s) for s in op[4:-1].split(",")]
    return args[0] * args[1]


def part_one(memory: str) -> int:
    ops = find_mul_ops(memory)
    products = map(eval_mul_op, ops)
    total = sum(products)
    return total


if __name__ == "__main__":
    memory = load_input()
    print(f"part one: {part_one()}")
