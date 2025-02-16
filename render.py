
import collections
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

# diac
diac_map = dict()
for marker in ["diac", "diacl", "diacr"]:
    marker_id = prog.functions["$" + marker][0]
    diac_map[marker_id] = dict()
    for diac in ["dot", "bar", "trema"]:
        diac_map[marker_id][diac] = prog.functions["$" + diac + marker[4:]][0]


class Variant:
    def __init__(self, id, start, end, desc, path, diac=None):
        self.id = id
        self.start = start
        self.end = end
        self._path = path
        self.desc = desc
        self._diac = diac

    def __repr__(self):
        return f"{self.start}{self.id}{self.desc if self.desc else ""}{self._diac if self._diac else ""}{self.end}"

    def diac(self, diac):
        path = list(self._path)

        for i in range(len(path)):
            if path[i] in diac_map:
                path[i] = diac_map[path[i]][diac]
                break
        else:
            raise RuntimeError("diac marker not found")

        return Variant(self.id, self.start, self.end, self.desc, path, diac)

    def path(self):
        return self._path

class Char:
    def __init__(self, n, fns):
        self.id = n
        self.variants = self._get_variants(n, fns)

        if n > 10:
            vars = self._get_variants(n - 10, fns)
            for var in (var for var in vars if var.start in "_iu"):
                var._path = path_i + var.path()
                var.start = "i"
            self.variants.extend(vars)

        if n > 20:
            vars = self._get_variants(n - 10, fns)
            self.variants.extend(var.diac("dot") for var in vars)
            self.variants.extend(var.diac("bar") for var in vars)

            vars = self._get_variants(n - 20, fns)
            self.variants.extend(var.diac("dot") for var in vars)
            self.variants.extend(var.diac("bar") for var in vars)

            for var in (var for var in vars if var.start in "_iu"):
                var._path = path_i * 2 + var._path
                var.start = "u"
            self.variants.extend(vars)

    def _get_variants(self, n, fns):
        re_num = re.compile(rf"^(?P<start>.){n}(?P<desc>[a-zA-Z]\w+)?(?P<end>.)$")
        variants = []
        for fn in fns:
            if match := re_num.match(fn):
                var = Variant(
                    id=n,
                    start=match["start"],
                    end=match["end"],
                    desc=match["desc"],
                    path=plot.run(prog, f"$chr{fn}"))
                variants.append(var)

        return variants

    def path(self):
        return random.choice(self.variants).path()

    def variant(self, diac):
        return random.choice([var for var in self.variants if not var._diac]).diac(diac)


char_fns = sorted([fn[4:] for fn in prog.functions if fn.startswith("$chr")])
chars = dict()
for i in range(1, 30):
    if i not in [10, 20, 25]:
        chars[i] = Char(i, char_fns)
print([ch.variants for ch in chars.values()])

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

def lig(word):
    word = list(word)
    i = 0
    while i < len(word) - 1:
        if word[i].id == word[i+1].id:
            del word[i+1]
            word[i] = word[i].variant("trema")
        i += 1
    return word

text = eval(sys.argv[1])

for i, line in enumerate(text):
    code = []
    for word in line:
        word = [chars[c] for c in word]
        word = lig(word)

        for c in word:
            code.extend(c.path())
        code.append(space)

    sub(code)
    plot.run(prog, "$call_n", len(code), *code)

    if i < len(text) - 1:
        plot.run(prog, "$newline")


plot.show(2)
