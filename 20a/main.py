DEBUG = False
SYMBOL_START = "S"
SYMBOL_END = "E"
SYMBOL_EMPTY = "."
SYMBOL_WALL = "#"
INFINITY = 1000 * 1000 * 1000
TIME_TO_SAVE = 100
#TIME_TO_SAVE = 12


class Solver:
    def __init__(self):
        self.field: list[list[str]] = None
        self.start: tuple[int, int] = None
        self.end: tuple[int, int] = None
        self.height: int = None
        self.width: int = None

    def read(self):
        y = 0
        self.field = []
        while i := input():
            self.field.append(list(i))
            if SYMBOL_START in i:
                x = i.index(SYMBOL_START)
                self.start = (x, y)
                self.field[y][x] = SYMBOL_EMPTY
            if SYMBOL_END in i:
                x = i.index(SYMBOL_END)
                self.end = (x, y)
                self.field[y][x] = SYMBOL_EMPTY
            y += 1
        self.height = len(self.field)
        self.width = len(self.field[0])

    def solve(self):
        result = 0
        # first find all regular distances to the end
        self.distances = [[INFINITY for _ in range(self.width)] for __ in range(self.height)]
        self.distances[self.end[1]][self.end[0]] = 0
        queue = [self.end]
        while queue:
            x, y = queue[0]
            queue.pop(0)
            if DEBUG:
                print(x, y, queue)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_x, next_y = x + dx, y + dy
                if not (0 <= next_x < self.width and 0 <= next_y < self.height):
                    continue
                if self.field[next_y][next_x] != SYMBOL_EMPTY:
                    continue
                if self.distances[next_y][next_x] == INFINITY:
                    queue.append((next_x, next_y))
                self.distances[next_y][next_x] = min(self.distances[next_y][next_x], self.distances[y][x] + 1)
        if DEBUG:
            print(self.distances)
        # now check each cell and find cheats when we save more than specified amount of time
        for x in range(self.width):
            for y in range(self.height):
                for dx1, dy1 in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    for dx2, dy2 in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        dx, dy = dx1 + dx2, dy1 + dy2
                        next_x, next_y = x + dx, y + dy
                        if not (0 <= next_x < self.width and 0 <= next_y < self.height):
                            continue
                        if self.field[y][x] != SYMBOL_EMPTY or self.field[next_y][next_x] != SYMBOL_EMPTY:
                            continue
                        time_save = self.distances[y][x] - self.distances[next_y][next_x] - 2
                        if time_save >= TIME_TO_SAVE:
                            if DEBUG:
                                print(f"Cheat from=({x},{y}) to=({next_x},{next_y}), with distance savings of {time_save} ({self.distances[y][x]} - {self.distances[next_y][next_x]})")
                            result += 1
        return result
        #amount_of_cheats = 1
        ## dp[y][x][m] = amount of ways to reach (x,y) with m uses of cheats
        #self.dp = [[[0 for ___ in range(amount_of_cheats + 1)] for _ in range(self.width)] for __ in range(self.height)]
        #self.dp[self.end[1]][self.end[0]] = [1 for ___ in range(amount_of_cheats + 1)]
        #to_update = [(self.end[0], self.end[1], 0)]
        #while to_update:
        #    x, y, m = to_update[0]
        #    to_update.pop(0)
        #    if DEBUG:
        #        print(x, y, m, to_update)
        #    # regular move
        #return sum(self.dp[self.start[1]][self.start[0]])


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

