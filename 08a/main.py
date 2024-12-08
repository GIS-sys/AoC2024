def group(items: list, key_foo) -> dict:
    groups = dict()
    for item in items:
        key = key_foo(item)
        if not key in groups:
            groups[key] = []
        groups[key].append(item)
    return groups

class Antenna:
    def __init__(self, x: int, y: int, frequency: str):
        self.x = x
        self.y = y
        self.frequency = frequency

    def __repr__(self) -> str:
        return f"(x={self.x} y={self.y} f={self.frequency})"

class Antennas:
    def __init__(self, antennas: list[Antenna]):
        self.grouped_antennas = group(antennas, lambda x: x.frequency)

    def get_antinodes_map(self, width: int, height: int) -> list[list[bool]]:
        antinodes = [[False for __ in range(width)] for _ in range(height)]
        for group in self.grouped_antennas.values():
            for i, antenna_1 in enumerate(group):
                for j, antenna_2 in enumerate(group[i+1:]):
                    possible_positions = [
                        (antenna_2.x * 2 - antenna_1.x, antenna_2.y * 2 - antenna_1.y),
                        (antenna_1.x * 2 - antenna_2.x, antenna_1.y * 2 - antenna_2.y),
                    ]
                    for x, y in possible_positions:
                        if 0 <= x and x < width and 0 <= y and y < height:
                            antinodes[y][x] = True
        return antinodes

class Solver:
    def __init__(self):
        self.antennas = None
        self.width = 0
        self.height = 0

    def read(self):
        self.width = 0
        self.height = 0
        antennas_list = []
        while i := input():
            for x in range(len(i)):
                if i[x]== ".":
                    continue
                antennas_list.append(Antenna(x, self.height, i[x]))
            self.width = len(i)
            self.height += 1
        self.antennas = Antennas(antennas_list)

    def solve(self):
        antinodes = self.antennas.get_antinodes_map(self.width, self.height)
        result = 0
        for line in antinodes:
            for v in line:
                if v:
                    result += 1
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

