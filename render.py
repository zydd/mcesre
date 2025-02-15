import random
import re
import sys
import mcesre

random.seed(42)


with open("scripts/cursive.sh", "r") as f:
    prog = mcesre.Compiler.compile(f.read())

plot = mcesre.Plot()
plot.run_code(".4i")

path_i = plot.run(prog, "$chr_i_")
space = prog.functions["$space"][0]


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
                    self.cp.append(path_i + path)
        if n > 20:
            for fn, path in self._get_paths(n - 20, fns):
                if fn[0] in "_iu":
                    self.fns.append("u" + fn[1:])
                    self.cp.append(path_i * 2 + path)

        if not self.cp:
            raise RuntimeError(f"{n} in {fns}")

        for c in self.cp:
            if c[-1] == 0:
                del c[-1]

    def _get_paths(self, n, fns):
        re_num = re.compile(rf"^.{n}([a-zA-Z]\w+)?.$")
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

def split_list_0(l):
    zero = l.index(0)
    return l[:zero], l[zero+1:]

sub_fns = [split_list_0(plot.run(prog, fn)) for fn in prog.functions if fn.startswith("$sub")]
print(sub_fns)


def sub(code):
    idx = [0] * len(sub_fns)
    i = 0
    while i < len(code):
        for j in range(len(sub_fns)):
            find, rep = sub_fns[j]
            if code[i] == find[idx[j]]:
                idx[j] += 1
                if idx[j] == len(find):
                    i -= idx[j]-1
                    code[i:i+idx[j]] = rep
                    for j in range(len(sub_fns)):
                        idx[j] = max(0, idx[j] - len(find))
                    i -= 1
            else:
                idx[j] = 0
        i += 1

text = eval(sys.argv[1])

for i, line in enumerate(text):
    code = []
    for word in line:
        for c in word:
            print(chars[c].fns)
            code.extend(chars[c].path())
        code.append(space)

    sub(code)
    plot.run(prog, "$call_n", len(code), *code)

    if i < len(text) - 1:
        plot.run(prog, "$newline")


plot.show(2)
