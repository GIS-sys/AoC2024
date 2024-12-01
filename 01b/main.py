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
        right_amounts = {}
        for b in self.right:
            right_amounts[b] = right_amounts.get(b, 0) + 1
        answer = 0
        for a in self.left:
            answer += right_amounts.get(a, 0) * a
        return answer


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

