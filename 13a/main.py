DEBUG = False


def split(s: str, inbetween: list[str]) -> list[str]:
    result = []
    for b in inbetween:
        index = s.index(b)
        if index == -1:
            return None
        result.append(s[:index])
        s = s[index + len(b):]
    result.append(s)
    return result

#print(split("AAA BBCCDD", [" ", "CC"]))


def gcd(a: int, b: int):
    a, b = abs(a), abs(b)
    if b == 0:
        raise Exception(f"gcd(...) got 0 as an argument: {a=} {b=}")
    while b != 0:
        a, b = b, a % b
    return a


class Machine:
    def __init__(self, button_a: str, button_b: str, prize: str):
        self.original_button_a = button_a
        self.original_button_b = button_b
        self.original_prize = prize
        _, self.a1, self.a2 = split(button_a, ["Button A: X", ", Y"])
        _, self.b1, self.b2 = split(button_b, ["Button B: X", ", Y"])
        _, self.c1, self.c2 = split(prize, ["Prize: X=", ", Y="])
        self.a1, self.a2, self.b1, self.b2, self.c1, self.c2 = map(int, (self.a1, self.a2, self.b1, self.b2, self.c1, self.c2))
        gcd1 = gcd(self.a1, gcd(self.b1, self.c1))
        self.a1, self.b1, self.c1 = self.a1 // gcd1, self.b1 // gcd1, self.c1 // gcd1
        gcd2 = gcd(self.a2, gcd(self.b2, self.c2))
        self.a2, self.b2, self.c2 = self.a2 // gcd2, self.b2 // gcd2, self.c2 // gcd2

    def __repr__(self) -> str:
        return f"A: ({self.a1}, {self.a2})\nB: ({self.b1}, {self.b2})\nPrize: ({self.c1}, {self.c2})"

    @staticmethod
    def diofant_general_solution(a: int, b: int) -> tuple[int, int]:
        if a == 0 or b == 0:
            raise Exception(f"diofant_general_solution(...) got 0 as an argument: {a=} {b=}")
        if a < 0:
            recursion = Machine.diofant_general_solution(-a, b)
            return -recursion[0], recursion[1]
        if b < 0:
            recursion = Machine.diofant_general_solution(a, -b)
            return recursion[0], -recursion[1]
        gcd_ab = gcd(a, b)
        if gcd_ab != 1:
            raise Exception(f"diofant_general_solution(...) got arguments with gcd={gcd_ab}: {a=} {b=}")
        return Machine._diofant_general_solution_clean(a, b)

    @staticmethod
    def _diofant_general_solution_clean(a: int, b: int) -> tuple[int, int]:
        if b == 0:
            return 1, 0
        recursion = Machine._diofant_general_solution_clean(b, a % b)
        return recursion[1], recursion[0] - recursion[1] * (a // b)

    def find_minimum_buttons(self) -> tuple[int, int]:
        # calculate how much we need to move on each axis
        try:
            k1, m1 = self.diofant_general_solution(self.a1, self.b1)
            k1, m1 = k1 * self.c1, m1 * self.c1
            k2, m2 = self.diofant_general_solution(self.a2, self.b2)
            k2, m2 = k2 * self.c2, m2 * self.c2
        except:
            return None, None
        if DEBUG:
            print("Diofant:")
            print("k1, m1:", k1, m1, "    a, b, c: ", self.a1, self.b1, self.c1, "    result:", self.a1*k1+self.b1*m1)
            print("k2, m2:", k2, m2, "    a, b, c: ", self.a2, self.b2, self.c2, "    result:", self.a2*k2+self.b2*m2)
        # check if collinear or not - this will tell us how many solutions can be
        D = self.a2 * self.b1 - self.a1 * self.b2
        if D == 0:
            # TODO
            # if collinear - check if on the same line
            # minimize 3*k+m
            raise NotImplemented("Discriminant is equal to 0")
        # if not collinear - solve
        # k = k1+b1*t = k2+b2*p
        # m = m1-a1*t = m2-a2*p
        # ---
        # t = (k2-k1+b2*p)/b1
        # m1-a1*(k2-k1)/b1-a1*b2*p/b1=m2-a2*p
        # p = (m2-m1+a1*(k2-k1)/b1) / (a2-a1*b2/b1)
        # p = ((m2-m1)*b1+(k2-k1)*a1) / (a2*b1-a1*b2)
        pD = ((m2 - m1) * self.b1 + (k2 - k1) * self.a1)
        if DEBUG:
            print(f"{D=}, {pD=}")
        if pD % D != 0:
            return None, None
        p = pD // D
        k, m = k2 + self.b2 * p, m2 - self.a2 * p
        if DEBUG:
            print(k, m, self.a1, self.b1, self.c1, self.a2, self.b2, self.c2)
        if k * self.a1 + m * self.b1 != self.c1:
            return None, None
        return k, m


class Solver:
    def __init__(self):
        self.machines = []

    def read(self):
        while button_a := input():
            button_b = input()
            prize = input()
            input()
            self.machines.append(Machine(button_a, button_b, prize))


    def solve(self):
        result = 0
        for machine in self.machines:
            button_a_clicks, button_b_clicks = machine.find_minimum_buttons()
            if DEBUG:
                print("Machine:")
                print(machine)
                print(f"{button_a_clicks=} {button_b_clicks=}")
            if button_a_clicks is not None and button_b_clicks is not None:
                result += 3 * button_a_clicks + button_b_clicks
        return result


if __name__ == "__main__":
    print("ATTENTION: this task needs input with 2 empty lines in the end")
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

