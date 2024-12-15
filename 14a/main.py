DEBUG = False

WIDTH = 101
HEIGHT = 103
#WIDTH = 11
#HEIGHT = 7
STEPS = 100


def mod(x: int, y: int) -> int:
    y = abs(y)
    return ((x % y) + y) % y


def get_quadrant(p: tuple[int, int]) -> int:
    if p[0] == WIDTH // 2 or p[1] == HEIGHT // 2:
        return -1
    qx = (p[0] * 2) // WIDTH
    qy = (p[1] * 2) // HEIGHT
    return qx * 2 + qy


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
        quadrants = [[] for _ in range(5)]
        for robot in self.robots:
            robot.predict(STEPS)
            quadrant = get_quadrant(robot.get_predicted_position())
            quadrants[quadrant].append(robot)
        if DEBUG:
            print(quadrants)
        result = 1
        for robots_in_quadrant in quadrants[:-1]:
            result *= len(robots_in_quadrant)
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

