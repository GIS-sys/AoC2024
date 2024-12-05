def bubblesort(l: list, smaller):
    for i in range(len(l)):
        for j in range(0, len(l)-1-i):
            if not smaller(l[j], l[j+1]):
                l[j], l[j+1] = l[j+1], l[j]


class Solver:
    def __init__(self):
        self.rules = dict()
        self.pages = []

    def read(self):
        while i := input():
            rule_a, rule_b = map(int, i.split("|"))
            rules = self.rules.get(rule_a, set())
            rules.add(rule_b)
            self.rules[rule_a] = rules
        while i := input():
            page = list(map(int, i.split(",")))
            self.pages.append(page)

    def solve(self):
        result = 0
        for page in self.pages:
            for i, x in enumerate(page):
                good = True
                for y in page[i+1:]:
                    if y in self.rules and x in self.rules[y]:
                        good = False
                        break
                if not good:
                    break
            if not good:
                bubblesort(page, smaller=lambda x, y: x in self.rules.get(y, set()))
                result += page[len(page)//2]
        return result


if __name__ == "__main__":
    solver = Solver()
    solver.read()
    answer = solver.solve()
    print(answer)

