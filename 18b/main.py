DEBUG = False
SIZE, LENGTH = 71, 1024
#SIZE, LENGTH = 7, 12


class Solver:
    def __init__(self):
        self.corruptions: list[tuple[int]] = None
        self.start = (0, 0)
        self.width = SIZE
        self.height = SIZE
        self.end = (SIZE - 1, SIZE - 1)

    def read(self):
        self.corruptions = []
        while i := input():
            x, y = map(int, i.split(","))
            self.corruptions.append((x, y))

    def find_path_length(self, length):
        # construct field
        blocks = [[False for _ in range(self.width)] for __ in range(self.height)]
        for x, y in self.corruptions[:length]:
            blocks[y][x] = True
        # bfs
        queue = [self.start]
        parents = dict()
        parents[self.start] = None
        while queue:
            # current x, y; already in parents
            x, y = queue[0]
            queue.pop(0)
            if DEBUG:
                print(x, y, queue)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_x, next_y = x + dx, y + dy
                if not (0 <= next_x < self.width and 0 <= next_y < self.height):
                    continue
                if (next_x, next_y) in parents:
                    continue
                if blocks[y][x]:
                    continue
                parents[(next_x, next_y)] = (x, y)
                queue.append((next_x, next_y))
        # restore path
        if self.end not in parents:
            return -1
        path = [self.end]
        while parent := parents[path[-1]]:
            path.append(parent)
        path = path[::-1]
        if DEBUG:
            print(path)
        return len(path) - 1

    def solve(self):
        lu, ru = 0, len(self.corruptions)
        while lu + 1 < ru:
            length = (lu + ru) // 2
            is_in_right_half = self.find_path_length(length + 1) == -1
            if is_in_right_half:
                ru = length
            else:
                lu = length
        return self.corruptions[ru]


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

