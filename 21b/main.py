DEBUG = True
INTERMEDIATE_AMOUNT = 25 - 1
MAX_LOOKUP_SIZE = 1_000_000


class Keypad:
    @classmethod
    def find_specific_sequence_length(cls, code: str, amount: int = 0) -> int:
        code = "A" + code
        weight = 0
        for i in range(0, len(code) - 1):
            key_from, key_to = code[i], code[i + 1]
            part_weight = cls.how_to_press(key_from, key_to, amount)
            weight += part_weight
        return weight

    @classmethod
    def how_to_press(cls, key_from: str, key_to: str, amount: int = 0) -> int:
        pos_from = cls.POSITIONS[key_from]
        pos_to = cls.POSITIONS[key_to]
        return cls.how_to_press_pos(pos_from[0], pos_from[1], pos_to[0], pos_to[1], amount)

    @classmethod
    def how_to_press_pos(cls, pos_from_x: int, pos_from_y: int, pos_to_x: int, pos_to_y: int, amount: int = 0) -> int:
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
    def how_to_press_pos(cls, pos_from_x: int, pos_from_y: int, pos_to_x: int, pos_to_y: int, amount: int = 0) -> int:
        return abs(pos_from_x - pos_to_x) + abs(pos_from_y - pos_to_y) + 1


class DirectionalIntermediateKeypad(DirectionalKeypad):
    LOOKUP: dict[tuple[int, int, int, int, int], tuple[str, int]] = dict()
    @classmethod
    def how_to_press_pos(cls, pos_from_x: int, pos_from_y: int, pos_to_x: int, pos_to_y: int, amount: int = 0) -> int:
        args = (pos_from_x, pos_from_y, pos_to_x, pos_to_y, amount)
        if args in cls.LOOKUP:
            return cls.LOOKUP[args]
        if DEBUG and amount >= 20:
            print(f"{amount}, {len(cls.LOOKUP)=}")
        if amount == 0:
            return DirectionalKeypad.how_to_press_pos(pos_from_x, pos_from_y, pos_to_x, pos_to_y)
        # calc horizontal and vertical adjustments
        hor = ("<" if pos_from_x > pos_to_x else ">") * abs(pos_from_x - pos_to_x)
        ver = ("^" if pos_from_y > pos_to_y else "v") * abs(pos_from_y - pos_to_y)
        # combine them to minimize length after next directional keypad
        if pos_from_y == cls.BAD_POS[1] and pos_to_x == cls.BAD_POS[0]:
            result = ver + hor + "A"
            result = DirectionalIntermediateKeypad.find_specific_sequence_length(result, amount - 1)
            if len(cls.LOOKUP) < MAX_LOOKUP_SIZE:
                cls.LOOKUP[args] = result
            return result
        if pos_from_x == cls.BAD_POS[0] and pos_to_y == cls.BAD_POS[1]:
            result = hor + ver + "A"
            result = DirectionalIntermediateKeypad.find_specific_sequence_length(result, amount - 1)
            if len(cls.LOOKUP) < MAX_LOOKUP_SIZE:
                cls.LOOKUP[args] = result
            return result
        hor_first = DirectionalIntermediateKeypad.find_specific_sequence_length(hor + ver + "A", amount - 1)
        ver_first = DirectionalIntermediateKeypad.find_specific_sequence_length(ver + hor + "A", amount - 1)
        if hor_first < ver_first:
            result = hor_first
        else:
            result = ver_first
        if len(cls.LOOKUP) < MAX_LOOKUP_SIZE:
            cls.LOOKUP[args] = result
        return result


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
    def how_to_press_pos(cls, pos_from_x: int, pos_from_y: int, pos_to_x: int, pos_to_y: int, amount: int = 0) -> int:
        # calc horizontal and vertical adjustments
        hor = ("<" if pos_from_x > pos_to_x else ">") * abs(pos_from_x - pos_to_x)
        ver = ("^" if pos_from_y > pos_to_y else "v") * abs(pos_from_y - pos_to_y)
        # combine them to minimize length after next directional keypad
        if pos_from_y == cls.BAD_POS[1] and pos_to_x == cls.BAD_POS[0]:
            result = ver + hor + "A"
            return DirectionalIntermediateKeypad.find_specific_sequence_length(result, amount=INTERMEDIATE_AMOUNT)
        if pos_from_x == cls.BAD_POS[0] and pos_to_y == cls.BAD_POS[1]:
            result = hor + ver + "A"
            return DirectionalIntermediateKeypad.find_specific_sequence_length(result, amount=INTERMEDIATE_AMOUNT)
        hor_first = DirectionalIntermediateKeypad.find_specific_sequence_length(hor + ver + "A", amount=INTERMEDIATE_AMOUNT)
        ver_first = DirectionalIntermediateKeypad.find_specific_sequence_length(ver + hor + "A", amount=INTERMEDIATE_AMOUNT)
        if hor_first < ver_first:
            return hor_first
        else:
            return ver_first


class Solver:
    def __init__(self):
        self.codes: list[str] = None

    def read(self):
        self.codes = []
        while i := input():
            self.codes.append(i)

    def find_sequence_length(self, code: str):
        result = NumericKeypad.find_specific_sequence_length(code)
        return result

    def solve(self):
        result = 0
        for code in self.codes:
            length = self.find_sequence_length(code)
            if DEBUG:
                print(length)
            complexity = int(code[:-1]) * length
            result += complexity
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

