
import copy

import matplotlib.pyplot as plt

import matplotlib.patches as mpatches
import matplotlib.path as mpath

plt.style.use("dark_background")

Path = mpath.Path

phi = (1 + 5**0.5)*0.5

class State:
    slant = phi**-2
    curv = phi-1
    x_scale = 1.4
    y_scale = 1

    def clone(self):
        return copy.copy(self)

stack = [State()]


path = dict()
path["d"] = lambda: [
    (Path.CURVE4, (stack[-1].curv, 0)),
    (Path.CURVE4, (1 + (1-stack[-1].curv) * stack[-1].slant, 1-stack[-1].curv)),
    (Path.CURVE4, (1 + stack[-1].slant, 1))
]
path["c"] = lambda: [
    (Path.CURVE4, (-stack[-1].curv * stack[-1].slant, -stack[-1].curv)),
    (Path.CURVE4, (1-stack[-1].slant-stack[-1].curv, -1)),
    (Path.CURVE4, (1-stack[-1].slant, -1))
]
path["b"] = lambda: [
    (Path.CURVE4, (stack[-1].curv, 0)),
    (Path.CURVE4, (1 + (stack[-1].curv-1) * stack[-1].slant, stack[-1].curv-1)),
    (Path.CURVE4, (1 - stack[-1].slant, -1))
]
path["a"] = lambda: [
    (Path.CURVE4, (stack[-1].slant * stack[-1].curv, stack[-1].curv)),
    (Path.CURVE4, (1 + stack[-1].slant - stack[-1].curv, 1)),
    (Path.CURVE4, (1 + stack[-1].slant, 1))
]
path["<"] = lambda: [
    (Path.MOVETO, (-1, 0)),
]
path[">"] = lambda: [
    (Path.MOVETO, (1, 0)),
]
path["v"] = lambda: [
    (Path.MOVETO, (-stack[-1].slant, -1)),
]
path["^"] = lambda: [
    (Path.MOVETO, (stack[-1].slant, 1)),
]
path["V"] = lambda: [
    (Path.LINETO, (-stack[-1].slant, -1)),
]
path["A"] = lambda: [
    (Path.LINETO, (stack[-1].slant, 1)),
]
path["_"] = lambda: [
    (Path.LINETO, (1, 0)),
]



def plot_path(verts, codes):
    fig, ax = plt.subplots(figsize=(18 - 1, 10))
    pp1 = mpatches.PathPatch(
        Path(verts, codes),
        fc="none", zorder=2)

    ax.add_patch(pp1)
    ax.plot(*list(zip(*verts)), ".", zorder=1, color="#ff000040")

    ax.set_ylim(-20, 0)
    ax.set_xlim(0, 36)
    ax.grid(zorder=-1, color="#323232")

    plt.tight_layout()
    plt.show()


def gen_path(pth):
    points = []
    pos = [1, 0]
    points.append((Path.MOVETO, tuple(pos)))

    for p in pth:
        if p == " ":
            stack[-1] = stack[-2].clone()
        elif p == "=":
            stack[-1].y_scale *= 0.5
            stack[-1].slant *= 0.5
        elif p == "*":
            stack[-1].y_scale *= 2
            stack[-1].slant *= 2
        elif p == "-":
            stack[-1].x_scale *= 0.5
            stack[-1].slant /= 0.5
        elif p == "+":
            stack[-1].x_scale *= 2
            stack[-1].slant /= 2
        elif p == "%":
            stack[-1].x_scale *= 1.5
            stack[-1].slant /= 1.5
        elif p == "|":
            stack[-1].slant *= 0.5
        elif p == "/":
            stack[-1].slant *= 1.3
        elif p == "r":
            stack[-1].curv += 0.1
        elif p == "[":
            stack.append(stack[-1].clone())
        elif p == "]":
            stack.pop()
        elif p == "$":
            pos = [1, pos[1] - 4 * stack[-1].y_scale]
            points.append((Path.MOVETO, tuple(pos)))
        else:
            points.extend([(code, (pos[0] + x * stack[-1].x_scale, pos[1] + y * stack[-1].y_scale)) for code, (x, y) in path[p]()])
            pos[0] = points[-1][1][0]
            pos[1] = points[-1][1][1]

    codes, verts = list(zip(*points))

    # verts = [(x + y, y) for x, y in verts]
    return verts, codes

chars = dict()
chars["i26"] = "[ -**dV *a b <vdv< ]"
chars["06"] = "%%[ *a -b<vdv< ]"


chars["1"] = "*[ -rrrd ||-<vd<v ]"
chars["2"] = "*[ -rrrd |V -ac ]"
chars["3"] = "[ -d ra*b-a -*c ]"
chars["4"] = "[ -d a--%_< <v c ]"
chars["5"] = "[ -d a===b^ V <<cd -c ]"
chars["6"] = "[ -d ra b -<vdv< ]"
chars["7"] = "[ -d -rrra _ v-<a<v -c ]"
chars["8"] = "*[ -rrrd|V a =b-c ]"
chars["9"] = "[ -d ra*ba b-c ]"


chars["1"] = "*[ ^ ||-%<vd<v ]"
chars["2"] = "*[ ^ |V -ac ]"
chars["3"] = "[ ^^ *b-a *c ]"
chars["4"] = "[ ^ a--_< <v c ]"
chars["5"] = "[ ^ ab <<cd v ]"
chars["6"] = "[ ^^ b -<vdv< ]"
chars["7"] = "[ ^ -rrra _ v-<a<v v ]"
chars["8"] = "*[ ^|/V ]"
chars["9"] = "[ ^^ *b ]"

enter = dict()
enter["1"] = "d"
enter["2"] = "d"
enter["3"] = "a"
enter["4"] = "o"
enter["5"] = "o"
enter["6"] = "6"
enter["7"] = "7"
enter["8"] = "d"
enter["9"] = "a"

exit = dict()
exit["1"] = "+v"
exit["2"] = "v"
exit["3"] = "v"
exit["4"] = "+v"
exit["5"] = "5"
exit["6"] = "+v"
exit["7"] = "7"
exit["8"] = "V"
exit["9"] = "V"


lig = dict()
lig[("v", "o")] = "-dv"
lig[("v", "d")] = "-*dv"
lig[("v", "7")] = "-dv"
lig[("v", "a")] = "-davv"
lig[("v", "6")] = "-d ra vv"
lig[("+v", "a")] = "d -avv"
lig[("+v", "d")] = "*rdv"
lig[("+v", "o")] = "rdv"
lig[("+v", "6")] = "rd ra vv"
lig[("+v", "7")] = "rdv"
lig[("^", "d")] = "^^--_vv"
lig[("5", "d")] = "^--A vv"
lig[("5", "a")] = "^-avv"
lig[("5", "o")] = ""
lig[("7", "d")] = "-%^c*dv"
lig[("7", "a")] = "-^cdavv"
lig[("7", "o")] = "^-cdv"
lig[("V", "d")] = "-%[*a bc *dv]"
lig[("V", "o")] = "Av"
lig[("V", "a")] = "*av"
lig[("5", "6")] = "^avv"
lig[("5", "7")] = ""
lig[("7", "6")] = "^-cd avv"
lig[("V", "6")] = "*[-a bav]"
lig[("V", "7")] = "Av"
lig[("7", "7")] = "^-%cdv"


abcd = "-[ [+d a===b^ V <<cd -c ]  [ -**dV *a b <vdv< ] [+d a===b^ <<v c  ] [+d a===b^ <<v c dA*A*c  ] "

def enc(chrs):
    res = ""
    chrs = chrs.split()

    # while chrs and chrs[0] not in chars:
    #     res += chrs.pop(0)
    #     res += " "
    #
    # if chars:
    #     res += lig[("+v", enter[chrs[0]])]
    #     res += " "

    for c, n in zip(chrs, chrs[1:]):
        if c in chars:
            res += chars[c]
            res += " "
            if n in chars:
                res += lig[(exit[c], enter[n])]
                res += " "
        else:
            res += c
        res += " "
    res += chars.get(chrs[-1], chrs[-1])
    return res


testpattern = lambda n, s=10: f'{n} ' + f' {n} '.join(map(str, range(1, s))) + f' {n}'
# plot_path(*gen_path(enc("-[$ " + testpattern(1))))
plot_path(*gen_path(enc("--=[$ " + " $ ".join(testpattern(n) for n in range(1, 10)) )))
# plot_path(*gen_path(enc("-[ $ 5 1 > " + " > ".join(map(str, range(1, 10))) + " > 1 ")))

