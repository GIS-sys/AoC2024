DEBUG = False


def copy(x: list[list]) -> list[list]:
    return [[b for b in a] for a in x]


class Solver:
    def __init__(self):
        self.field = []
        self.x, self.y = 0, 0
        self.width, self.height = 0, 0

    def read(self):
        while i := input():
            if "^" in i:
                self.y = len(self.field)
                self.x = i.index("^")
            self.field.append(list(i))
        self.width = len(self.field[0])
        self.height = len(self.field)

    def solve(self):
        field = copy(self.field)
        x = self.x
        y = self.y

        dir = (0,-1)
        field[y][x] = "X"

        while x >= 0 and x < self.width and y >= 0 and y < self.height:
            x += dir[0]
            y += dir[1]
            if not (x >= 0 and x < self.width and y >= 0 and y < self.height):
                break
            # if stepped onto the wall
            if field[y][x]=="#":
                # politely move back and turn right
                x -= dir[0]
                y -= dir[1]
                dir = (-dir[1], dir[0])
            else:
                # else mark as visited
                field[y][x]="X"

        # calculate result
        result = 0
        for line in field:
            result += line.count("X")
            if DEBUG:
                print("".join(line))
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

