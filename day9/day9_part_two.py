from dataclasses import dataclass
from typing import Generator

from day9 import load_input


@dataclass
class File:
    id: int | None
    size: int

    def is_free(self):
        return self.id is None

    def is_empty(self):
        return self.size == 0

    def __str__(self):
        if self.is_free():
            return "." * self.size
        return "".join(str(self.id % 10) * self.size)

    def __hash__(self):
        return hash((self.id, self.size))


class DiskMap:
    def __init__(self, string):
        self.files = []
        index = 0
        is_free_space = False
        for num_blocks in map(int, string):
            if is_free_space:
                if num_blocks != 0:
                    self.files.append(File(None, num_blocks))
            else:
                self.files.append(File(index, num_blocks))
                index += 1
            is_free_space = not is_free_space

    def __str__(self) -> str:
        return "".join(str(file) for file in self.files)

    def num_files(self) -> int:
        return sum(not file.is_free() for file in self.files)

    def merge_free(self):
        files = []
        free_file = File(None, 0)
        for my_file in self.files:
            if my_file.is_free():
                free_file = File(None, free_file.size + my_file.size)
            else:
                if not free_file.is_empty():
                    files.append(free_file)
                    free_file = File(None, 0)
                files.append(my_file)
        self.files = files

    def defragment(self):
        for file_id in range(self.num_files() - 1, -1, -1):
            # find file
            for loc, file in enumerate(self.files):
                if file.id == file_id:
                    break
            # search for free space
            for free_id, free_space in enumerate(self.files[:loc]):
                if not free_space.is_free() or free_space.size < file.size:
                    continue
                # found free space
                self.files[loc] = File(None, file.size)
                self.files.pop(free_id)
                self.files.insert(free_id, file)
                if (new_size := free_space.size - file.size) > 0:
                    self.files.insert(free_id + 1, File(None, new_size))
                self.merge_free()
                break

    def blocks(self) -> Generator[int | None, None, None]:
        for file in self.files:
            for _ in range(file.size):
                yield file.id

    def check_sum(self) -> int:

        total = 0
        for block_id, file_id in enumerate(self.blocks()):
            if file_id is not None:
                total += block_id * file_id

        return total


def part_two() -> int:
    string = load_input()
    dm = DiskMap(string)
    dm.defragment()
    return dm.check_sum()


if __name__ == "__main__":
    print(f"part_two: {part_two()}")
