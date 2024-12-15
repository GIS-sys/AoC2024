DEBUG = False
CELL_WALL = "#"
CELL_BOX = "O"
CELL_BOXL = "["
CELL_BOXR = "]"
CELL_EMPTY = "."
CELL_ROBOT = "@"
COMMAND_LEFT = "<"
COMMAND_UP = "^"
COMMAND_RIGHT = ">"
COMMAND_DOWN = "v"


class Field:
    def __init__(self, cells: list[list[str]]):
        self.cells = []
        for line in cells:
            self.cells.append([])
            for cell in line:
                if cell == CELL_WALL:
                    self.cells[-1] += [CELL_WALL, CELL_WALL]
                if cell == CELL_BOX:
                    self.cells[-1] += [CELL_BOXL, CELL_BOXR]
                if cell == CELL_EMPTY:
                    self.cells[-1] += [CELL_EMPTY, CELL_EMPTY]
                if cell == CELL_ROBOT:
                    self.cells[-1] += [CELL_ROBOT, CELL_EMPTY]
        self.height = len(self.cells)
        self.width = len(self.cells[0])
        for y in range(self.height):
            for x in range(self.width):
                if self.cells[y][x] == CELL_ROBOT:
                    self.cells[y][x] = CELL_EMPTY
                    self.robot_pos = [x, y]
                    break

    def move(self, command: str):
        if command == COMMAND_LEFT or command == COMMAND_RIGHT:
            self.move_hor(command)
        else:
            self.move_ver(command)

    def move_hor(self, command: str):
        # direction
        direction = None
        if command == COMMAND_LEFT:
            direction = -1
        if command == COMMAND_RIGHT:
            direction = 1
        # move
        x = self.robot_pos[0] + direction
        y = self.robot_pos[1]
        while True:
            cell = self.cells[y][x]
            if cell == CELL_WALL:
                break
            if cell == CELL_EMPTY:
                bx, by = x, y
                while bx != self.robot_pos[0] + direction:
                    self.cells[by][bx] = self.cells[by][bx - direction]
                    bx -= direction
                self.robot_pos[0] += direction
                self.cells[self.robot_pos[1]][self.robot_pos[0]] = CELL_EMPTY
                break
            x += direction * 2

    def move_ver(self, command: str):
        # direction
        direction = None
        if command == COMMAND_UP:
            direction = -1
        if command == COMMAND_DOWN:
            direction = 1
        # predict what to move
        x = self.robot_pos[0]
        y = self.robot_pos[1] + direction
        boxes_to_move = []
        to_check = [(x, y)]
        while to_check:
            x, y = to_check[0]
            to_check.pop(0)
            cell = self.cells[y][x]
            if cell == CELL_WALL:
                boxes_to_move = []
                return
            if cell == CELL_EMPTY:
                continue
            if cell == CELL_BOXL:
                boxes_to_move.append((x, y))
                to_check += [(x, y + direction), (x + 1, y + direction)]
            else:
                boxes_to_move.append((x - 1, y))
                to_check += [(x - 1, y + direction), (x, y + direction)]
        # move
        self.robot_pos[1] += direction
        for x, y in boxes_to_move[::-1]:
            self.cells[y + direction][x] = CELL_BOXL
            self.cells[y + direction][x + 1] = CELL_BOXR
            self.cells[y][x] = CELL_EMPTY
            self.cells[y][x + 1] = CELL_EMPTY


    def boxes(self) -> list[tuple[int, int]]:
        result = []
        for y in range(self.height):
            for x in range(self.width):
                if self.cells[y][x] == CELL_BOXL:
                    result.append((x, y))
        return result

    def __repr__(self) -> str:
        result = ""
        for y, line in enumerate(self.cells):
            if y == self.robot_pos[1]:
                result += "".join(line[:self.robot_pos[0]] + [CELL_ROBOT] + line[self.robot_pos[0] + 1:])
            else:
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
        if DEBUG:
            print(self.field)
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

