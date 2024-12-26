from collections import defaultdict, namedtuple
from dataclasses import dataclass


# forward declaration
class Computer:
    ...


@dataclass
class Computer:
    name: str

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return self.name

    def __lt__(self, computer: Computer) -> bool:
        return self.name < computer.name


@dataclass
class Connection:
    computer1: Computer
    computer2: Computer

    def __repr__(self) -> str:
        return f"{str(self.computer1)}-{str(self.computer2)}"

    def __iter__(self):
        return iter([self.computer1, self.computer2])


# forward declaration
class Network:
    ...


class Network:
    def __init__(self, connections: list[Connection]):
        self.connection_dict = defaultdict(set)
        self.add_connections(connections)

    def __str__(self) -> str:
        return (
            f"Network(computers={self.num_computers}, "
            + f"connections={self.num_connections})"
        )

    @property
    def num_computers(self) -> int:
        return len(self.connection_dict.keys())

    @property
    def num_connections(self) -> int:
        return sum(len(neighbors) for neighbors in self.connection_dict.values()) // 2

    @property
    def computers(self) -> list[Computer]:
        return list(self.connection_dict.keys())

    @property
    def connections(self) -> list[Connection]:
        connections = []
        for c1, neighbors in self.connection_dict.items():
            for c2 in neighbors:
                if c1.name > c2.name:
                    continue
                connections.append(Connection(c1, c2))
        return connections

    def add_connections(self, connections: list[Connection]) -> None:
        for c1, c2 in connections:
            self.connection_dict[c1].add(c2)
            self.connection_dict[c2].add(c1)

    @classmethod
    def from_string(cls, string) -> Network:
        lines = string.strip().split("\n")
        connections = []
        for line in lines:
            c1, c2 = line.split("-")
            connections.append(Connection(Computer(c1), Computer(c2)))
        return Network(connections)

    def triangles(self) -> set[tuple[Computer, Computer, Computer]]:
        triangles = set()
        for c1 in self.computers:
            for c2 in self.connection_dict[c1]:
                for c3 in self.connection_dict[c2]:
                    if c3 == c1:
                        continue
                    if c1 in self.connection_dict[c3]:
                        triangle = tuple(sorted([c1, c2, c3]))
                        triangles.add(triangle)
        return triangles
