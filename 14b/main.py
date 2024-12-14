DEBUG = True

WIDTH = 101
HEIGHT = 103
MAX_STEPS = 100000


def mod(x: int, y: int) -> int:
    y = abs(y)
    return ((x % y) + y) % y

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

#for p in [(0, 5), (5, 0), (10, 0), (2, 0), (10, 0)]:
#    print(p, get_quadrant(p))


class Robot:
    def __init__(self, p: tuple[int, int], v: tuple[int, int]):
        self.p = p
        self.v = v

    def predict(self, steps: int):
        self.predicted_position = mod(self.p[0] + self.v[0] * steps, WIDTH), mod(self.p[1] + self.v[1] * steps, HEIGHT)

    def get_predicted_position(self) -> tuple[int, int]:
        return self.predicted_position

    def __repr__(self) -> str:
        return f"p={self.p} v={self.v}, predicted={self.predicted_position}"


class Field:
    def __init__(self, robots: list[Robot]):
        self.robots = dict()
        for robot in robots:
            self.robots[robot.get_predicted_position()] = self.robots.get(robot.get_predicted_position(), []) + [robot]

    def __repr__(self) -> str:
        result = [[" " for _ in range(WIDTH)] for __ in range(HEIGHT)]
        for pos in self.robots.keys():
            result[pos[1]][pos[0]] = "8"
        return "\n".join(["".join(line) for line in result])

    def is_tree(self) -> bool:
        return False

    def looks_like_tree(self) -> bool:
        for required_position in [(WIDTH // 2, 0), (WIDTH // 2 - 1, 1), (WIDTH // 2 + 1, 1)]:
            if self.robots.get(required_position, None) is None:
                return False
        return True


class Solver:
    def __init__(self):
        self.robots = []

    def read(self):
        while i := input():
            _, *values = split(i, ["p=", ",", " v=", ","])
            values = list(map(int, values))
            p = values[0:2]
            v = values[2:4]
            self.robots.append(Robot(p, v))

    def solve(self):
        for step in range(MAX_STEPS):
            for robot in self.robots:
                robot.predict(step)
            field = Field(self.robots)
            if field.is_tree():
                return step
            if field.looks_like_tree():
                print(step)
                print(field)
                input()
            if DEBUG:
                if (step * 10) % MAX_STEPS == 0:
                    print(f"{step}/{MAX_STEPS}")
        return None


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

