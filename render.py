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

path_i = plot.run(prog, "$prefix_i")
space = prog.functions["$space"][0]

# diac
diac_markers = [prog.functions["$" + marker][0] for marker in ["diac", "diacl", "diacr"]]
diac_map = {diac: prog.functions["$" + diac][0]
                for diac in ["dot", "bar", "trema", "acute", "grave", "caron", "hat", "dgrave", "dacute"]}

class Variant:
    def __init__(self, id, fn, path, diac=None):
        self.id = id
        self.fn = fn
        self._path = path
        self.diac = diac

    def __repr__(self):
        return f"[{self.fn}/{self.diac if self.diac else "-"}]"

    def get_diac(self, diac):
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
            raise RuntimeError("No diacritic marker")

        return Variant(self.id, self.fn, path, diac)

    def has_diac_mark(self):
        return not self.diac and any(p for p in self._path if p in diac_markers)

    def path(self):
        if self.diac:
            return self._path
        else:
            return [c for c in self._path if c not in diac_markers]

class Char:
    def __init__(self, n=None, variants: list[Variant]|None = None):
        self.id = n

        if variants is None:
            variants = []
        self.variants = variants

    def path(self):
        return random.choice(self.variants).path()

    def variant(self, diac):
        return random.choice([var for var in self.variants if var.has_diac_mark()]).get_diac(diac)

    def __repr__(self):
        return repr(self.variants)


char_fns = [fn for fn in prog.functions if fn.startswith("$chr")]
re_chr = re.compile(r"^\$chr_(?P<num>\d+)(?P<desc>\w+)?$")
chars = dict()
for fn in char_fns:
    chr_match = re_chr.match(fn)
    if not chr_match:
        breakpoint()
    id = int(chr_match["num"])
    if id not in chars: chars[id] = Char(id)
    chars[id].variants.append(
        Variant(
            id=id,
            fn=fn,
            path=plot.run(prog, fn)
        )
    )

for char in list(chars.values()):
    if char.id > 10: continue  # disable .j
    vars = []
    vars.extend(var.get_diac("dot") for var in char.variants if var.has_diac_mark())
    vars.extend(var.get_diac("bar") for var in char.variants if var.has_diac_mark())
    if vars:
        id = 20 + char.id % 10
        if id not in chars:
            chars[id] = Char(id)
        chars[id].variants.extend(vars)

    vars = [var.get_diac("trema") for var in char.variants if var.has_diac_mark()]
    if vars:
        id = (char.id, char.id)
        if id not in chars:
            chars[id] = Char(id)
        chars[id].variants.extend(vars)


# print(chars)

def split_list_0(l):
    zero = l.index(0)
    return l[:zero], l[zero+1:]

sub_fns = [split_list_0(plot.run(prog, fn)) for fn in prog.functions if fn.startswith("$sub")]
# print(sub_fns)

lig_fns = list(fn for fn in prog.functions if fn.startswith("$lig_"))
# print(lig_fns)
re_lig = re.compile(
    r"^\$lig_"
    r"(?P<d1>\d+)(?P<desc1>[^_]\w*)?"
    r"_"
    r"(?P<d2>\d+)(?P<desc2>[^_]\w*)?$"
)
for fn in lig_fns:
    lig_match = re_lig.match(fn)
    assert lig_match, fn

    id = (int(lig_match["d1"]), int(lig_match["d2"]))

    var = Variant(
        id=id,
        fn=fn,
        path=plot.run(prog, fn)
    )
    if id not in chars: chars[id] = Char(id)
    chars[id].variants.append(var)


groups = {fn[7:]: plot.run(prog, fn) for fn in prog.functions if fn.startswith("$group_")}
prod_fns = {fn for fn in prog.functions if fn.startswith("$prod_")}

for fn in prod_fns:
    g1, g2 = fn[6:].split("_")
    for chr1 in groups[g1]:
        chr1_fn = fn_map[chr1]
        chr1_match = re_chr.match(chr1_fn)
        for chr2 in groups[g2]:
            chr2_fn = fn_map[chr2]
            chr2_match = re_chr.match(chr2_fn)

            id = (int(chr1_match["num"]), int(chr2_match["num"]))

            if id[0] % 10 == id[1] % 10:
                continue

            if id not in chars:
                chars[id] = Char(id, [])

            var = Variant(
                id=id,
                fn=(fn, chr1_fn, chr2_fn),
                path=plot.run(prog, fn, chr1, chr2)
            )
            chars[id].variants.append(var)

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


def combine(a, b):
    index = None
    matched = 0
    for i in range(len(a)):
        for j in range(len(b)):
            k = 0
            while i + k < len(a) and j + k < len(b) and  a[i + k] == b[j + k]:
                k += 1
            if k > matched:
                index = (i, j)
                matched = k

    if not index or matched < 2:
        return

    # do not match only suffix of `b`
    if index[1] + matched == len(b):
        return

    return a[:index[0]] + b[index[1]:]


def lig(word: list[Char]):
    word = list(word)
    i = 0
    while i < len(word) - 1:
        if type(word[i].id) is int and type(word[i+1].id) is int:
            combined_id = (word[i].id, word[i+1].id)
            if combined_id in chars:
                word[i] = chars[combined_id]
                del word[i+1]
                i -= 1

            elif word[i].id + 10 == word[i+1].id:
                del word[i+1]
                word[i] = word[i].variant("acute")
                word[i].id = word[i].id * 101 + 10
            elif word[i].id == (word[i+1].id - 20) * 101 + 10:
                del word[i]
                word[i] = chars[word[i].id - 20].variant("dacute")
                word[i].id = word[i].id * 10101 + 1020
            elif word[i].id + 20 == word[i+1].id:
                del word[i+1]
                word[i] = word[i].variant("caron")
                word[i].id = word[i].id * 101 + 20
            elif word[i].id == word[i+1].id + 10:
                del word[i]
                word[i] = word[i].variant("grave")
                word[i].id = word[i].id * 101 + 1000
            elif word[i].id == word[i+1].id * 101 + 2010:
                del word[i]
                word[i] = word[i].variant("dgrave")
                word[i].id = word[i].id * 10100 + 201000 + word[i].id
            elif word[i].id == word[i+1].id + 20:
                del word[i]
                word[i] = word[i].variant("hat")
                word[i].id = word[i].id * 101 + 2000
        elif type(word[i].id) is tuple and type(word[i+1].id) is int:
            combined_id = (word[i].id[1], word[i+1].id)
            if combined_id in chars:
                print(word[i].id, word[i+1].id, word[i].path(), chars[combined_id].path())
                comb = combine(word[i].path(), chars[combined_id].path())
                if comb:
                    word[i] = Variant(word[i].id + (word[i+1].id,), None, comb)
                    del word[i + 1]
            pass
        i += 1
    return word

text = eval(sys.argv[1])

for i, line in enumerate(text):
    code = []
    print(line)
    line = [lig(lig([chars[c] for c in word])) for word in line]
    print([[c.id for c in word] for word in line])
    print("-")
    for word in line:
        for c in word:
            code.extend(c.path())
        code.append(space)

    sub(code)
    # print(",".join(map(lambda x: fn_map[x], code)))
    plot.run(prog, "$call_n", len(code), *code)

    if i < len(text) - 1:
        plot.run(prog, "$newline")


plot.show(2)
