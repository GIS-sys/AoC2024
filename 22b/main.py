DEBUG = False


PRUNE_MASK = 2**24 - 1


def predict(secret: int, step: int) -> list[int]:
    secrets = [secret]
    for _ in range(step):
        result = secret << 6
        secret = (result ^ secret) & PRUNE_MASK
        result = secret >> 5
        secret = (result ^ secret) & PRUNE_MASK
        result = secret << 11
        secret = (result ^ secret) & PRUNE_MASK
        secrets.append(secret)
    return secrets


class Solver:
    def __init__(self):
        self.secrets: list[int] = None

    def read(self):
        self.secrets = []
        while i := input():
            self.secrets.append(int(i))

    def solve(self):
        # find all secrets
        all_secrets: list[list[int]] = []
        for secret in self.secrets:
            new_secrets = predict(secret, 2000)
            all_secrets.append(new_secrets)
        # prices
        all_prices: list[list[int]] = [[s % 10 for s in secrets] for secrets in all_secrets]
        # find all changes in prices
        all_changes: list[list[int]] = []
        for prices in all_prices:
            all_changes.append([prices[i + 1] - prices[i] for i in range(len(prices) - 1)])
        # create dictionary with all possible 4s of differences, mapping them to the sum of prices
        differences: dict[tuple[int, int, int, int], int] = dict()
        for changes in all_changes:
            for i in range(len(changes) - 3):
                differences[tuple(changes[i:i+4])] = 0
        # for every buyer for every change find how much will be bought and add to all differences
        for prices, changes in zip(all_prices, all_changes):
            local_differences: dict[tuple[int, int, int, int], int] = dict()
            for i in range(len(changes) - 3):
                price = prices[i + 4]
                change = tuple(changes[i:i+4])
                if change not in local_differences:
                    local_differences[change] = price
            for k, v in local_differences.items():
                differences[k] += v
        # find difference with the best total cost
        max_price = 0
        max_diff = None
        for diff, price in differences.items():
            if price > max_price:
                max_diff = diff
                max_price = price
        if DEBUG:
            print(max_diff)
        return max_price


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

