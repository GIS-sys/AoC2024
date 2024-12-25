DEBUG = False
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

    def solve(self):
        output = []
        ip = 0
        iter = 0
        while ip < len(self.program) - 1 and iter < DEBUG_MAX_ITER:
            op = self.program[ip]
            literal = self.program[ip + 1]
            # parse combo
            combo = ([0,1,2,3] + self.reg + [None])[literal]
            # parse op
            if op == 0:
                self.reg[0] = self.reg[0] // 2**combo
            elif op == 1:
                self.reg[1] = xor(self.reg[1], literal)
            elif op == 2:
                self.reg[1] = combo % 8
            elif op == 3:
                if self.reg[0] != 0:
                    ip = literal - 2
            elif op == 4:
                self.reg[1] = xor(self.reg[1], self.reg[2])
            elif op == 5:
                output.append(combo % 8)
            elif op == 6:
                self.reg[1] =self. reg[0] // 2**combo
            elif op == 7:
                self.reg[2] = self.reg[0] // 2**combo
            if DEBUG:
                print(f"{ip}: {op} <- {literal} ({combo})  {self.reg} {output}")
            # next
            ip += 2
            iter += 1
        return ",".join(map(str, output))


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)
