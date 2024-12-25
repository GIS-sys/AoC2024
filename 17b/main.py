from multiprocessing import Pool


DEBUG = True
DEBUG_MAX_ITER = 100000


MOCK_INPUT = False
lines_real = [
    "Register A: 52884621",
    "Register B: 0",
    "Register C: 0",
    "",
    "Program: 2,4,1,3,7,5,4,7,0,3,1,5,5,5,3,0"
]
lines_example = [
    "Register A: 729",
    "Register B: 0",
    "Register C: 0",
    "",
    "Program: 0,1,5,4,3,0"
]
lines = lines_real
#lines = lines_example
MI = 0
def mock_input():
 global MI, lines
 if MI >= len(lines):
  raise Exception("mock input ended")
 MI += 1
 return lines[MI - 1]
if MOCK_INPUT:
    input = mock_input


PROCESSES = 32


def xor(a, b):
    return a ^ b


class Solver:
    def __init__(self):
        self.reg = None
        self.program = None

    def read(self):
        self.reg = [input() for _ in range(3)]
        self.reg = [int(x[x.index(": ") + 2:]) for x in self.reg]
        input()
        self.program = input()
        self.program = self.program[self.program.index(": ") + 2:].split(",")
        self.program = list(map(int, self.program)) + [None]

    def model(self, prediction: list[int]):
        output = []
        ip = 0
        iter = 0
        program = self.program.copy()
        reg = self.reg.copy()
        while ip < len(program) - 1 and iter < DEBUG_MAX_ITER:
            op = program[ip]
            literal = program[ip + 1]
            # parse combo
            combo = ([0,1,2,3] + reg + [None])[literal]
            # parse op
            if op == 0:
                reg[0] = reg[0] // 2**combo
            elif op == 1:
                reg[1] = xor(reg[1], literal)
            elif op == 2:
                reg[1] = combo % 8
            elif op == 3:
                if reg[0] != 0:
                    ip = literal - 2
            elif op == 4:
                reg[1] = xor(reg[1], reg[2])
            elif op == 5:
                output.append(combo % 8)
                if len(output) > len(prediction) or output[-1] != prediction[len(output) - 1]:
                    return False
            elif op == 6:
                reg[1] = reg[0] // 2**combo
            elif op == 7:
                reg[2] = reg[0] // 2**combo
            # if DEBUG:
            #     print(f"{ip}: {op} <- {literal} ({combo})  {reg} {output}")
            # next
            ip += 2
            iter += 1
        return len(output) == len(prediction) - 1

    @staticmethod
    def iterate_solution(args):
        self, start, step, length = args
        a = start
        for _ in range(length):
            self.reg[0] = a
            if self.model(self.program):
                return a
            a += step
        return None

    def solve(self):
        ONE_STEP_LENGTH = 1_000_000
        # iter = 10_000_000_000 // ONE_STEP_LENGTH // PROCESSES
        iter = 16608_000_000 // ONE_STEP_LENGTH // PROCESSES
        # iter = 0
        while True:
            with Pool(PROCESSES) as p:
                results = p.map(Solver.iterate_solution, [(self.copy(), iter * ONE_STEP_LENGTH * PROCESSES + index, PROCESSES, ONE_STEP_LENGTH) for index in range(PROCESSES)])
            for result in results:
                if result is not None:
                    return result
            iter += 1
            if DEBUG:
                print(f"{iter * PROCESSES} * {ONE_STEP_LENGTH}")

    def copy(self):
        result = Solver()
        result.reg = self.reg.copy()
        result.program = self.program.copy()
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)
