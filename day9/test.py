from day9 import (
    disk_map_to_blocks,
    defrag_blocks,
    checksum,
)


string = "2333133121414131402"
string = "12345"
blocks = disk_map_to_blocks(string)
new_blocks = defrag_blocks(blocks)
print(checksum(new_blocks))
