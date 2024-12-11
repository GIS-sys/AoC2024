DEBUG = False
SPACE = -1


class FileSystem:
    def __init__(self, dense: list[int]):
        self.dense_values = [(i, v) for i, v in enumerate(dense[0::2])]
        self.dense_spaces = dense[1::2]
        if len(self.dense_spaces) < len(self.dense_values):
            self.dense_spaces.append(0)
        if DEBUG:
            print("DENSE")
            print(self.dense_values)
            print("\n")
            print(self.dense_spaces)
            print("\n" * 5)

    def compact(self):
        self.compacted_values = self.dense_values.copy()
        self.compacted_spaces = self.dense_spaces.copy()
        document_index = len(self.compacted_values) - 1
        rightmost_nonempty_space_index = 0
        while self.compacted_spaces[rightmost_nonempty_space_index] == 0:
            rightmost_nonempty_space_index += 1
        while document_index > 0:
            document_length = self.compacted_values[document_index][1]
            free_space_index = None
            for space_index in range(rightmost_nonempty_space_index, document_index):
                space_length = self.compacted_spaces[space_index]
                if space_length >= document_length:
                    free_space_index = space_index
                    break
            if free_space_index is not None:
                # insert document inside space_index
                free_space_length = self.compacted_spaces[free_space_index]
                if free_space_index == document_index - 1:
                    # Before:
                    # AAA   C   DDD
                    # UUU  V Y  ZZZ
                    #
                    # so we found space V bigger than document C
                    # C.index = document_index
                    # V.index = free_space_index
                    #
                    # After:
                    # AAA  C    DDD
                    # UUU 0 V+Y ZZZ
                    self.compacted_spaces[free_space_index + 1] += self.compacted_spaces[free_space_index]  # Y = V+Y
                    self.compacted_spaces[free_space_index] = 0                                             # B = 0
                else:
                    # Before:
                    # AAA       BBB   C   DDD
                    # UUU  V    WWW  X Y  ZZZ
                    #
                    # so we found space V bigger than document C
                    # C.index = document_index
                    # V.index = free_space_index
                    #
                    # After:
                    # AAA  C    BBB       DDD
                    # UUU 0 V-C WWW X+C+Y ZZZ
                    self.compacted_spaces = (self.compacted_spaces[:free_space_index] +                       # UUU
                                            [0, free_space_length - document_length] +                        # 0, V-C
                                            self.compacted_spaces[free_space_index + 1:document_index - 1] +  # WWW
                                            [self.compacted_spaces[document_index - 1] + document_length + self.compacted_spaces[document_index]] +
                                            self.compacted_spaces[document_index + 1:])                       # ZZZ
                    self.compacted_values = (self.compacted_values[:free_space_index + 1] +               # AAA
                                            [self.compacted_values[document_index]] +                     # C
                                            self.compacted_values[free_space_index + 1:document_index] +  # BBB
                                            self.compacted_values[document_index + 1:])                   # DDD
                while self.compacted_spaces[rightmost_nonempty_space_index] == 0:
                    rightmost_nonempty_space_index += 1
            else:
                document_index -= 1
            print(f"{len(self.compacted_values) - document_index} / {len(self.compacted_values)}")
            if DEBUG:
                print("COMPACTED")
                print(self.compacted_values)
                print("\n")
                print(self.compacted_spaces)
                print("\n" * 2)

    def checksum(self) -> int:
        checksum = 0
        global_index = 0
        for document, space_length in zip(self.compacted_values, self.compacted_spaces):
            document_index, document_length = document
            for i in range(document_length):
                checksum += global_index * document_index
                global_index += 1
            global_index += space_length
        return checksum


class Solver:
    def __init__(self):
        self.filesystem_dense = ""

    def read(self):
        self.filesystem_dense = input()

    def solve(self):
        self.filesystem = FileSystem(list(map(int, self.filesystem_dense)))
        self.filesystem.compact()
        checksum = self.filesystem.checksum()
        return checksum


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

