import random
import re
import sys
import mcesre


with open("scripts/cursive.sh", "r") as f:
    prog = mcesre.Compiler.compile(f.read())

plot = mcesre.Plot()
plot.run_code(".4i")

path_i = prog.functions["$chr_i_"][0]
path_u = prog.functions["$chr_i_"][0]


class Char:
    def __init__(self, n, fns):
        self.n = n
        self.fns = []
        self.cp = []

        self.fns, self.cp = map(list, zip(*self._get_paths(n, fns)))

        if n > 10:
            for fn, path in self._get_paths(n - 10, fns):
                if fn[0] in "_iu":
                    self.fns.append("i" + fn[1:])
                    self.cp.append([path_i] + path)
        if n > 20:
            for fn, path in self._get_paths(n - 20, fns):
                if fn[0] in "_iu":
                    self.fns.append("u" + fn[1:])
                    self.cp.append([path_u] + path)

        if not self.cp:
            raise RuntimeError(f"{n} in {fns}")

        for c in self.cp:
            if c[-1] == 0:
                del c[-1]

    def _get_paths(self, n, fns):
        re_num = re.compile(rf"^.{n}(v\d)?.$")
        fns = [fn for fn in fns if re_num.match(fn)]
        paths = [plot.run(prog, f"$chr{fn}") for fn in fns]
        return zip(fns, paths)

    def path(self):
        return random.choice(self.cp)


char_fns = sorted([fn[4:] for fn in prog.functions if fn.startswith("$chr")])
chars = dict()
for i in range(1, 30):
    if i not in [10, 20, 25]:
        chars[i] = Char(i, char_fns)
print([ch.fns for ch in chars.values()])

space = prog.functions["$space"][0]

text = eval(sys.argv[1])


for i, line in enumerate(text):
    code = []
    for word in line:
        for c in word:
            code.extend(chars[c].path())
        code.append(space)

    plot.run(prog, "$call_n", len(code), *code)

    if i < len(text) - 1:
        plot.run(prog, "$newline")


plot.show(2)
