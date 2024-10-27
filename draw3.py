import copy
import operator
import re
import time

import numpy as np

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.path as mpath

plt.style.use("dark_background")

Path = mpath.Path

phi = (1 + 5**0.5)*0.5





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
        self.reset()

    def reset(self, reset_pos=True):
        self.state = State()

        self.points = [(Path.MOVETO, self.state.pos)]

        self.xmin = float('inf')
        self.xmax = float('-inf')
        self.ymin = float('inf')
        self.ymax = float('-inf')


    def _condense_path(self, path):
        r = P(0, 0)
        for p in path:
            r += p
        return r

    def _add_point(self, cmd, point):
        self.xmin = min(self.xmin, point[0])
        self.xmax = max(self.xmax, point[0])
        self.ymin = min(self.ymin, point[1])
        self.ymax = max(self.ymax, point[1])
        self.points.append((cmd, point))

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
        # print(f"exec > \"{''.join(map(str, prog[ip:ip+4]))}\"", itr)
        initial_state = state.clone()

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
                self._add_point(Path.MOVETO, state.translate(self._condense_path(state.path)))
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
                case ";":
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
                    self._add_point(Path.MOVETO, state.pos)

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
                        self._add_point(Path.LINETO, state.translate(p))
                    state.path.clear()

                case "M":
                    self._add_point(Path.MOVETO, self.points[-1][1])

                case "L":
                    if len(self.points) > 1 and self.points[-1][0] == Path.MOVETO:
                        self.points.pop()
                        self._add_point(Path.LINETO, state.pos)

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

                        self._add_point(Path.CURVE4, state.pos + v1 * state.curv[0])
                        state.pos = state.pos + p
                        self._add_point(Path.CURVE4, state.pos - v2 * state.curv[1])

                        self._add_point(Path.CURVE4, state.pos)

                    state.path.clear()

                case "S":
                    begin = 0
                    while self.points[begin - 1][0] == Path.LINETO:
                        begin -= 1

                    # Need at least 2 line segments to make a spline
                    if -begin >= 2:
                        curve = self.points[begin:]
                        self.points = self.points[:begin]

                        v1 = curve[0][1] - self.points[-1][1]
                        v2 = curve[1][1] - curve[0][1]
                        v = v1 + v2

                        self._add_point(Path.CURVE3, curve[0][1] - 0.25 * v)
                        self._add_point(Path.CURVE3, curve[0][1])

                        for i in range(1, len(curve)-1):
                            self._add_point(Path.CURVE4, curve[i-1][1] + 0.25 * v)
                            v1 = v2
                            v2 = curve[i+1][1] - curve[i][1]
                            v = v1 + v2
                            self._add_point(Path.CURVE4, curve[i][1] - 0.25 * v)
                            self._add_point(Path.CURVE4, curve[i][1])


                        self._add_point(Path.CURVE3, curve[-2][1] + 0.25 * v)
                        self._add_point(Path.CURVE3, curve[-1][1])



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

    def compile(self, code):
        tokens = self._tokenize(code)
        prog = self._preprocess(tokens)
        print(*prog)
        return prog

    def run(self, prog, *args):
        t0 = time.time()

        self.reset()
        self.state.stack = list(args)
        self._exec(prog, self.state)

        print(f"time: {time.time() - t0:.2f} points: {len(self.points)}")

    def run_code(self, code):
        self.run(self.compile(code))

    def get_path(self):
        return list(zip(*self.points))

    def show(self):
        codes, verts = self.get_path()

        fig, ax = plt.subplots(figsize=(8, 6))
        pp1 = mpatches.PathPatch(Path(verts, codes), zorder=2, fill=False)

        ax.add_patch(pp1)
        # ax.plot(*list(zip(*verts)), ".", zorder=1, color="#ff000040")

        by = (self.ymax - self.ymin) * 0.1
        bx = (self.xmax - self.xmin) * 0.1
        ax.set_xlim(self.xmin - bx, self.xmax + bx)
        ax.set_ylim(self.ymin - by, self.ymax + by)
        ax.grid(zorder=-1, color="#323232")
        ax.set_aspect('equal')

        plt.tight_layout()
        plt.show()


def dragon_animation():
    plot = Plot()

    dragon = plot.compile("""
        M $dra!L

        ]

        1$dra=[$1?1r8$1-1$dra!|7r8$1-1$drai!b 1z4;1r8> L >>[>v]vvl v]
        1$drai=[$1?7r8$1-1$dra!|1r8$1-1$drai!b 1z4;1r8v L vv[v>]>>l >]

        1$ldra=[$1?1r8$1-1$ldra!|7r8$1-1$ldra!b 1z4;1r8> L >>[>v]vvl v]
    """)

    plot.run(dragon, 10)
    plot.show()

    codes, verts = plot.get_path()

    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
    pp1 = mpatches.PathPatch(Path(verts, codes), zorder=2, fill=False)

    patch = ax.add_patch(pp1)
    # ax.plot(*list(zip(*verts)), ".", zorder=1, color="#ff000040")

    ax.set_aspect('equal')


    by = (plot.ymax - plot.ymin) * 0.1
    bx = (plot.xmax - plot.xmin) * 0.1
    xlims = (plot.xmin - bx, plot.xmax + bx)
    ylims = (plot.ymin - by, plot.ymax + by)
    ax.set_xlim(*xlims)
    ax.set_ylim(*ylims)


    plt.axis('off')
    plt.tight_layout()


    def animate(i):
        print(f"animate {i}")

        if i < 15:
            plot.run(dragon, i)

        by = (plot.ymax - plot.ymin) * 0.1
        bx = (plot.xmax - plot.xmin) * 0.1
        xlims = (plot.xmin - bx, plot.xmax + bx)
        ylims = (plot.ymin - by, plot.ymax + by)
        ax.set_xlim(*xlims)
        ax.set_ylim(*ylims)

        codes, verts = plot.get_path()
        patch.set_path(Path(verts, codes))
        return patch,


    ani = animation.FuncAnimation(
        fig, animate, interval=500, blit=False, frames=range(1,20), repeat=False)
    # ani.save("dragon.gif")
    plt.show()


dragon_animation()
