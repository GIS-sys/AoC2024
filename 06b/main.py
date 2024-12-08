DEBUG = True


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

    def check_loop(self) -> bool:
        field = copy(self.field)
        x = self.x
        y = self.y

        dir = (0,-1)
        field[y][x] = "X"
        used = [[set() for __ in _] for _ in field]

        while x >= 0 and x < self.width and y >= 0 and y < self.height and hash(dir) not in used[y][x]:
            used[y][x].add(hash(dir))
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
        if not (x >= 0 and x < self.width and y >= 0 and y < self.height):
            return False
        return True
    
    def solve(self):
        result = 0
        for i in range(len(self.field)):
            for j in range(len(self.field[0])):
                # skip placing wall on top of the guard
                if i == self.y and j == self.x:
                    continue
                # check whether adding a wall will create a loop
                prev_symbol = self.field[i][j]
                self.field[i][j] = "#"
                loop = self.check_loop()
                self.field[i][j] = prev_symbol
                if loop:
                    result += 1
            if DEBUG:
                print(f"{i}/{len(self.field)}")
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

