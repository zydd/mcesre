import re
import sys
import mcesre


with open("scripts/cursive.sh", "r") as f:
    prog = mcesre.Compiler.compile(f.read())

plot = mcesre.Plot()
plot.run_code(".4i")


class Char:
    def __init__(self, n, fns):
        self.n = n
        self.fns = []
        self.cp = []
        self.var = dict()

        re_num = re.compile(f"^.{n}.$")

        for fn in fns:
            if re_num.match(fn):
                self.fns.append(fn)

        if not self.fns:
            raise RuntimeError(f"{n} in {fns}")

        if len(self.fns) > 1:
            raise NotImplementedError

        self.cp = [plot.run(prog, f"$chr{self.fns[0]}")]

        for c in self.cp:
            if c[-1] == 0:
                del c[-1]

    def __repr__(self):
        return f"({self.n}: {self.cp[0]})"

char_fns = sorted([fn[4:] for fn in prog.functions if fn.startswith("$chr")])
print(char_fns)

chars = dict()

for i in range(1, 30):
    if i not in [10, 20, 25]:
        chars[i] = Char(i, char_fns)


space = prog.functions["$space"][0]

with open(sys.argv[1], "r") as f:
    text = eval(f.read())

for line in text:
    code = []
    for word in line:
        for c in word:
            code.extend(chars[c].cp[0])
        code.append(space)

    plot.run(prog, "$call_n", len(code), *code)
    plot.run(prog, "$newline")


plot.show(2)
