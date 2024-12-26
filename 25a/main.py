DEBUG = False
SYMBOL_BLOCK = "#"
SYMBOL_EMPTY = "."


class Solver:
    def __init__(self):
        self.locks: list[list[int]] = None
        self.keys: list[list[int]] = None

    def read(self):
        self.locks = []
        self.keys = []
        while top_row := input():
            item = []
            # parse top row
            if top_row[0] == SYMBOL_BLOCK:
                is_lock = True
            else:
                is_lock = False
            item = [int(s == SYMBOL_BLOCK) for s in top_row]
            # parse all other rows
            while row := input():
                item = [it + int(cell == SYMBOL_BLOCK) for it, cell in zip(item, row)]
            # memorize item according to it's type
            if is_lock:
                self.locks.append(item)
            else:
                self.keys.append(item)
        if DEBUG:
            print(self.locks)
            print(self.keys)

    def solve(self):
        result = 0
        for lock in self.locks:
            for key in self.keys:
                combined = [h1 + h2 for h1, h2 in zip(lock, key)]
                if DEBUG:
                    print(combined, lock, key)
                if max(combined) <= 5 + 2:
                    result += 1
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

