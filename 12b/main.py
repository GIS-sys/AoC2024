DEBUG = False


class Group:
    def __init__(self, cells: list[tuple[int, int]]):
        self.cells = set(cells)

    def __repr__(self) -> str:
        return str(self.cells)

    def area(self) -> int:
        return len(self.cells)

    def perimeter(self) -> int:
        result = 0
        for x, y in self.cells:
            result += 4
            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                new_x, new_y = x + dx, y + dy
                if (new_x, new_y) in self.cells:
                    result -= 1
        return result

    def sides(self) -> int:
        SIDES = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        SIDE_CHECKERS = [(0, 1), (1, 0), (0, 1), (1, 0)]
        # calculate sides for each cell individually
        cell_sides = dict()
        for x, y in self.cells:
            cell_sides[(x, y)] = []
            for dx, dy in SIDES:
                new_x, new_y = x + dx, y + dy
                cell_sides[(x, y)].append(not ((new_x, new_y) in self.cells))
        # calculate amount of sides by ignoring all horizontal sides with cells to the left, vertical with cells to the top
        if DEBUG:
            print(cell_sides)
        result = 0
        for x, y in self.cells:
            for cell_side_index, (dx, dy) in enumerate(SIDE_CHECKERS):
                if not cell_sides[(x, y)][cell_side_index]:
                    continue
                new_x, new_y = x + dx, y + dy
                if not ((new_x, new_y) in self.cells):
                    result += 1
                    continue
                if cell_sides[(new_x, new_y)][cell_side_index]:
                    continue
                result += 1
        return result


class Solver:
    def __init__(self):
        self.field = []
        self.width = 0
        self.height = 0

    def read(self):
        self.field = []
        while i := input():
            self.field.append(list(i))
        self.width = len(self.field[0])
        self.height = len(self.field)

    def solve(self):
        # determine groups
        group_index = 0
        group_indexes = dict()
        for new_x in range(self.width):
            for new_y in range(self.height):
                if not ((new_x, new_y) in group_indexes):
                    bfs = [(new_x, new_y)]
                    group_indexes[(new_x, new_y)] = group_index
                    while bfs:
                        x, y = bfs[0]
                        bfs.pop(0)
                        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                            next_x, next_y = x + dx, y + dy
                            if 0 > next_x or next_x >= self.width:
                                continue
                            if 0 > next_y or next_y >= self.height:
                                continue
                            if self.field[y][x] != self.field[next_y][next_x]:
                                continue
                            if (next_x, next_y) in group_indexes:
                                continue
                            bfs.append((next_x, next_y))
                            group_indexes[(next_x, next_y)] = group_index
                    group_index += 1
        # create groups
        group_cells = [[] for _ in range(group_index)]
        for x in range(self.width):
            for y in range(self.height):
                index = group_indexes[(x, y)]
                group_cells[index].append((x, y))
        groups = [Group(g) for g in group_cells]
        # find perimeters and areas
        result = 0
        for group in groups:
            area = group.area()
            sides = group.sides()
            if DEBUG:
                print("Checking group:", group)
                print(f"{area=} {sides=}")
            result += area * sides
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

