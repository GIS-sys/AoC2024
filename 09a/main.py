DEBUG = False
SPACE = -1


class Solver:
    def __init__(self):
        self.filesystem_dense = ""

    def read(self):
        self.filesystem_dense = input()

    def solve(self):
        # undense
        self.filesystem = []
        for index, block in enumerate(self.filesystem_dense):
            block_amount = int(block)
            is_space = (index % 2 == 1)
            id = index // 2
            if is_space:
                self.filesystem += [SPACE for _ in range(block_amount)]
            else:
                self.filesystem += [id for _ in range(block_amount)]
        if DEBUG:
            print(self.filesystem)
            print("\n" * 5)
        # compact
        self.filesystem_compacted = self.filesystem.copy()
        lu = 0
        ru = len(self.filesystem_compacted) - 1
        while lu < ru:
            if self.filesystem_compacted[lu] != SPACE:
                lu += 1
                continue
            if self.filesystem_compacted[ru] == SPACE:
                ru -= 1
                continue
            self.filesystem_compacted[lu], self.filesystem_compacted[ru] = self.filesystem_compacted[ru], SPACE
            lu += 1
            ru -= 1
        if DEBUG:
            print(self.filesystem_compacted)
            print("\n" * 5)
        # calculate checksum
        checksum = 0
        for index, value in enumerate(self.filesystem_compacted):
            if value == SPACE:
                break
            checksum += index * value
        return checksum


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

