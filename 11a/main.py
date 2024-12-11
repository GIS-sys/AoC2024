DEBUG = False


class Solver:
    def __init__(self):
        self.stones = None

    def read(self):
        self.stones = list(map(int, input().split()))

    def solve(self):
        # blink
        for _ in range(25):
            next_stones = []
            for stone in self.stones:
                strstone = str(stone)
                lenstone = len(strstone)
                if stone == 0:
                    next_stones.append(1)
                elif lenstone % 2 == 0:
                    next_stones.append(int(strstone[:lenstone//2]))
                    next_stones.append(int(strstone[lenstone//2:]))
                else:
                    next_stones.append(stone * 2024)
            self.stones = next_stones
            if DEBUG:
                if len(self.stones) < 100:
                    print(self.stones)
                else:
                    print(len(self.stones))
        # calculate result
        result = len(self.stones)
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

