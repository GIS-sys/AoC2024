DEBUG = True


def mix(secret: int, result: int) -> int:
    return secret ^ result

def prune(secret: int) -> int:
    return secret % 2**24

def predict(secret: int, step: int) -> int:
    for _ in range(step):
        # step 1
        result = secret * 64
        secret = mix(secret, result)
        secret = prune(secret)
        # step 2
        result = secret // 32
        secret = mix(secret, result)
        secret = prune(secret)
        # step 3
        result = secret * 2048
        secret = mix(secret, result)
        secret = prune(secret)
    return secret


class Solver:
    def __init__(self):
        self.secrets: list[int] = None

    def read(self):
        self.secrets = []
        while i := input():
            self.secrets.append(int(i))

    def solve(self):
        result = 0
        for secret in self.secrets:
            new_secret = predict(secret, 2000)
            result += new_secret
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

