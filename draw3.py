import copy
import operator
import re
import time

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.path as mpath

plt.style.use("dark_background")

Path = mpath.Path

phi = (1 + 5**0.5)*0.5


def plot_path(codes, verts):
    ##print("Plot:", list(zip(codes, map(tuple, verts))))

    fig, ax = plt.subplots(figsize=((20 - 0) * 0.35, 20 * 0.35))
    pp1 = mpatches.PathPatch(Path(verts, codes), zorder=2, fill=False)

    ax.add_patch(pp1)
    # ax.plot(*list(zip(*verts)), ".", zorder=1, color="#ff000040")

    ax.set_ylim(0, 20)
    ax.set_xlim(0, 20)
    ax.grid(zorder=-1, color="#323232")

    plt.tight_layout()
    plt.show()


P = lambda x, y: np.array([x, y], dtype="double")


class State:
    def __init__(self):
        self.curv = P(0.5, 0.5)
        self.path = []
        self.stack = []
        self.pos = P(0, 0)
        self.rot = 0
        self.scale = P(1, 1)
        self.transformation_matrix = np.array([
            [1, 0],
            [0, 1],
        ], dtype="double")

    def clone(self):
        c = copy.deepcopy(self)
        c.path.clear()
        return c

    def transform(self, p):
        # p = np.array(p, dtype="double")
        # p *= self.scale
        # p += self.shear * list(reversed(p))
        #
        # if self.rot != 1:
        #     cos = np.cos(self.rot * 2 * np.pi)
        #     sin = np.sin(self.rot * 2 * np.pi)
        #     p = np.array((p[0] * cos - p[1] * sin, p[0] * sin + p[1] * cos), dtype='double')

        return self.transformation_matrix @ p

    def stretch_x(self, k):
        self.scale[0] *= k
        mat = np.array([
            [k, 0],
            [0, 1],
        ], dtype="double")

        self.transformation_matrix = self.transformation_matrix @ mat

    def stretch_y(self, k):
        self.scale[1] *= k
        mat = np.array([
            [1, 0],
            [0, k],
        ], dtype="double")

        self.transformation_matrix = self.transformation_matrix @ mat

    def shear_x(self, k):
        mat = np.array([
            [1, k],
            [0, 1],
        ], dtype="double")

        self.transformation_matrix = self.transformation_matrix @ mat

    def shear_y(self, k):
        mat = np.array([
            [1, 0],
            [k, 1],
        ], dtype="double")

        self.transformation_matrix = self.transformation_matrix @ mat

    def rotate(self, a):
        self.rot += a
        a *= 2 * np.pi
        cos = np.cos(a)
        sin = np.sin(a)
        mat = np.array([
            [cos, -sin],
            [sin, cos],
        ], dtype="double")

        self.transformation_matrix = self.transformation_matrix @ mat

    def translate(self, p):
        self.pos = self.pos + p
        return self.pos

    def scale_prop(self, **kwargs):
        keys = dict(
            x=(float, "scale", 0),
            y=(float, "scale", 1),
            c1=(float, "curv", 0),
            c2=(float, "curv", 1),
            r=(float, "rot", None)
        )

        ops = dict(
            d=operator.truediv,
            m=operator.mul,
            a=operator.add,
            s=operator.sub,
        )

        for k in kwargs:
            if kwargs[k] == "" or kwargs[k] is None:
                continue

            op = ops[k[0]]

            typ, name, idx = keys[k[1:]]

            if idx is not None:
                getattr(self, name)[idx] = op(getattr(self, name)[idx], typ(kwargs[k]))
            else:
                setattr(self, name, op(getattr(self, name), typ(kwargs[k])))


class Plot:
    def __init__(self):
        self.points = []

    def _condense_path(self, path):
        r = P(0, 0)
        for p in path:
            r += p
        return r

    def _tokenize(self, prog):
        tokens = [";"]
        i = 0

        while i < len(prog):
            if num := re.match(r"^\d*\.?\d+(e[+-]?\d+)?", prog[i:]):
                i += num.end()
                num = num[0]
                if "." in num or "e" in num:
                    num = float(num)
                else:
                    num = int(num)
                tokens.append(num)

            elif ident := re.match(r"^\$\d+", prog[i:]):
                tokens.append(ident[0])
                i += ident.end()

            elif ident := re.match(r"^\$\w+", prog[i:]):
                tokens.append(ident[0])
                i += ident.end()

            elif space := re.match(r"^\s+", prog[i:]):
                tokens.append(" ")
                i += space.end()

            elif prog[i] == ",":
                i += 1
            else:
                tokens.append(prog[i])
                i += 1

        tokens.append(" ")

        return tokens

    def _preprocess(self, prog):
        self.labels = dict()
        self.argc = dict()
        i = 1
        pop_num = False
        while i < len(prog)-1:
            #print(i, *prog)
            if (    prog[i] in ["+", "-", "*", "/", "c"]
                    and (type(prog[i+1]) in [int, float]
                        or prog[i+1].startswith("$"))):
                prog[i:i+2] = [prog[i+1], prog[i]]
                i += 1

            elif (  prog[i] in ["x", "y", "z", "r"]
                    and (type(prog[i+1]) in [int, float]
                        or prog[i+1].startswith("$"))):
                prog[i:i+2] = [prog[i+1], "/", prog[i]]
                i += 2

            elif prog[i] == "=":
                assert type(prog[i-2]) is int
                assert prog[i-1].startswith("$")
                self.labels[prog[i-1]] = i - 2
                self.argc[i-2] = prog[i-2]
                del prog[i-2:i+1]
                i -= 3

            i += 1

        return prog

    def _exec(self, prog, state, single_statement=False, ip=1, itr=None, depth=0):
        # #print(f"exec > \"{''.join(map(str, prog[ip:ip+4]))}\"", itr)
        initial_state = state.clone()
        start = ip

        def _args(n):
            assert len(state.stack) >= n
            args = state.stack[-n:]
            state.stack = state.stack[:-n]
            return args

        while ip < len(prog)-1:
            #print(f"{prog[ip]:<4} {ip} {depth}  {state.pos}  {state.stack}")

            if state.path and prog[ip] not in ["s", "l", "[", "]", ">", "v", "<", "^", "L", "M"]:
                if self.points[-1][0] == Path.MOVETO:
                    self.points.pop()
                self.points.append((Path.MOVETO, state.translate(self._condense_path(state.path))))
                state.path.clear()

            if type(prog[ip]) in [int, float]:
                state.stack.append(prog[ip])
                ip += 1
                continue

            if prog[ip].startswith("$"):
                value = self.labels.get(prog[ip])
                if value is None:
                    value = state.stack[-int(prog[ip][1:])]
                state.stack.append(value)
                ip += 1
                continue

            match prog[ip]:
                case ";" | "i":
                    pass

                case " ":
                    if single_statement:
                        break

                case "|":
                    pos = state.pos
                    state = initial_state.clone()
                    state.pos = pos

                case "[":
                    st, ip = self._exec(prog, state=state.clone(), ip=ip + 1, itr=itr, depth=depth)
                    if st.path:
                        state.path.append(self._condense_path(st.path))

                    state.pos = st.pos

                case "]":
                    break

                case "(":
                    _, ip = self._exec(prog, state=state.clone(), ip=ip + 1, itr=itr, depth=depth)
                    if self.points[-1][0] == Path.MOVETO:
                        self.points.pop()
                    self.points.append((Path.MOVETO, state.pos))

                case ")":
                    break

                case "^":
                    state.path.append(state.transform((0, 1)))
                case ">":
                    state.path.append(state.transform((1, 0)))
                case "v":
                    state.path.append(state.transform((0, -1)))
                case "<":
                    state.path.append(state.transform((-1, 0)))

                case "l":
                    for p in state.path:
                        self.points.append((Path.LINETO, state.translate(p)))
                    state.path.clear()

                case "M":
                    self.points.append((Path.MOVETO, self.points[-1][1]))

                case "L":
                    if len(self.points) > 1 and self.points[-1][0] == Path.MOVETO:
                        self.points.pop()
                        self.points.append((Path.LINETO, state.pos))

                case "s":
                    if type(prog[ip-1]) in [int, float]:
                        if ip >= 2 and type(prog[ip-2]) in [int, float]:
                            state.curv[0] = prog[ip-2]
                            state.curv[1] = prog[ip-1]
                        else:
                            state.curv[1] = state.curv[0] = prog[ip-1]

                    assert len(state.path) >= 3, state.path
                    assert len(state.path) % 2 == 1, state.path

                    v2 = state.path.pop(0)

                    while len(state.path) >= 2:
                        v1 = v2
                        p = state.path[0]
                        v2 = state.path[1]
                        state.path = state.path[2:]

                        self.points.append((Path.CURVE4, state.pos + v1 * state.curv[0]))
                        state.pos = state.pos + p
                        self.points.append((Path.CURVE4, state.pos - v2 * state.curv[1]))

                        self.points.append((Path.CURVE4, state.pos))

                    state.path.clear()

                case "c":
                    state.curv = _args(2)
                case "x":
                    state.stretch_x(_args(1)[0])
                case "y":
                    state.stretch_y(_args(1)[0])
                case "z":
                    v = _args(1)[0]
                    state.stretch_x(v)
                    state.stretch_y(v)
                case "r":
                    state.rotate(_args(1)[0])
                case "/":
                    num, den = _args(2)
                    state.stack.append(num/den)
                case "+":
                    lhs, rhs = _args(2)
                    state.stack.append(lhs + rhs)
                case "-":
                    lhs, rhs = _args(2)
                    state.stack.append(lhs - rhs)

                case ":":
                    start = ip + 1
                    for n in range(*_args(1)):
                        ##print(f"loop {n}")
                        state, ip = self._exec(prog, state=state, single_statement=True, ip=start, itr=n+1, depth=depth)
                        ##print(f"loopd {n}")
                    ip -= 1

                case "!":
                    label = _args(1)[0]
                    state, _ = self._exec(prog, state=state, single_statement=True, ip=label, depth=depth+1)

                    state.stack = state.stack[:-self.argc[label]]

                case "?":
                    ##print(state.stack, "cond")
                    cond = _args(1)[0]
                    if not cond:
                        level = 0
                        for j, c in enumerate(prog[ip+1:], start=ip+1):
                            if c == " " and level == 0:
                                break
                            elif c in ["[", "("]:
                                level += 1
                            elif c in ["]", ")"]:
                                level -= 1

                            if level < 0:
                                break
                        ip = j - 1

                case "b":
                    break

                case _:
                    assert False, prog[ip]

            ip += 1

        #print(f"exec {ip} {depth}: \"{''.join(map(str, prog[start:ip]))}\"", state.stack)
        return state, ip


    def gen_path(self, prog):
        tokens = self._tokenize(prog)
        tokens = self._preprocess(tokens)
        print(*tokens)

        state = State()

        if not self.points:
            self.points = [(Path.MOVETO, state.pos)]

        self._exec(tokens, state)

        return list(zip(*self.points))


plotter = Plot()


# plot_path(*plotter.gen_path("2x;2y[ 4y3v>^<vs y2^ v>^<vl vv 4y3v>^>v>^s 3x<y2^ v>^>v>^l"))
# plot_path(*plotter.gen_path("""
# 3:r10[>l<]
# """))
# #
# points = plotter.gen_path("""
# y2^
# ((v>l) ([2:v][v>][>]1s) >> (v>^>v>^s) (v>^>v>^l))
# 2yv
# (>l (y2v 4y3v>^<vs) >> (r3>l >l) (2r3>l >l) (>l))
# 3yv 10:r10(>l10:(ir10(x8>l)))
# >>>10:>l<r10
# >>> 10:r10[>l< ] >>>> 10:r10>l
# 4yv

# 10x<

# (2x;r4>l) > (r4;2x>l)

# > (vl) 3x> (vl) 3:[>] (vl) [3:>] (vl)

# """)

# points = plotter.gen_path("""v[>]vs""")
#


t0 = time.time()
# points = plotter.gen_path("""8y 13x >v|4z
# (3:1r3;6$tri!)
# ]
# $tri$1=>l(1r3;1z2;3:1r3[$1?$1-1$tri!])>l
# """)
points = plotter.gen_path("""10y;10x>^|4z;3r4
0.2z6

1:1r4;(M11$dra!)]
1$dra=[$1?1r8$1-1$dra!|7r8$1-1$drai!b 1z4;1r8> L >>[>v]vvl v]
1$drai=[$1?7r8$1-1$dra!|1r8$1-1$drai!b 1z4;1r8v L vv[v>]>>l >]


1$zdra=[$1?1r8$1-1$zdra!|7r8$1-1$zdra!b 1z4;1r8> L >>[>v]vvl v]
""")
print(f"time: {time.time() - t0:.2f} points: {len(points[0])}")
plot_path(*points)
