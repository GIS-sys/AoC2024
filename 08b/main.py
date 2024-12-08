def group(items: list, key_foo) -> dict:
    groups = dict()
    for item in items:
        key = key_foo(item)
        if not key in groups:
            groups[key] = []
        groups[key].append(item)
    return groups

def gcd(x: int, y: int) -> int:
    while y > 0:
        x, y = y, x % y
    return x

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
                    # calculate the minimal grid step for given antennas
                    step = (antenna_2.x - antenna_1.x, antenna_2.y - antenna_1.y)
                    step_divider = gcd(step[0], step[1])
                    step = (step[0] // step_divider, step[1] // step_divider)
                    # iterate in both directions to cover all field
                    x, y = antenna_1.x, antenna_1.y
                    while 0 <= x and x < width and 0 <= y and y < height:
                        antinodes[y][x] = True
                        x, y = x + step[0], y + step[1]
                    x, y = antenna_1.x, antenna_1.y
                    while 0 <= x and x < width and 0 <= y and y < height:
                        antinodes[y][x] = True
                        x, y = x - step[0], y - step[1]
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

