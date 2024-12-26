from computer_network import Network


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        network = Network.from_string(f.read().strip())

    num_traingles_with_t = sum(
        1 for triangle in network.triangles() if any(c.name[0] == "t" for c in triangle)
    )
    print(f"part one: {num_traingles_with_t}")
