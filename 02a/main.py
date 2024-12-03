def is_report_safe(report: list) -> bool:
    if len(report) < 2:
        return True
    asc = 1 if report[0] < report[1] else -1
    for i in range(len(report) - 1):
        level_before = report[i]
        level_after = report[i + 1]
        if abs(level_after - level_before) < 1:
            return False
        if abs(level_after - level_before) > 3:
            return False
        # B-A > 0 -> asc, B-A < 0 -> desc
        # multiplying by asc we only need to compare once
        if (level_after - level_before) * asc < 0:
            return False
    return True


class Solver:
    def __init__(self):
        self.reports = []

    def read(self):
        while i := input():
            reports = list(map(int, i.split(" ")))
            self.reports.append(reports)

    def solve(self):
        result = 0
        for report in self.reports:
            result += is_report_safe(report)
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

