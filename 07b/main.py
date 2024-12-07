def iterate(ranges: list[tuple[int, int]]) -> list[int]:
    values = [r[0] for r in ranges]
    while True:
        yield values
        values[-1] += 1
        i = len(values) - 1
        while values[i] >= ranges[i][1]:
            if i == 0:
                return
            values[i] = ranges[i][0]
            values[i - 1] += 1
            i -= 1


def bin_iter(amount: int) -> list[int]:
    for x in iterate([(0, 2)] * amount):
        yield x


def ter_iter(amount: int) -> list[int]:
    for x in iterate([(0, 3)] * amount):
        yield x


DEBUG = False


class Equation:
    def __init__(self, values, result):
        self.values = values
        self.result = result
        self.processed = False
        self.solutions = []

    def solve_iteratively(self):
        if DEBUG:
            print(f"Solving: {self.result} = {'?'.join(map(str, self.values))}")
        self.solutions = []
        for signs in ter_iter(len(self.values) - 1):
            predicted_result = self.values[0]
            for sign, value in zip(signs, self.values[1:]):
                if sign == 0:
                    predicted_result += value
                elif sign == 1:
                    predicted_result *= value
                else:
                    predicted_result = int(str(predicted_result) + str(value))
            if predicted_result == self.result:
                self.solutions.append(signs)
            if DEBUG:
                print(f"attempt: signs={signs}, result={predicted_result}")
        self.processed = True


class Solver:
    def __init__(self):
        self.equations: list[Equation] = []

    def read(self):
        while i := input():
            result, values = i.split(": ")
            result = int(result)
            values = list(map(int, values.split(" ")))
            self.equations.append(Equation(values, result))

    def solve(self):
        result = 0
        for equation in self.equations:
            equation.solve_iteratively()
            if equation.processed and equation.solutions:
                result += equation.result
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

