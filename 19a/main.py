DEBUG = True


class Solver:
    def __init__(self):
        self.towels: list[str] = None
        self.designs: list[str] = None

    def read(self):
        self.towels = input().split(", ")
        input()
        self.designs = []
        while i := input():
            self.designs.append(i)

    def check(self, design):
        dp = [False for _ in design] + [True]
        for i in range(len(design) - 1, -1, -1):
            for towel in self.towels:
                if len(towel) > len(design) - i:
                    continue
                if not dp[i + len(towel)]:
                    continue
                if design[i:i + len(towel)] != towel:
                    continue
                dp[i] = True
                break
        return dp[0]

    def solve(self):
        result = 0
        for design in self.designs:
            correct = self.check(design)
            if correct:
                result += 1
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

