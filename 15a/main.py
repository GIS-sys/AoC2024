DEBUG = False
CELL_WALL = "#"
CELL_BOX = "O"
CELL_EMPTY = "."
CELL_ROBOT = "@"
COMMAND_LEFT = "<"
COMMAND_UP = "^"
COMMAND_RIGHT = ">"
COMMAND_DOWN = "v"


class Field:
    def __init__(self, cells: list[list[str]]):
        self.cells = cells
        self.height = len(cells)
        self.width = len(cells[0])
        for y in range(self.height):
            for x in range(self.width):
                if self.cells[y][x] == CELL_ROBOT:
                    self.cells[y][x] = CELL_EMPTY
                    self.robot_pos = [x, y]
                    break

    def move(self, command: str):
        # direction
        direction = (None, None)
        if command == COMMAND_LEFT:
            direction = (-1, 0)
        if command == COMMAND_RIGHT:
            direction = (1, 0)
        if command == COMMAND_UP:
            direction = (0, -1)
        if command == COMMAND_DOWN:
            direction = (0, 1)
        # move
        x, y = self.robot_pos[0] + direction[0], self.robot_pos[1] + direction[1]
        while True:
            cell = self.cells[y][x]
            if cell == CELL_WALL:
                break
            if cell == CELL_EMPTY:
                self.robot_pos[0] += direction[0]
                self.robot_pos[1] += direction[1]
                self.cells[y][x] = CELL_BOX
                self.cells[self.robot_pos[1]][self.robot_pos[0]] = CELL_EMPTY
                break
            x += direction[0]
            y += direction[1]


    def boxes(self) -> list[tuple[int, int]]:
        result = []
        for y in range(self.height):
            for x in range(self.width):
                if self.cells[y][x] == CELL_BOX:
                    result.append((x, y))
        return result

    def __repr__(self) -> str:
        result = ""
        for line in self.cells:
            result += "".join(line)
            result += "\n"
        return result


class Solver:
    def __init__(self):
        self.field: Field = None
        self.commands: list[str] = None

    def read(self):
        cells = []
        while i:= input():
            cells.append(list(i))
        self.field = Field(cells)
        self.commands = []
        while i := input():
            self.commands += list(i)

    def solve(self):
        for command in self.commands:
            self.field.move(command)
            if DEBUG:
                print(command)
                print(self.field)
        result = 0
        for box in self.field.boxes():
            gps = box[0] + box[1] * 100
            result += gps
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

