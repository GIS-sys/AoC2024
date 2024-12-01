class Solver:
    def __init__(self):
        self.left = []
        self.right = []

    def read(self):
        while i := input():
            a, b = map(int, i.split())
            self.left.append(a)
            self.right.append(b)

    def solve(self):
        self.left.sort()
        self.right.sort()
        answer = 0
        for a, b in zip(self.left, self.right):
            answer += abs(a - b)
        return answer


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

