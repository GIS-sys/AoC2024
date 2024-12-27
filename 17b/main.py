# By analazing the program it looks like it's a single big cycle, which transforms
# a    a//2^3
# b -> (a%2^3)^(a//2^5)^6
# c    a//2^5
# and then outputs register b. In other words, if a = ak....a7a6a5a4a3a2a1, then program transforms
# a      ak...a5a3
# ... -> a2a1a0 ^ a7a6a5 ^ 110
# ...    ak...a6a5
# and outputs a2a1a0 ^ a7a6a5 ^ 110
#
# so we only need to create dependencies and then iterate over free elements


DEBUG = False
DEBUG_MAX_ITER = 100000
MAX_NUMBER = 1_000_000_000_000_000


def dec_to_bin(x: int, length: int = None) -> list[int]:
    result = []
    while x:
        r, x = x % 2, x // 2
        result.append(r)
    if length:
        result = result + [0] * (length - len(result))
    return result[::-1]


def xor(a, b):
    return a ^ b


class Solver:
    def __init__(self):
        self.bits_read_a = 3 # this means we take a2a1a0
        self.bits_bias_a = 5 # this means we take same amount as before, but from 5: a7a6a5
        self.bits_const = dec_to_bin(6, self.bits_read_a) # this represents 110

    def read(self):
        [input() for _ in range(3)]
        input()
        self.program = input()
        self.program = self.program[self.program.index(": ") + 2:].split(",")
        self.program = list(map(int, self.program))

    def solve(self):
        # find dependencies based on output
        dependencies: dict[int, tuple[int, bool]] = dict() # dependencies[x] = (y, a) <=> bit X is equal to bit Y (reversed if a==True)
        for iter, out in enumerate(self.program):
            out_bin = dec_to_bin(out, self.bits_read_a)
            for i, (out_bit, const_bit) in enumerate(zip(out_bin, self.bits_const)):
                dependencies[iter * self.bits_read_a + i + self.bits_bias_a] = (iter * self.bits_read_a + i, out_bit == const_bit)
        # find free bits
        free_bits_indexes = []
        for index in range(max(dependencies.keys())):
            if index not in dependencies:
                free_bits_indexes.append(index)
        # generate numbers using free bits and dependencies
        min_number = MAX_NUMBER
        for step in range(2**len(free_bits_indexes)):
            free_bits = dec_to_bin(step, len(free_bits_indexes))
            number: dict[int, int] = dict()
            print(free_bits_indexes, free_bits)
            print(number)
            print(dependencies)
            for bit, index in zip(free_bits, free_bits_indexes):
                number[index] = bit
            for next_index in sorted(dependencies.keys()):
                prev_index, reverse = dependencies[next_index]
                next_number = number[prev_index]
                if reverse:
                    next_number = 1 - next_number
                number[next_index] = next_number
            number_dec = 0
            for index, bit in number.items():
                number_dec += bit * 2**index
            print(number_dec)
            min_number = min(min_number, number_dec)
        return min_number

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
