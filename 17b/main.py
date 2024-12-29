# By analazing the program it looks like it's a single big cycle, which transforms
# a    a           a               a               a                           a//(2**3)                   a//(2**3)
# b -> a%(2**3) -> (a%(2**3))^3 -> (a%(2**3))^3 -> (a%(2**3))^3^(a//(2**B)) -> (a%(2**3))^3^(a//(2**B)) -> (a%(2**3))^3^5^(a//(2**((a%(2**3))^3)))
# c    c           c               a//(2**B)       a//(2**B)                   a//(2**B)                   a//(2**B)
# and then outputs register b. In other words, if a = ak....a7a6a5a4a3a2a1a0, then program transforms
# a      ak...a5a3
# ... -> a2a1a0 ^ am+2am+1am ^ 110
# ...    ak...am
# m = a2a1a0 ^ 3
# and outputs a2a1a0 ^ am+2am+1am ^ 110
#
# so we only need to create dependencies and then iterate over free elements


#0, 0, 0, 0, 0, 1 (reversed)
# 100000  100000  100000  100000  100000  100  100
# 0       000     011     011     111     111  010 = 2
# 0       0       0       100     100     100  100
#0, 0, 1, None, None, None, None, 0, 0, 0 (reversed)
# 000????100  000????100  000????100  000????100  000????100  000????  000????
# 0           100         111         111         111         111      010 = 2
# 0           0           0           000         000         000      000


DEBUG = False


def dec_to_bin(x: int, length: int = None) -> list[int]:
    result = []
    while x:
        r, x = x % 2, x // 2
        result.append(r)
    if length:
        result = result + [0] * (length - len(result))
    return result


def bin_to_dec(x: list[int]) -> int:
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
    def __init__(self, value: list[int]):
        #self.index = index
        self.value = value

    def __repr__(self) -> str:
        return f">{self.value}<"

    def copy(self):
        return BitsOption(self.value.copy())


class Options:
    def __init__(self):
        self.bits = [BitsOption([0]), BitsOption([1])]

    def get_bits(self, index_from: int, index_to: int) -> list[BitsOption]:
        # return all possible bit options
        if DEBUG:
            print("get_bits")
            print(self.bits)
        for i in range(index_from, index_to):
            new_bits = []
            for bit in self.bits:
                if len(bit.value) < i + 1 or bit.value[i] is None:
                    while len(bit.value) < i + 1:
                        bit.value.append(None)
                    new_bits.append(bit.copy())
                    new_bits.append(bit.copy())
                    new_bits[-2].value[i] = 0
                    new_bits[-1].value[i] = 1
                else:
                    new_bits.append(bit.copy())
            self.bits = new_bits
        return [b.copy() for b in self.bits]

    def add_dependencies(self, bias_list: list[BitsOption], value_list: list[int], current_iter_bit: int):
        # set dependency for bits starting from bias[i] to bias[i+BIT_SHIFT], setting them to (a[current_iter_bit:current_iter_bit+BIT_SHIFT] + values)
        bias_list = [bin_to_dec(b.value) for b in bias_list]
        if DEBUG:
            print("add dependencies")
            print(len(self.bits), self.bits)
            print(f"{bias_list=}")
            print(f"{value_list=} {current_iter_bit=}")
        assert(len(bias_list) == len(self.bits))
        # predict
        new_bits = []
        for i, (bias, bit) in enumerate(zip(bias_list, self.bits)):
            bit = bit.copy()
            new_bits.append(bit)
            for value_index, value in enumerate(value_list):
                # predicted value
                new_value = bit.value[current_iter_bit + value_index]
                if value:
                    new_value = 1 - new_value
                # index of predicted value
                new_index = current_iter_bit + value_index + bias
                # pad
                while len(bit.value) < new_index + 1:
                    bit.value.append(None)
                # check conflict
                if bit.value[new_index] == 1 - new_value:
                    new_bits.pop()
                    break
                bit.value[new_index] = new_value
        self.bits = new_bits
        if DEBUG:
            print(len(self.bits), self.bits)

    def get_numbers(self) -> int:
       return [bin_to_dec([z if z is not None else 0 for z in x.value]) for x in self.bits]


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
                a.value = xor(a.value[iter_bit:iter_bit+3], CONST_XOR1)
            values_to_conform = xor(xor(CONST_XOR1, CONST_XOR2), dec_to_bin(out, BIT_SHIFT))
            options.add_dependencies(bias, values_to_conform, iter_bit)
        result = options.get_numbers()
        if DEBUG:
            print("Numbers:")
            print(result)
        result = min(result)
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)
