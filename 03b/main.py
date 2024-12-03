from typing import Optional


DEBUG = True


class STATE:
    START = 0

    U = 1
    L = 2
    LBRACKET = 3
    NUMBER_BEFORE_OR_COMMA = 4
    # SPACE = 6
    NUMBER_AFTER_OR_RBRACKET = 7

    O = 11
    N_OR_LBRACKET = 12
    APOSTROFE = 13
    T = 14
    DISABLE_LBRACKET = 15
    DISABLE_RBRACKET = 16
    ENABLE_RBRACKET = 17


class Parser:
    def __init__(self):
        self.state = STATE.START
        self.number_before = 0
        self.number_after = 0
        self.disabled = False

    def parse(self, letter: str) -> Optional[tuple[int, int]]:
        if DEBUG:
            print(letter, self.state)
        match self.state:
            # start
            case STATE.START:
                if letter == "m":
                    self.state = STATE.U
                elif letter == "d":
                    self.state = STATE.O

            # mul
            case STATE.U:
                if letter == "u":
                    self.state = STATE.L
                else:
                    self.state = STATE.START
                    self.parse(letter)
            case STATE.L:
                if letter == "l":
                    self.state = STATE.LBRACKET
                else:
                    self.state = STATE.START
                    self.parse(letter)
            case STATE.LBRACKET:
                if letter == "(":  # )
                    self.state = STATE.NUMBER_BEFORE_OR_COMMA
                    self.number_before = 0
                    self.number_after = 0
                else:
                    self.state = STATE.START
                    self.parse(letter)
            case STATE.NUMBER_BEFORE_OR_COMMA:
                if letter == ",":
                    # self.state = STATE.SPACE
                    self.state = STATE.NUMBER_AFTER_OR_RBRACKET
                elif letter in "1234567890":
                    self.number_before = self.number_before * 10 + int(letter)
                else:
                    self.state = STATE.START
                    self.parse(letter)
            # case STATE.SPACE:
            #     if letter == " ":
            #         self.state = STATE.NUMBER_AFTER_OR_RBRACKET
            #     else:
            #         self.state = STATE.START
            #         self.parse(letter)
            case STATE.NUMBER_AFTER_OR_RBRACKET:
                if letter == ")":
                    self.state = STATE.START
                    if self.disabled:
                        return None
                    return (self.number_before, self.number_after)
                elif letter in "1234567890":
                    self.number_after = self.number_after * 10 + int(letter)
                else:
                    self.state = STATE.START
                    self.parse(letter)

            # do and don't
            case STATE.O:
                if letter == "o":
                    self.state = STATE.N_OR_LBRACKET
                else:
                    self.state = STATE.START
                    self.parse(letter)
            case STATE.N_OR_LBRACKET:
                if letter == "n":
                    self.state = STATE.APOSTROFE
                elif letter == "(":
                    self.state = STATE.ENABLE_RBRACKET
                else:
                    self.state = STATE.START
                    self.parse(letter)
            case STATE.APOSTROFE:
                if letter == "'":
                    self.state = STATE.T
                else:
                    self.state = STATE.START
                    self.parse(letter)
            case STATE.T:
                if letter == "t":
                    self.state = STATE.DISABLE_LBRACKET
                else:
                    self.state = STATE.START
                    self.parse(letter)
            case STATE.DISABLE_LBRACKET:
                if letter == "(":  # )
                    self.state = STATE.DISABLE_RBRACKET
                else:
                    self.state = STATE.START
                    self.parse(letter)
            case STATE.DISABLE_RBRACKET:
                if letter == ")":
                    self.state = STATE.START
                    self.disabled = True
                    if DEBUG:
                        print("disabled", "\n\n")
                else:
                    self.state = STATE.START
                    self.parse(letter)
            case STATE.ENABLE_RBRACKET:
                if letter == ")":
                    self.state = STATE.START
                    self.disabled = False
                    if DEBUG:
                        print("enabled", "\n\n")
                else:
                    self.state = STATE.START
                    self.parse(letter)
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

