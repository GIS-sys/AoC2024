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
        while document_index > 0:
            document_length = self.compacted_values[document_index][1]
            free_space_index = None
            for space_index, space_length in enumerate(self.compacted_spaces):
                if space_index >= document_index:
                    break
                if space_length >= document_length:
                    free_space_index = space_index
                    break
            if free_space_index is not None:
                # insert document inside space_index
                free_space_length = self.compacted_spaces[free_space_index]
                self.compacted_spaces = self.compacted_spaces[:free_space_index] + \
                                        [0, free_space_length - document_length] + \
                                        self.compacted_spaces[free_space_index + 1:document_index - 1] + \
                                        [self.compacted_spaces[document_index - 1] + document_length + self.compacted_spaces[document_index]] + \
                                        self.compacted_spaces[document_index + 1:]
                self.compacted_values = self.compacted_values[:free_space_index + 1] + \
                                        [self.compacted_values[document_index]] + \
                                        self.compacted_values[free_space_index + 1:document_index] + \
                                        self.compacted_values[document_index + 1:]
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

