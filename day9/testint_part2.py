from day9_part_two import (
    DiskMap,
)


string = "2333133121414131402"
dm = DiskMap(string)
print(dm)
dm.defragment()
print(dm)
print(dm.check_sum())
