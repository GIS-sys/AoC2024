DEBUG = False


class Keypad:
    @classmethod
    def find_specific_sequence(cls, code: str) -> tuple[str, int]:
        code = "A" + code
        sequence = ""
        weight = 0
        for i in range(0, len(code) - 1):
            key_from, key_to = code[i], code[i + 1]
            part_sequence, part_weight = cls.how_to_press(key_from, key_to)
            sequence += part_sequence
            weight += part_weight
        return sequence, weight

    @classmethod
    def how_to_press(cls, key_from: str, key_to: str) -> tuple[str, int]:
        pos_from = cls.POSITIONS[key_from]
        pos_to = cls.POSITIONS[key_to]
        return cls.how_to_press_pos(pos_from[0], pos_from[1], pos_to[0], pos_to[1])

    @classmethod
    def how_to_press_pos(cls, pos_from_x: int, pos_from_y: int, pos_to_x: int, pos_to_y: int) -> tuple[str, int]:
        return "?", 0


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

    @classmethod
    def how_to_press_pos(cls, pos_from_x: int, pos_from_y: int, pos_to_x: int, pos_to_y: int) -> str:
        # calc horizontal and vertical adjustments
        hor = ("<" if pos_from_x > pos_to_x else ">") * abs(pos_from_x - pos_to_x)
        ver = ("^" if pos_from_y > pos_to_y else "v") * abs(pos_from_y - pos_to_y)
        # combine them to prioritize hor and avoid bad pos
        result = hor + ver + "A"
        if pos_from_y == cls.BAD_POS[1] and pos_to_x == cls.BAD_POS[0]:
            result = ver + hor + "A"
        return result, len(result)


class DirectionalIntermediateKeypad(DirectionalKeypad):
    @classmethod
    def how_to_press_pos(cls, pos_from_x: int, pos_from_y: int, pos_to_x: int, pos_to_y: int) -> str:
        # calc horizontal and vertical adjustments
        hor = ("<" if pos_from_x > pos_to_x else ">") * abs(pos_from_x - pos_to_x)
        ver = ("^" if pos_from_y > pos_to_y else "v") * abs(pos_from_y - pos_to_y)
        # combine them to minimize length after next directional keypad
        if pos_from_y == cls.BAD_POS[1] and pos_to_x == cls.BAD_POS[0]:
            result = ver + hor + "A"
            return result, DirectionalKeypad.find_specific_sequence(result)[1]
        if pos_from_x == cls.BAD_POS[0] and pos_to_y == cls.BAD_POS[1]:
            result = hor + ver + "A"
            return result, DirectionalKeypad.find_specific_sequence(result)[1]
        _, hor_first = DirectionalKeypad.find_specific_sequence(hor + ver + "A")
        _, ver_first = DirectionalKeypad.find_specific_sequence(ver + hor + "A")
        if hor_first < ver_first:
            return hor + ver + "A", hor_first
        else:
            return ver + hor + "A", ver_first


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

    @classmethod
    def how_to_press_pos(cls, pos_from_x: int, pos_from_y: int, pos_to_x: int, pos_to_y: int) -> str:
        # calc horizontal and vertical adjustments
        hor = ("<" if pos_from_x > pos_to_x else ">") * abs(pos_from_x - pos_to_x)
        ver = ("^" if pos_from_y > pos_to_y else "v") * abs(pos_from_y - pos_to_y)
        # combine them to minimize length after next directional keypad
        if pos_from_y == cls.BAD_POS[1] and pos_to_x == cls.BAD_POS[0]:
            result = ver + hor + "A"
            return result, DirectionalIntermediateKeypad.find_specific_sequence(result)[1]
        if pos_from_x == cls.BAD_POS[0] and pos_to_y == cls.BAD_POS[1]:
            result = hor + ver + "A"
            return result, DirectionalIntermediateKeypad.find_specific_sequence(result)[1]
        hfs, hor_first = DirectionalIntermediateKeypad.find_specific_sequence(hor + ver + "A")
        vfs, ver_first = DirectionalIntermediateKeypad.find_specific_sequence(ver + hor + "A")
        if DEBUG:
            print(f"{hor_first=} {ver_first=}")
            print(f"{hfs=} {vfs=}")
            print(f"{hor=} {ver=}")
            print(f"{pos_from_x=} {pos_from_y=}   {pos_to_x=} {pos_to_y=}")
        if hor_first < ver_first:
            return hor + ver + "A", hor_first
        else:
            return ver + hor + "A", ver_first


class Solver:
    def __init__(self):
        self.codes: list[str] = None

    def read(self):
        self.codes = []
        while i := input():
            self.codes.append(i)

    def find_sequence(self, code: str):
        robot1 = NumericKeypad.find_specific_sequence(code)[0]
        robot2 = DirectionalIntermediateKeypad.find_specific_sequence(robot1)[0]
        human = DirectionalKeypad.find_specific_sequence(robot2)[0]
        if DEBUG:
            print(code)
            print(robot1)
            print(robot2)
            print(human)
        return human

    def solve(self):
        result = 0
        for code in self.codes:
            sequence = self.find_sequence(code)
            if DEBUG:
                print(len(sequence))
            complexity = int(code[:-1]) * len(sequence)
            result += complexity
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

