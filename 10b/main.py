DEBUG = False


class TopographicMapIterator:
    def __init__(self, topographic_map):
        self.topographic_map = topographic_map
        self.x = -1
        self.y = 0

    def __next__(self) -> tuple[tuple[int, int], int]:
        self.x += 1
        if self.x >= self.topographic_map.width:
            self.x = 0
            self.y += 1
        if self.y >= self.topographic_map.height:
            raise StopIteration
        return (self.x, self.y), self.topographic_map.map[self.y][self.x]

class TopographicMap:
    def __init__(self, heights: list[list[int]]):
        self.map = [line.copy() for line in heights]
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.dp = [[0 for __ in range(self.width)] for _ in range(self.height)]
        if DEBUG:
            print(f"Map:")
            for line in self.map:
                print(line)

    def __iter__(self):
        return TopographicMapIterator(self)

    def dp_reachable_ends(self):
        for current_height in range(9, -1, -1):
            for (x, y), height in self:
                if height != current_height:
                    continue
                if height == 9:
                    self.dp[y][x] = 1
                    continue
                for dx, dy in [(1,0), (0,1), (-1,0), (0,-1)]:
                    cx, cy = x + dx, y + dy
                    if 0 <= cy and cy < self.height and 0 <= cx and cx < self.width and self.map[cy][cx] == height + 1:
                        self.dp[y][x] += self.dp[cy][cx]
            if DEBUG:
                print(f"DP: {current_height}")
                for line in self.dp:
                    print(line)

    def get_trailhead_scores(self) -> int:
        self.dp_reachable_ends()
        scores = []
        for (x, y), height in self:
            if height == 0:
                scores.append(self.dp[y][x])
                if DEBUG:
                    print(f"score {x} {y} = {self.dp[y][x]}")
        return scores


class Solver:
    def __init__(self):
        self.map = None

    def read(self):
        heights = []
        while i := input():
            heights.append(list(map(int, i)))
        self.map = TopographicMap(heights)

    def solve(self):
        trailhead_scores = self.map.get_trailhead_scores()
        result = sum(trailhead_scores)
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

