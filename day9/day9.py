DiskMap = str
Blocks = list[int | None]

FREE_SPACE = None


def load_input() -> DiskMap:
    with open("input.txt", "r") as f:
        string = f.read().strip()
    return string


def disk_map_to_blocks(dm: DiskMap) -> Blocks:
    index = 0
    is_free_space = False
    blocks = []
    for num_blocks in map(int, dm):
        if is_free_space:
            blocks += [FREE_SPACE for _ in range(num_blocks)]
        else:
            blocks += [index for _ in range(num_blocks)]
            index += 1
        is_free_space = not is_free_space

    return blocks


def defrag_blocks(input_blocks: Blocks) -> Blocks:
    blocks = input_blocks.copy()

    def swap(index1, index2):
        blocks[index1], blocks[index2] = blocks[index2], blocks[index1]

    head = 0
    tail = len(blocks) - 1
    while head < tail:
        # seek so head is next free space
        while blocks[head] is not FREE_SPACE:
            head += 1
        # seek so tail is last data value
        while tail > head and blocks[tail] is FREE_SPACE:
            tail -= 1
        swap(head, tail)

    return blocks


def checksum(blocks: Blocks):
    total = 0
    for block_pos, file_id in enumerate(blocks):
        if file_id is None:
            break
        total += block_pos * file_id
    return total


def part_one() -> int:
    string = load_input()
    blocks = disk_map_to_blocks(string)
    defraged = defrag_blocks(blocks)
    return checksum(defraged)


if __name__ == "__main__":
    print(f"part_one: {part_one()}")
