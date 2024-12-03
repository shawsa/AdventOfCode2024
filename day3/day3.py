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


def eval_and_sum(memory: str) -> int:
    ops = find_mul_ops(memory)
    products = map(eval_mul_op, ops)
    total = sum(products)
    return total


def extract_do_blocks(memory: str) -> list[str]:
    for chunk in memory.split("do()"):
        yield chunk.split("don't()")[0]


def eval_and_sum_enabled(memory: str) -> int:
    return sum(eval_and_sum(do_block) for do_block in extract_do_blocks(memory))


if __name__ == "__main__":
    memory = load_input()
    print(f"part one: {eval_and_sum(memory)}")
    print(f"part two: {eval_and_sum_enabled(memory)}")
