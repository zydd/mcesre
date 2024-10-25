import matplotlib.pyplot as plt

import matplotlib.patches as mpatches
import matplotlib.path as mpath

plt.style.use("dark_background")


phi = (1 + 5 ** 0.5) * 0.5

Path = mpath.Path

path = dict()
path["d"] = [
    (Path.CURVE3, (1, 0)),
    (Path.CURVE3, (1, 1)),
]
path["b"] = [
    (Path.CURVE3, (0, -1)),
    (Path.CURVE3, (1, -1)),
]
path["q"] = [
    (Path.CURVE3, (0.8, 0)),
    (Path.CURVE3, (1, -1)),
]
path["p"] = [
    (Path.CURVE3, (0, 1)),
    (Path.CURVE3, (1, 1)),
]
path["v"] = [
    (Path.LINETO, (0, -1)),
]
path["^"] = [
    (Path.LINETO, (0, 1)),
]
path["S"] = [
    (Path.CURVE4, (-0.5, -0.1)),
    (Path.CURVE4, (2, -2)),
    (Path.CURVE4, (1, -2)),
]
path["s"] = [
    (Path.CURVE4, (0.75, 0)),
    (Path.CURVE4, (0.25, 1)),
    (Path.CURVE4, (1, 1)),
]
path["~"] = [
    (Path.CURVE4, (-0.5, 0.5)),
    (Path.CURVE4, (0.5, 1.5)),
    (Path.CURVE4, (0, 2)),
]
path["2"] = [
    (Path.CURVE4, (2, 0)),
    (Path.CURVE4, (3, -2)),
    (Path.CURVE4, (2, -2)),
]


path["D"] = [
    (Path.CURVE3, (0, -1)),
    (Path.CURVE3, (-1, -1)),
]
path["B"] = [
    (Path.CURVE3, (0, -1)),
    (Path.CURVE3, (1, -1)),
]
# path["Q"] = [
#     (Path.CURVE3, (0.9, 0)),
#     (Path.CURVE3, (1, -1)),
# ]
path["P"] = [
    (Path.CURVE3, (-1, 0)),
    (Path.CURVE3, (-1, -1)),
]
path["_"] = [
    (Path.LINETO, (1, 0)),
]

path["<"] = [
    (Path.MOVETO, (-1, 0)),
]
path[">"] = [
    (Path.MOVETO, (1, 0)),
]
path["."] = [
    (Path.MOVETO, (1 - 0.2, 1.1)),
    (Path.LINETO, (1 - 0.1, 1.15)),
    (Path.MOVETO, (0, 0)),
]
path["˘"] = [
    (Path.MOVETO, (1 - 0.35, 1.22)),
    (Path.LINETO, (1 - 0.0, 1.1)),
    (Path.LINETO, (1 + 0.2, 1.2)),
    (Path.MOVETO, (0, 0)),
]
path["'"] = [
    (Path.MOVETO, (0, 1)),
]



def plot_path(verts, codes):
    fig, ax = plt.subplots(figsize=(18,8))
    pp1 = mpatches.PathPatch(
        Path(verts, codes),
        fc="none", transform=ax.transData, linewidth=1)

    ax.add_patch(pp1)
    # ax.plot(*list(zip(*verts)), "ro")

    ax.set_ylim(-20, 4)
    ax.set_xlim(-10, 96)
    # ax.grid()

    plt.tight_layout()
    plt.show()


def gen_path(pth):
    points = []
    points.append((Path.MOVETO, (0, 0, 0)))
    pos = [0, 0]

    line = 0
    x_scale = 1
    y_scale = 1
    slant = 0

    for p in pth:
        if p in " []":
            if p == "]":
                line += 4.4
                pos[0] = 0

            x_scale = 1
            y_scale = 1
            slant = 0

            if p == "[":
                pos[1] = -line
                points.append((Path.MOVETO, (line, *pos)))

        elif p == "=":
            y_scale *= phi**-1
        elif p == "-":
            x_scale *= phi**-1
        elif p == "+":
            x_scale *= phi
        elif p == "/":
            slant += 0.5 * x_scale
        elif p == "|":
            slant -= 0.5 * x_scale
        else:
            points.extend([(code, (line, pos[0] + x * x_scale + slant * y, pos[1] + y * y_scale))
                                for code, (x, y) in path[p]])
            pos[0] = points[-1][1][1]
            pos[1] = points[-1][1][2]

    codes, verts = list(zip(*points))

    verts = [(round(x + phi**-1 * 2 * (y + line), 6), round(y, 6)) for line, x, y in verts]
    print(verts)
    return verts, codes



chrmap = dict()
chrmap["0"]     = "---/d"

chrmap["01"]    = "/^ 'S"
chrmap["1"]     = "[-/d^ ||--PD"

chrmap["2"]     = "d '|/v /p '/b"
chrmap["2"]     = "[d^ |vv ^pvb"
chrmap["21"]    = "d '|/v /p 'S"

chrmap["3"]     = "-/dp '/q /~b"
chrmap["3"]     = "[dpqv /-~ vb"
chrmap["31"]    = "-/dp '/q /~ 'S"

chrmap["03"]    = "'q ~/b"

chrmap["4"]     = "-/dp//_< '-/|PB"
chrmap["4"]     = "[d+p---_< +PB----_"

chrmap["5"]     = "-/dp/_< '-/|PB ||d/|b"
chrmap["5"]     = "[d+pq<' +PBd"
chrmap["51"]    = "-/dp/_< '-/|PB ||d '_ '/-||PD/_"
chrmap["56"]    = "-/dp/_< '-/|PB ||d '/_ '2"

chrmap["6"]     = "-/dp '2"
chrmap["6"]     = "[dp2"
chrmap["06"]    = "-'|v |/p '2"

chrmap["7"]     = "-/|dp '_ '-/|PB"
chrmap["7"]     = "[d+p---_< +PB----_"
chrmap["07"]     = "-/|^p '_ '-/|PB"
chrmap["70"]    = "-/|dp '_ '-/|Pv"
chrmap["i7"]    = "-/|dp '_ '-/|Pv /|D '/>"
chrmap["71"]    = "-/|dp '_ '-/||PD/_"

chrmap["i8"]    = "/d|v /p '-/q /|D' />"
chrmap["80"]    = "/d|v /p '-/qv /D' />"
chrmap["8"]     = "/d|v /p '-/qb"
chrmap["8"]     = "[d+p---_< +PB----_"
chrmap["81"]    = "/d|v /p '-/q//D"

chrmap["9"]     = "-/dp '/qp '-/qb"
chrmap["9"]     = "[dpqv ^pqv"
chrmap["09"]    = "'/qp '-/qb"
chrmap["91"]    = "-/dp '/qp '-/q/D"
chrmap["96"]    = "-/dp '/qp '-/qv /p2"

chrmap["i"]     = "/db"
chrmap["u"]     = "/dbdb"


def merge(a, b):
    assert a[-1] == b[0]
    pa = chrmap[a]
    pb = chrmap[b]
    pc = chrmap[b[0]]

    prefix = 0
    suffix = 0

    while suffix < len(pa) and suffix < len(pc) and pa[-1-suffix] == pc[-1-suffix]:
        suffix += 1

    while prefix < len(pb) and prefix < len(pc) and pb[prefix] == pc[prefix]:
        prefix += 1

    return pa[:-suffix] + pc[len(pc) - suffix:prefix - len(pc)] + pb[prefix:]



def enc(s):
    pth = ""

    for c in s.split():
        if c in chrmap:
            pth += chrmap[c]
        elif len(c) == 3 and c.isdigit() and c[:-1] in chrmap and c[1:] in chrmap:
            pth += merge(c[:-1], c[1:])
        else:
            pth += c

        pth += " "

    print(pth)

    return pth



# plot_path(*gen_path(enc("i />//> ˘/<//< 31 7 8 1 4  0  ] i7 06 i8 /. 091 0  ] 51 2 31 96 0 ] i7 01 > 80 01 > 091 1")))
# plot_path(*gen_path(enc("3 > 2 > 1 ] 6 > 5 > 4 ] 9 > 8 > 7")))
plot_path(*gen_path(enc("] 3 > 2 > 1 ] 6 > 5 > 4 ] 9 > 8 > 7")))

