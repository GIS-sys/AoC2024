from typing import Optional


DEBUG = True


class STATE:
    M = 0
    U = 1
    L = 2
    LBRACKET = 3
    NUMBER_BEFORE_OR_COMMA = 4
    # SPACE = 6
    NUMBER_AFTER_OR_RBRACKET = 7


class Parser:
    def __init__(self):
        self.state = STATE.M
        self.number_before = 0
        self.number_after = 0

    def parse(self, letter: str) -> Optional[tuple[int, int]]:
        if DEBUG:
            print(letter, self.state)
        match self.state:
            case STATE.M:
                if letter == "m":
                    self.state = STATE.U
            case STATE.U:
                if letter == "u":
                    self.state = STATE.L
                else:
                    self.state = STATE.M
            case STATE.L:
                if letter == "l":
                    self.state = STATE.LBRACKET
                else:
                    self.state = STATE.M
            case STATE.LBRACKET:
                if letter == "(":  # )
                    self.state = STATE.NUMBER_BEFORE_OR_COMMA
                    self.number_before = 0
                    self.number_after = 0
                else:
                    self.state = STATE.M
            case STATE.NUMBER_BEFORE_OR_COMMA:
                if letter == ",":
                    # self.state = STATE.SPACE
                    self.state = STATE.NUMBER_AFTER_OR_RBRACKET
                elif letter in "1234567890":
                    self.number_before = self.number_before * 10 + int(letter)
                else:
                    self.state = STATE.M
            # case STATE.SPACE:
            #     if letter == " ":
            #         self.state = STATE.NUMBER_AFTER_OR_RBRACKET
            #     else:
            #         self.state = STATE.M
            case STATE.NUMBER_AFTER_OR_RBRACKET:
                if letter == ")":
                    self.state = STATE.M
                    return (self.number_before, self.number_after)
                elif letter in "1234567890":
                    self.number_after = self.number_after * 10 + int(letter)
                else:
                    self.state = STATE.M
        return None


class Solver:
    def __init__(self):
        self.program = ""

    def read(self):
        while i := input():
            self.program += i + "\n"

    def solve(self):
        result = 0
        parser = Parser()
        for symbol in self.program:
            parsed = parser.parse(symbol)
            if parsed:
                if DEBUG:
                    print(parsed, "\n\n")
                result += parsed[0] * parsed[1]
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

