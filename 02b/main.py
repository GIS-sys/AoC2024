DEBUG = False


def list_without(l: list, i: int) -> list:
    return l[:i] + l[i+1:]

def is_report_safe(report: list, tolerate: bool = False) -> bool:
    if len(report) < 2:
        return True
    if tolerate:
        # immediately check first two, because if first two are bad we will have wrong order
        if is_report_safe(list_without(report, 0), tolerate=False) or is_report_safe(list_without(report, 1), tolerate=False):
            return True
    asc = 1 if report[0] < report[1] else -1
    for i in range(len(report) - 1):
        level_before = report[i]
        level_after = report[i + 1]

        # If we are tolerating error, exclude either one of bad numbers and try again
        tolerate_fn = lambda: False if not tolerate else (is_report_safe(list_without(report, i), tolerate=False) or is_report_safe(list_without(report, i + 1), tolerate=False))

        if abs(level_after - level_before) < 1:
            return tolerate_fn()
        if abs(level_after - level_before) > 3:
            return tolerate_fn()
        # B-A > 0 -> asc, B-A < 0 -> desc
        # multiplying by asc we only need to compare once
        if (level_after - level_before) * asc < 0:
            return tolerate_fn()
    return True

def is_report_ultrasafe(report: list) -> bool:
    for i in range(len(report)):
        if is_report_safe(list_without(report, i), tolerate=False):
            return True
    return False

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
            is_safe = is_report_safe(report, tolerate=True)
            if DEBUG:
                is_ultrasafe = is_report_ultrasafe(report)
                print("Report", report, f"{is_safe=}", f"{is_ultrasafe=}")
                if is_safe != is_ultrasafe:
                    print("\n\nERROR ^^^\n\n\n\n")
            result += is_safe
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

