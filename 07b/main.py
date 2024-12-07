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


DEBUG = True


class Equation:
    def __init__(self, values, result):
        self.values = values
        self.result = result
        self.processed = False
        self.solutions = []

    @staticmethod
    def calc(values: list[int], signs: list[int]) -> int:
        predicted_result = values[0]
        for sign, value in zip(signs, values[1:]):
            if sign == 0:
                predicted_result += value
            elif sign == 1:
                predicted_result *= value
            else:
                predicted_result = int(str(predicted_result) + str(value))
        return predicted_result

    def solve_iteratively(self):
        if DEBUG:
            print(f"Solving: {self.result} = {'?'.join(map(str, self.values))}")
        self.solutions = []
        for signs in ter_iter(len(self.values) - 1):
            predicted_result = Equation.calc(self.values, signs)
            if predicted_result == self.result:
                self.solutions.append(signs)
            if DEBUG:
                print(f"attempt: signs={signs}, result={predicted_result}")
        self.processed = True

    # def solve_mim(self):
    #     if DEBUG:
    #         print(f"Solving: {self.result} = {'?'.join(map(str, self.values))}")
    #     if len(self.values) <= 4:
    #         if DEBUG:
    #             print("way too few values provided, defaulting to simple iterations")
    #         return self.solve_iteratively()
    #     self.values_before = map()
    #     for signs in ter_iter(len(self.values) // 2):
    #         predicted_result = Equation.calc(self.values[:len(signs)], signs)
    #         self.values_before[predicted_result] = self.values_before.get(predicted_result, []) + [signs]
    #     self.values_after = map()
    #     for signs in ter_iter(len(self.values) // 2):
    #         predicted_result = Equation.calc(self.values, signs)
    #         self.values_after[predicted_result] = self.values_after.get(predicted_result, []) + [signs]
    #     self.processed = True


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
            # equation.solve_mim()
            if equation.processed and equation.solutions:
                result += equation.result
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

