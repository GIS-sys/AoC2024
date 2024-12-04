class Field:
    def __init__(self):
        self.cells = []
        self.width = 0
        self.height = 0

    def read(self):
        self.cells = []
        self.width = 0
        self.height = 0
        while i := input():
            self.cells.append(i)
        if self.cells:
            self.height = len(self.cells)
            self.width = len(self.cells[0])

    def get(self, x: int, y: int, default: str = ""):
        if 0 <= x and x < self.width and 0 <= y and y < self.height:
            return self.cells[y][x]
        return default

    def subs(self, x: int, y: int, length: int, dirx: int, diry: int):
        result_list = [self.get(x+delta*dirx, y+delta*diry) for delta in range(length)]
        return "".join(result_list)

    def hor(self, x: int, y: int, length: int) -> str:
        return self.subs(x, y, length, 1, 0)

    def ver(self, x: int, y: int, length: int) -> str:
        return self.subs(x, y, length, 0, 1)

    def ld(self, x: int, y: int, length: int) -> str:
        return self.subs(x, y, length, -1, 1)

    def rd(self, x: int, y: int, length: int) -> str:
        return self.subs(x, y, length, 1, 1)


class Solver:
    def __init__(self):
        self.field = Field()

    def read(self):
        self.field.read()
        # print(self.field.hor(1, 1, 4))
        # print(self.field.ver(1, 1, 4))
        # print(self.field.ld(1, 1, 4))
        # print(self.field.rd(1, 1, 4))

    def solve(self):
        result = 0
        for x in range(self.field.width):
            for y in range(self.field.height):
                if self.field.rd(x-1, y-1, 3) in ["MAS", "SAM"] and self.field.ld(x+1, y-1, 3) in ["MAS", "SAM"]:
                    result += 1
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

