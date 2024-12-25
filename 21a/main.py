DEBUG = True


class Keypad:
    @classmethod
    def how_to_press(cls, key_from: str, key_to: str) -> str:
        pos_from = cls.POSITIONS[key_from]
        pos_to = cls.POSITIONS[key_to]
        return cls.how_to_press_pos(pos_from, pos_to)

    @classmethod
    def how_to_press_pos(cls, pos_from: tuple[int, int], pos_to: tuple[int, int]) -> str:
        # parse arguments
        pos_from_x, pos_from_y = pos_from
        pos_to_x, pos_to_y = pos_to
        # calc horizontal and vertical adjustments
        hor = ("<" if pos_from_x > pos_to_x else ">") * abs(pos_from_x - pos_to_x)
        ver = ("^" if pos_from_y > pos_to_y else "v") * abs(pos_from_y - pos_to_y)
        # combine them to prioritize hor and avoid bad pos
        if pos_from_y == cls.BAD_POS[1] and pos_to_x == cls.BAD_POS[0]:
            return ver + hor + "A"
        return hor + ver + "A"


class NumericKeypad(Keypad):
    POSITIONS = {
        "7": (0, 0),
        "8": (1, 0),
        "9": (2, 0),
        "4": (0, 1),
        "5": (1, 1),
        "6": (2, 1),
        "1": (0, 2),
        "2": (1, 2),
        "3": (2, 2),
        "0": (1, 3),
        "A": (2, 3),
    }
    FIELD_WIDTH = 3
    FIELD_HEIGHT = 4
    BAD_POS = (0, 3)


class DirectionalKeypad(Keypad):
    POSITIONS = {
        "^": (1, 0),
        "A": (2, 0),
        "<": (0, 1),
        "v": (1, 1),
        ">": (2, 1),
    }
    FIELD_WIDTH = 3
    FIELD_HEIGHT = 2
    BAD_POS = (0, 0)


class Solver:
    def __init__(self):
        self.codes: list[str] = None

    def read(self):
        self.codes = []
        while i := input():
            self.codes.append(i)

    def find_specific_sequence(self, code: str, keypad: Keypad):
        code = "A" + code
        sequence = ""
        for i in range(0, len(code) - 1):
            key_from, key_to = code[i], code[i + 1]
            part_sequence = keypad.how_to_press(key_from, key_to)
            sequence += part_sequence
        return sequence

    def find_sequence(self, code: str):
        robot1 = self.find_specific_sequence(code, NumericKeypad)
        robot2 = self.find_specific_sequence(robot1, DirectionalKeypad)
        #robot3 = self.find_specific_sequence(robot2, DirectionalKeypad)
        human = self.find_specific_sequence(robot2, DirectionalKeypad)
        if DEBUG:
            print(code)
            print(robot1)
            print(robot2)
            #print(robot3)
            print(human)
        return human

    def solve(self):
        result = 0
        for code in self.codes:
            sequence = self.find_sequence(code)
            print(len(sequence))
            complexity = int(code[:-1]) * len(sequence)
            result += complexity
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

