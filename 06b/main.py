from typing import Optional


DEBUG = True

def hash(pair: tuple[int, int]) -> int:
    return pair[0] * 3 + pair[1]

def copy(x: list[list]) -> list[list]:
    return [[b for b in a] for a in x]


#class Field:
#    def __init__(self, field: list[list[int]]):
#        pass
#
#    d

class Solver:
    def __init__(self):
        self.field = None
        self.x, self.y = 0, 0
        self.width, self.height = 0, 0

    def read(self):
        field = []
        while i := input():
            if "^" in i:
                self.y = len(field)
                self.x = i.index("^")
            field.append(list(i))
        self.field = field
        self.width = len(self.field[0])
        self.height = len(self.field)

    def move(self, point: tuple[int, int], dir: tuple[int, int]) -> tuple[Optional[int], Optional[int]]:
        x, y = point
        while x >= 0 and x < self.width and y >= 0 and y < self.height and self.field[y][x] != "#":
            x += dir[0]
            y += dir[1]
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return x - dir[0], y - dir[1]
        return None, None

    def check_loop(self, fill_path_field: bool) -> bool:
        field = self.field
        if fill_path_field:
            field = copy(self.field)
        x = self.x
        y = self.y

        dir = (0,-1)
        if fill_path_field:
            field[y][x] = "X"
        used = [[set() for __ in range(self.width)] for _ in range(self.height)]

        while x >= 0 and x < self.width and y >= 0 and y < self.height and hash(dir) not in used[y][x]:
            used[y][x].add(hash(dir))
            if fill_path_field:
                lastx, lasty = x, y
            x, y = self.move((x, y), dir)
            # mark as visited if required
            if fill_path_field:
                while lastx != x or lasty != y:
                    lastx += dir[0]
                    lasty += dir[1]
                    if not(0 <= lastx and lastx < self.width and 0 <= lasty and lasty < self.height):
                        break
                    field[lasty][lastx] = "X"
            if x is None or y is None:
                break
            # turn
            dir = (-dir[1], dir[0])

        # calculate result
        if x is None or y is None:
            return False, field
        return True, field
    
    def solve(self):
        result = 0
        # find out cells where guard is walking originally
        _, original_field = self.check_loop(fill_path_field=True)
        # try placing walls on guards' path
        for i in range(len(self.field)):
            for j in range(len(self.field[0])):
                # skip placing wall on top of the guard
                if i == self.y and j == self.x:
                    continue
                # skip placing wall where guard is not walking
                if original_field[i][j] != "X":
                    continue
                # check whether adding a wall will create a loop
                prev_symbol = self.field[i][j]
                self.field[i][j] = "#"
                loop, _ = self.check_loop(fill_path_field=False)
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

