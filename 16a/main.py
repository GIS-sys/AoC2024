DEBUG = True
SYMBOL_EMPTY = "."
SYMBOL_START = "S"
SYMBOL_END = "E"
SYMBOL_WALL = "#"
MAX_SCORE = 100000000000


def rot_distance(x: int, y: int, cycle: int):
    distance = (x - y) % cycle
    if distance > cycle // 2:
        distance = cycle - distance
    return distance


class State:
    def __init__(self, x: int, y: int, direction: int):
        self.x = x
        self.y = y
        self.direction = direction

    def __hash__(self) -> int:
        return self.x * 1000 + self.y * 4 + self.direction

    def __eq__(self, oth) -> bool:
        if isinstance(oth, State):
            return self.x == oth.x and self.y == oth.y and self.direction == oth.direction

    def __add__(self, oth):
        if isinstance(oth, tuple):
            if len(oth) == 2:
                return State(self.x + oth[0], self.y + oth[1], self.direction)
        raise NotImplementedError(f"State cannot add {type(oth)} {oth}")

    def __sub__(self, oth):
        if isinstance(oth, tuple):
            if len(oth) == 2:
                return self + (-oth[0], -oth[1])
        raise NotImplementedError(f"State cannot sub {type(oth)} {oth}")

    def __repr__(self) -> str:
        return f"(x={self.x} y={self.y} direction={self.direction})"


class Maze:
    def __init__(self, lines: list[list[str]]):
        self.lines: list[list[str]] = []
        self.end_states: list[State] = None
        self.start_state: State = None
        for y, line in enumerate(lines):
            if SYMBOL_START in line:
                x = line.index(SYMBOL_START)
                self.lines.append(line[:x] + [SYMBOL_EMPTY] + line[x+1:])
                self.start_state = State(x=x, y=y, direction=0)
            elif SYMBOL_END in line:
                x = line.index(SYMBOL_END)
                self.lines.append(line[:x] + [SYMBOL_EMPTY] + line[x+1:])
                self.end_states = [State(x=x, y=y, direction=d) for d in [0, 1, 2, 3]]
            else:
                self.lines.append(line.copy())
        self.height: int = len(self.lines)
        self.width: int = len(self.lines[0])
        self.fastest: dict[State, int] = dict()

    def calculate_fastest(self):
        for state in self.end_states:
            self.fastest[state] = 0
        queue = self.end_states.copy()
        used = set()
        while queue:
            state = queue[0]
            queue.pop(0)
            used.add(hash(state))
            if self.lines[state.y][state.x] == SYMBOL_WALL:
                continue
            if DEBUG:
                print("calculating fastest:", state, self.fastest[state])
            for direction_index, direction in enumerate([(1, 0), (0, 1), (-1, 0), (0, -1)]):
                next_state = state - direction
                if not (0 <= next_state.x < self.width and 0 <= next_state.y < self.height):
                    continue
                for next_direction_index in [0, 1, 2, 3]:
                    next_state = State(next_state.x, next_state.y, next_direction_index)
                    next_score = self.fastest[state] + 1
                    next_score += 1000 * rot_distance(direction_index, state.direction, 4)
                    next_score += 1000 * rot_distance(direction_index, next_direction_index, 4)
                    self.fastest[next_state] = min(self.fastest.get(next_state, MAX_SCORE), next_score)
                    if hash(next_state) in used:
                        continue
                    used.add(hash(next_state))
                    queue.append(next_state)


class Solver:
    def __init__(self):
        self.maze: Maze = None

    def read(self):
        lines = []
        while i := input():
            lines.append(list(i))
        self.maze = Maze(lines)

    def solve(self):
        self.maze.calculate_fastest()
        return self.maze.fastest[self.maze.start_state]


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

