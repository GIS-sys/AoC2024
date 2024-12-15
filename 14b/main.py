DEBUG = False

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
        self.predicted_position = (self.p[0] + self.v[0] * steps) % WIDTH, (self.p[1] + self.v[1] * steps) % HEIGHT

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
        return self.looks_like_tree__long_branch(10)
        #return self.looks_like_tree__square(3)
        #return self.looks_like_tree__precise()

    def looks_like_tree__top_cone(self) -> bool:
        for required_position in [(WIDTH // 2, 0), (WIDTH // 2 - 1, 1), (WIDTH // 2 + 1, 1)]:
            if self.robots.get(required_position, None) is None:
                return False
        return True

    def looks_like_tree__precise(self) -> bool:
        for required_position in [(WIDTH // 2 - 2, 17), (WIDTH // 2 - 1, 17), (WIDTH // 2, 17), (WIDTH // 2 + 1, 17), (WIDTH // 2 + 2, 17)]:
            if required_position not in self.robots:
                return False
        return True

    def looks_like_tree__square(self, side_length: int = 6) -> bool:
        for pos in self.robots.keys():
            found = True
            for dxy in range(side_length * side_length):
                next_pos = (pos[0] + (dxy // side_length), pos[1] + (dxy % side_length))
                if next_pos not in self.robots:
                    found = False
                    break
            if found:
                return True
        return False

    def looks_like_tree__long_branch(self, branch_length: int = 6) -> bool:
        for pos in self.robots.keys():
            if pos[0] > WIDTH // 2 + branch_length or pos[0] < WIDTH // 2 - branch_length:
                continue
            found = True
            for branch_iter in range(branch_length):
                if self.robots.get((pos[0] - branch_iter, pos[1] + branch_iter), None) is None:
                    found = False
                    break
            if found:
                return True
        return False

    def looks_like_tree(self) -> bool:
        #return self.looks_like_tree__top_cone()
        return self.looks_like_tree__long_branch()


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
        self.robots = self.robots[:len(self.robots) * 8 // 10]

    def solve(self):
        for step in range(MAX_STEPS):
            for robot in self.robots:
                robot.predict(step)
            field = Field(self.robots)
            if field.is_tree():
                return step
            if DEBUG:
                if field.looks_like_tree():
                    print(step)
                    print(field)
                    input("Press any key to continue...")
            if DEBUG:
                if (step * 10) % MAX_STEPS == 0:
                    print(f"{step}/{MAX_STEPS}")
        return None


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

