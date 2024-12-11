from typing import Union


DEBUG = False


class Solver:
    def __init__(self):
        self.stones = None

    def read(self):
        self.stones = list(map(int, input().split()))

    @staticmethod
    def transform_stone(stone: int) -> Union[int, tuple[int, int]]:
        strstone = str(stone)
        lenstone = len(strstone)
        if stone == 0:
            return 1
        elif lenstone % 2 == 0:
            return int(strstone[:lenstone//2]), int(strstone[lenstone//2:])
        else:
            return stone * 2024

    @staticmethod
    def transform_stones(stones: list[int]) -> list[int]:
        next_stones = []
        for stone in stones:
            transformed = Solver.transform_stone(stone)
            if isinstance(transformed, int):
                next_stones.append(transformed)
            elif isinstance(transformed, tuple):
                next_stones.append(transformed[0])
                next_stones.append(transformed[1])
            else:
                raise Exception()
        return next_stones

    def solve(self):
        # try blinking to understand hwhich numbers are important on each stage
        stage_stones = [set(self.stones)]
        for iter in range(75):
            next_stones = set(self.transform_stones(stage_stones[-1]))
            stage_stones.append(next_stones)
        # calculate them from the bottom
        stage_amounts = []
        stage_amounts.append({s: 1 for s in stage_stones[-1]})
        for stage in stage_stones[::-1][1:]:
            stage_amounts = [dict()] + stage_amounts
            for stone in stage:
                transformed = self.transform_stones([stone])
                stage_amounts[0][stone] = sum([stage_amounts[1][transformed_stone] for transformed_stone in transformed])
        ## calculate result
        result = sum([stage_amounts[0][stone] for stone in self.stones])
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

