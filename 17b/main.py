# By analazing the program it looks like it's a single big cycle, which transforms
# a    a           a               a               a                           a//(2**3)                   a//2^3
# b -> a%(2**3) -> (a%(2**3))^3 -> (a%(2**3))^3 -> (a%(2**3))^3^(a//(2**B)) -> (a%(2**3))^3^(a//(2**B)) -> (a%(2**3))^3^5^(a//(2**((a%(2**3))^3)))
# c    c           c               a//(2**B)       a//(2**B)                   a//(2**B)                   a//2^B
# and then outputs register b. In other words, if a = ak....a7a6a5a4a3a2a1a0, then program transforms
# a      ak...a5a3
# ... -> a2a1a0 ^ am+2am+1am ^ 110
# ...    ak...am
# m = a2a1a0 ^ 3
# and outputs a2a1a0 ^ am+2am+1am ^ 110
#
# so we only need to create dependencies and then iterate over free elements


DEBUG = True
#MAX_NUMBER = 1_000_000_000_000_000


def dec_to_bin(x: int, length: int = None) -> list[int]:
    result = []
    while x:
        r, x = x % 2, x // 2
        result.append(r)
    if length:
        result = result + [0] * (length - len(result))
    return result[::-1]


def bin_to_dec(x: list[int], length: int = None) -> int:
    result = 0
    for i, bit in enumerate(x):
        result += bit * 2**i
    return result


def xor(x: list[int], y: list[int]) -> list[int]:
    if len(x) != len(y):
        raise Exception(f"xor: len({x=}) != len({y=})")
    return [a ^ b for a, b in zip(x, y)]


BIT_SHIFT = 3
CONST_XOR1 = dec_to_bin(3, BIT_SHIFT)
CONST_XOR2 = dec_to_bin(5, BIT_SHIFT)


class BitsOption:
    def __init__(self, option: list[int], value: list[int]):
        self.option = option
        self.value = value

    def __repr__(self) -> str:
        return f"{self.option}<->{self.value}"


class Options:
    def __init__(self):
        pass

    def get_bits(self, index_from: int, index_to: int) -> list[BitsOption]:
        # return all possible bits for 
        return [BitsOption([0] * (index_to - index_from), [0] * (index_to - index_from)) for _ in range(2)]  # TODO

    def add_dependencies(self, bias: list[BitsOption], values: list[int], current_iter_bit: int):
        # set dependency for bits starting from bias[i] to bias[i+BIT_SHIFT], setting them to (a[current_iter_bit:current_iter_bit+BIT_SHIFT] + values)
        if DEBUG:
            print(bias, values, current_iter_bit)
       pass  # TODO

   def get_min(self) -> int:
       return -1  # TODO


class Solver:
    def __init__(self):
        self.program: list[int] = None

    def read(self):
        [input() for _ in range(3)]
        input()
        self.program = input()
        self.program = self.program[self.program.index(": ") + 2:].split(",")
        self.program = list(map(int, self.program))

    def solve(self):
        options = Options()
        for iter_raw, out in enumerate(self.program):
            iter_bit = BIT_SHIFT * iter_raw
            bias = options.get_bits(iter_bit, iter_bit + BIT_SHIFT)
            for a in bias:
                a.value = xor(a.value, CONST_XOR1)
            options.add_dependencies(bias, xor(xor(CONST_XOR1, CONST_XOR2), dec_to_bin(out, BIT_SHIFT)), iter_bit)
        return options.get_min()


        ## find dependencies based on output
        #dependencies: dict[int, tuple[int, bool]] = dict() # dependencies[x] = (y, a) <=> bit X is equal to bit Y (reversed if a==True)
        #for iter, out in enumerate(self.program):
        #    out_bin = dec_to_bin(out, self.bits_read_a)
        #    bits_bias = out
        #    for i, (out_bit, const_bit) in enumerate(zip(out_bin, self.bits_const)):
        #        dependencies[iter * self.bits_read_a + i + self.bits_bias_a] = (iter * self.bits_read_a + i, out_bit == const_bit)
        ## find free bits
        #free_bits_indexes = []
        #for index in range(max(dependencies.keys())):
        #    if index not in dependencies:
        #        free_bits_indexes.append(index)
        ## generate numbers using free bits and dependencies
        #min_number = MAX_NUMBER
        #for step in range(2**len(free_bits_indexes)):
        #    free_bits = dec_to_bin(step, len(free_bits_indexes))
        #    number: dict[int, int] = dict()
        #    print(free_bits_indexes, free_bits)
        #    print(number)
        #    print(dependencies)
        #    for bit, index in zip(free_bits, free_bits_indexes):
        #        number[index] = bit
        #    for next_index in sorted(dependencies.keys()):
        #        prev_index, reverse = dependencies[next_index]
        #        next_number = number[prev_index]
        #        if reverse:
        #            next_number = 1 - next_number
        #        number[next_index] = next_number
        #    number_dec = 0
        #    for index, bit in number.items():
        #        number_dec += bit * 2**index
        #    print(number_dec)
        #    min_number = min(min_number, number_dec)
        #return min_number

    #def copy(self):
    #    result = Solver()
    #    result.reg = self.reg.copy()
    #    result.program = self.program.copy()
    #    return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)
