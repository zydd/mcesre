
import copy
import random
import re
import sys
import mcesre

random.seed(42)


with open("scripts/cursive.sh", "r") as f:
    prog = mcesre.Compiler.compile(f.read())

fn_names, addr_argc = list(zip(*prog.functions.items()))
addrs, _ = zip(*addr_argc)
fn_map = dict(zip(addrs, fn_names))

plot = mcesre.Plot()
plot.run_code(".4i")

path_i = plot.run(prog, "$chr_i_")
space = prog.functions["$space"][0]

# diac
diac_markers = [prog.functions["$" + marker][0] for marker in ["diac", "diacl", "diacr"]]
diac_map = {diac: prog.functions["$" + diac][0]
                for diac in ["dot", "bar", "trema", "acute", "grave", "caron", "hat"]}

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
            if path[i] == diac_markers[0]:
                path[i] = diac_map[diac]
                break
            elif path[i] == diac_markers[1]:
                path[i:i+1] = [diac_markers[1], diac_map[diac], diac_markers[2]]
                break
            elif path[i] == diac_markers[2]:
                path[i:i+1] = [diac_markers[2], diac_map[diac], diac_markers[1]]
                break
        else:
            return None

        return Variant(self.id, self.start, self.end, self.desc, path, diac)

    def has_diac_mark(self):
        return not self._diac and any(p for p in self._path if p in diac_markers)

    def path(self):
        if self._diac:
            return self._path
        else:
            return [c for c in self._path if c not in diac_markers]

class Char:
    def __init__(self, n, fns):
        self.id = n
        self.variants = self._get_variants(n, fns)

        if n > 10 and n < 30:
            vars = self._get_variants(n - 10, fns)
            for var in (var for var in vars if var.start in "_iu"):
                var._path = path_i + var._path
                var.start = "i"
            self.variants.extend(vars)

        if n > 20 and n < 30:
            vars = self._get_variants(n - 10, fns)
            for var in vars:
                vard = var.diac("dot")
                varb = var.diac("bar")
                if vard: self.variants.append(vard)
                if varb: self.variants.append(varb)

            vars = self._get_variants(n - 20, fns)
            for var in vars:
                vard = var.diac("dot")
                varb = var.diac("bar")
                if vard: self.variants.append(vard)
                if varb: self.variants.append(varb)

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
        return random.choice([var for var in self.variants if var.has_diac_mark()]).diac(diac)

    def __repr__(self):
        return repr(self.variants)

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

lig_fns = list(fn for fn in prog.functions if fn.startswith("$lig_"))
print(sub_fns)
re_lig = re.compile(
    r"^\$lig(?P<start>.)"
    r"(?P<d1>\d+)(?P<desc1>[a-zA-Z]\w+)?"
    r"_"
    r"(?P<d2>\d+)(?P<desc2>[a-zA-Z]\w+)?"
    r"(?P<end>.)$"
)
for fn in lig_fns:
    match = re_lig.match(fn)

    id = int(match["d1"]) * 100 + int(match["d2"])
    if id not in chars:
        chars[id] = Char(id, [])

    var = Variant(
        id=id,
        start=match["start"],
        end=match["end"],
        desc=fn,
        path=plot.run(prog, fn)
    )
    chars[id].variants.append(var)

    if id < 10 * 100:
        id += 10 * 100
        if id not in chars:
            chars[id] = Char(id, [])

        var1 = copy.deepcopy(var)
        var1.id = id
        var1._path = path_i + var1._path
        chars[id].variants.append(var1)

        id += 10 * 100
        if id not in chars:
            chars[id] = Char(id, [])
        var2 = copy.deepcopy(var1)
        var2.id = id
        var2._path = path_i + var1._path
        chars[id].variants.append(var2)

        for diac in ["dot", "bar"]:
            var2 = var.diac(diac)
            var2.id = id
            chars[id].variants.append(var2)

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
                    # i += len(rep)
            else:
                idx[j] = 0
        i += 1

def lig(word):
    word = list(word)
    i = 0
    while i < len(word) - 1:
        combined_id = word[i].id * 100 + word[i+1].id
        if combined_id in chars:
            word[i] = chars[combined_id]
            del word[i+1]
            i -= 1
        elif word[i].id == word[i+1].id:
            del word[i+1]
            word[i] = word[i].variant("trema")
        elif word[i].id + 10 == word[i+1].id:
            del word[i+1]
            word[i] = word[i].variant("acute")
        elif word[i].id + 20 == word[i+1].id:
            del word[i+1]
            word[i] = word[i].variant("caron")
        elif word[i].id == word[i+1].id + 10:
            del word[i]
            word[i] = word[i].variant("grave")
        elif word[i].id == word[i+1].id + 20:
            del word[i]
            word[i] = word[i].variant("hat")
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
    print(",".join(map(lambda x: fn_map[x], code)))
    plot.run(prog, "$call_n", len(code), *code)

    if i < len(text) - 1:
        plot.run(prog, "$newline")


plot.show(2)
