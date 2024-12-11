import time
from typing import Optional


DEBUG = True
DEBUG_CHECK_SHORTCUTS = False
SYM_GUARD = "^"
SYM_WALL = "#"
SYM_EMPTY = "."
SYM_USED = "X"

def hash(pair: tuple[int, int]) -> int:
    return pair[0] * 3 + pair[1]

def copy(x: list[list]) -> list[list]:
    return [[b for b in a] for a in x]


class Solver:
    def __init__(self):
        self.field = None
        self.field_shortcuts_to_walls = None
        self.x, self.y = 0, 0
        self.width, self.height = 0, 0

    def read(self):
        field = []
        while i := input():
            if SYM_GUARD in i:
                self.y = len(field)
                self.x = i.index(SYM_GUARD)
            field.append(list(i))
        self.field = field
        self.width = len(self.field[0])
        self.height = len(self.field)
        self.recalculate_shortcuts()

    def recalculate_shortcuts_hor(self, y: int):
        last_wall_x = None
        for x in range(0, self.width, 1):
            self.field_shortcuts_to_walls[y][x][hash((-1, 0))] = last_wall_x, y
            if self.field[y][x] == SYM_WALL:
                last_wall_x = x + 1
        last_wall_x = None
        for x in range(self.width - 1, -1, -1):
            self.field_shortcuts_to_walls[y][x][hash((1, 0))] = last_wall_x, y
            if self.field[y][x] == SYM_WALL:
                last_wall_x = x - 1

    def recalculate_shortcuts_ver(self, x: int):
        last_wall_y = None
        for y in range(0, self.height, 1):
            self.field_shortcuts_to_walls[y][x][hash((0, -1))] = x, last_wall_y
            if self.field[y][x] == SYM_WALL:
                last_wall_y = y + 1
        last_wall_y = None
        for y in range(self.height - 1, -1, -1):
            self.field_shortcuts_to_walls[y][x][hash((0, 1))] = x, last_wall_y
            if self.field[y][x] == SYM_WALL:
                last_wall_y = y - 1

    def recalculate_shortcuts(self):
        self.field_shortcuts_to_walls = [[dict() for __ in range(self.height)] for _ in range(self.width)]
        for y in range(self.height):
            self.recalculate_shortcuts_hor(y)
        for x in range(self.width):
            self.recalculate_shortcuts_ver(x)

    def move(self, point: tuple[int, int], dir: tuple[int, int]) -> tuple[Optional[int], Optional[int]]:
        x, y = point
        result = self.field_shortcuts_to_walls[y][x][hash(dir)]

        if DEBUG_CHECK_SHORTCUTS:
            x, y = point
            while x >= 0 and x < self.width and y >= 0 and y < self.height and self.field[y][x] != SYM_WALL:
                x += dir[0]
                y += dir[1]
            if x >= 0 and x < self.width and y >= 0 and y < self.height:
                result_easy = x - dir[0], y - dir[1]
            else:
                result_easy = None, None

            if result != result_easy and (sum([_ is None for _ in result]) > 0) ^ (sum([_ is None for _ in result_easy]) > 0):
                print("!!!!!!!!!!")
                for line in self.field:
                    print(line)
                for line in self.field_shortcuts_to_walls:
                    print(line)
                print(point, dir)
                print(result, result_easy)
                exit()

        return result

    def check_loop(self, fill_path_field: bool) -> bool:
        field = self.field
        if fill_path_field:
            field = copy(self.field)
        x = self.x
        y = self.y

        dir = (0,-1)
        if fill_path_field:
            field[y][x] = SYM_USED
        #used = [[set() for __ in range(self.width)] for _ in range(self.height)]
        used = dict()

        while x >= 0 and x < self.width and y >= 0 and y < self.height and hash(dir) not in used.get((y, x), set()):#used[y][x]:
            #used[y][x].add(hash(dir))
            used[(y, x)] = used.get((y, x), set()) | set([hash(dir)])
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
                    field[lasty][lastx] = SYM_USED
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
                if original_field[i][j] != SYM_USED:
                    continue
                # check whether adding a wall will create a loop
                prev_symbol = self.field[i][j]
                self.field[i][j] = SYM_WALL
                self.recalculate_shortcuts_hor(i)
                self.recalculate_shortcuts_ver(j)
                loop, _ = self.check_loop(fill_path_field=False)
                self.field[i][j] = prev_symbol
                self.recalculate_shortcuts_hor(i)
                self.recalculate_shortcuts_ver(j)
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

