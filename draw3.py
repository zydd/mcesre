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
PATH_LINK_LAST = -1
PATH_MOVE_CUR = -2

phi = (1 + 5**0.5)*0.5

P = lambda x, y: np.array([x, y], dtype="double")

class State:
    def __init__(self):
        self.curv = P(0.5, 0.5)
        self.path = []
        self.stack = []
        self.pos = P(0, 0)
        self.transformation_matrix = np.array([
            [1, 0],
            [0, 1],
        ], dtype="double")

    def clone(self):
        c = copy.deepcopy(self)
        c.path.clear()
        return c

    def transform(self, p):
        return self.transformation_matrix @ p

    def stretch_x(self, k):
        mat = np.array([
            [k, 0],
            [0, 1],
        ], dtype="double")

        self.transformation_matrix = self.transformation_matrix @ mat

    def stretch_y(self, k):
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
        a = 2 * a * np.pi
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


class Plot:
    def __init__(self):
        self.reset()

    def reset(self, reset_pos=True):
        self.mem = dict()
        self.state = State()

        self.verts = [self.state.pos]
        self.cmds = [Path.MOVETO]

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
        self.verts.append(point)
        self.cmds.append(cmd)

    def _tokenize(self, prog):
        tokens = [";"]
        i = 0

        while i < len(prog):
            if ident := re.match(r"^#.*\n", prog[i:]):
                if tokens[-1] != " ":
                    tokens.append(" ")

                i += ident.end()

            elif num := re.match(r"^\d*\.?\d+(e[+-]?\d+)?", prog[i:]):
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
                if tokens[-1] != " ":
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
        functions = dict()
        conditionals = list()
        references = list()
        calls = list()

        operations = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            "p": operator.pow,
        }

        i = 1
        while i < len(prog)-1:
            # print(f"{i:<3}: ", *prog)

            if prog[i] in ["+", "-", "*", "/", "p"]:
                if type(prog[i+1]) in [int, float] and type(prog[i-1]) in [int, float]:
                    prog[i-1] = operations[prog[i]](prog[i-1], prog[i+1])
                    del prog[i:i+2]
                    i -= 1
                elif type(prog[i+1]) in [int, float] or prog[i+1].startswith("$"):
                    prog[i:i+2] = [prog[i+1], prog[i]]
                    i += 1

            elif prog[i] in ["x", "y", "z", "r"] and type(prog[i+1]) in [int, float]:
                if type(prog[i-1]) in [int, float]:
                    prog[i-1] /= prog[i+1]
                    del prog[i+1]
                else:
                    prog[i:i+2] = [prog[i+1], "/", prog[i]]
                    i += 2

            elif type(prog[i]) is str and prog[i].startswith("$"):
                if prog[i][1:].isdigit():
                    prog[i] = int(prog[i][1:])
                    prog.insert(i + 1, "$")
                else:
                    references.append(i)

            elif prog[i] == "=":
                assert type(prog[i-2]) is int
                assert prog[i-1].startswith("$")
                addr = i - 2
                name = prog[i-1]
                argc = prog[i-2]

                functions[name] = (addr, argc)

                del prog[i-2:i+1]
                references.pop()
                i -= 3

            elif prog[i] == "?":
                prog.insert(i, None)
                conditionals.append(i)
                i += 1

            elif prog[i] == "!":
                calls.append(i)
                prog.insert(i, None)
                i += 1

            i += 1

        for i in conditionals:
            level = 0
            for j, c in enumerate(prog[i+1:], start=i+1):
                if c == " " and level == 0:
                    break
                elif c in ["[", "("]:
                    level += 1
                elif c in ["]", ")"]:
                    level -= 1

                if level < 0:
                    break
            prog[i] = j

        for i in calls:
            addr, argc = functions[prog[i-1]]
            prog[i] = argc

        for i in references:
            fninfo = functions.get(prog[i])
            if fninfo:
                prog[i] = fninfo[0]

        return prog

    def _exec(self, prog, state, single_statement=False, ip=0, itr=None, depth=0):
        # print(f"exec > \"{''.join(map(str, prog[ip:ip+4]))}\"", itr)
        initial_state = state.clone()

        def _args(n):
            assert len(state.stack) >= n
            args = state.stack[-n:]
            state.stack = state.stack[:-n]
            return args

        while ip < len(prog)-1:
            print(f"{prog[ip]:<4} {ip} {depth}  {state.pos}  {state.stack}")

            if state.path and prog[ip] not in ["s", "l", "[", "]", ">", "v", "<", "^", "L", "M"]:
                self._add_point(Path.MOVETO, state.translate(self._condense_path(state.path)))
                state.path.clear()

            if type(prog[ip]) in [int, float]:
                state.stack.append(prog[ip])
                ip += 1
                continue

            match prog[ip]:
                case ";":
                    pass

                case " ":
                    if single_statement:
                        break

                case "$":
                    arg, = _args(1)
                    state.stack.append(initial_state.stack[-arg])

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
                    self._add_point(PATH_MOVE_CUR, self.verts[-1])

                case "L":
                    if self.cmds[-1] == Path.MOVETO:
                        self._add_point(PATH_LINK_LAST, state.pos)

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
                    v, = _args(1)
                    state.stretch_x(v)
                    state.stretch_y(v)
                case "r":
                    state.rotate(_args(1)[0])
                case "+":
                    lhs, rhs = _args(2)
                    state.stack.append(lhs + rhs)
                case "-":
                    lhs, rhs = _args(2)
                    state.stack.append(lhs - rhs)
                case "*":
                    lhs, rhs = _args(2)
                    state.stack.append(lhs * rhs)
                case "/":
                    num, den = _args(2)
                    state.stack.append(num/den)
                case "p":
                    base, exp = _args(2)
                    state.stack.append(base ** exp)

                case ":":
                    start = ip + 1
                    for n in range(*_args(1)):
                        state, ip = self._exec(prog, state=state, single_statement=True, ip=start, itr=n+1, depth=depth)
                    ip -= 1

                case "!":
                    addr, argc = _args(2)
                    key = (addr, tuple(state.stack[len(state.stack)-argc:]))
                    arg0 = len(state.stack)

                    if self.mem is not None and key in self.mem:
                        tra, dpos, verts, cmds, ret = self.mem[key]

                        for c, p in zip(cmds, verts):
                            self._add_point(c, state.pos + state.transform(p))

                        state.pos = state.pos + state.transform(dpos)
                        state.transformation_matrix = state.transformation_matrix @ tra

                        del state.stack[arg0-argc:arg0]
                        state.stack.extend(ret)
                    else:
                        p0 = len(self.verts)
                        tra0 = np.linalg.inv(state.transformation_matrix)
                        pos0 = state.pos

                        state, _ = self._exec(prog, state=state, single_statement=True, ip=addr, depth=depth+1)

                        if self.mem is not None:
                            tra = state.transformation_matrix @ tra0
                            verts = [tra0 @ (p - pos0) for p in self.verts[p0:]]
                            dpos = tra0 @ (state.pos - pos0)
                            ret = state.stack[arg0:]

                            self.mem[key] = (tra, dpos, verts, self.cmds[p0:], ret)

                            del state.stack[arg0-argc:arg0]

                case "?":
                    cond, stmt_end = _args(2)

                    if not cond:
                        ip = stmt_end - 1

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

    def run(self, prog, *args, nomem=False):
        t0 = time.time()

        self.reset()
        self.state.stack = list(args)

        if nomem:
            self.mem = None
        self._exec(prog, self.state)

        del self.mem

        print(f"run time: {time.time() - t0:.2f} points: {len(self.verts)}")

    def run_code(self, code):
        self.run(self.compile(code))

    def get_path(self):
        t0 = time.time()
        codes = np.array(self.cmds, dtype="int")
        verts = np.array(self.verts, dtype="double")

        # Only keep last of consecutive moves
        moves = np.hstack((codes != Path.MOVETO, [True]))
        d = (np.diff(moves.astype("int")) == 1)
        moves = np.logical_or(moves[:-1], d)
        codes = codes[moves]
        verts = verts[moves]

        move_curs = (codes == PATH_MOVE_CUR)
        codes[move_curs] = Path.MOVETO
        verts[1:][move_curs[1:]] = verts[:-1][move_curs[:-1]]

        links = (codes == PATH_LINK_LAST)
        codes[1:-1][links[2:]] = Path.LINETO

        nlinks = np.logical_not(links)
        codes = codes[nlinks]
        verts = verts[nlinks]

        assert len(codes) == len(verts)

        print(f"gen time: {time.time() - t0:.2f} points: {len(codes)}")
        return codes, verts

    def show(self):
        codes, verts = self.get_path()

        t0 = time.time()

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

        print(f"plt time: {time.time() - t0:.2f}")
        plt.show()


def dragon_animation(prog, itr, size=(8, 6), filename=None):
    plot.run(prog, 0)
    codes, verts = plot.get_path()

    fig, ax = plt.subplots(figsize=size, dpi=100)
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
        if i < itr:
            print(f"animate {i:2} ", end="")
            plot.run(prog, i)

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
        fig, animate, interval=2000, blit=False, frames=range(0,itr+3), repeat=False)

    if filename:
        ani.save(filename, dpi=200)

    plt.show()

plot = Plot()

dragon = plot.compile(
    """
    4:(M $1$dra! L)1r4

    ]

    1$dra=[$1?1r8$1-1$dra!|7r8$1-1$drai!b 1z4;1r8> L >>[>v]vvl v]
    1$drai=[$1?7r8$1-1$dra!|1r8$1-1$drai!b 1z4;1r8v L vv[v>]>>l >]

    1$zdra=[$1?1r8$1-1$zdra!|7r8;0-1y$1-1$zdra!b 1z4;1r8> L >>[>v]vvl v]
    1$ldra=[$1?1r8$1-1$ldra!|7r8$1-1$ldra!b 1z4;1r8> L >>[>v]vvl v]
""")
hilbert = plot.compile(
    """
    1 2 1$1+p 1-/z
    $1$hil!]
    1$hil=[$1?$1-1[3r4;0-1x$hil! | ^l $hil! | >l $hil! | vl 1r4;0-1x$hil!]b ^>vl]
""")
gosper = plot.compile(
    """
    $1$S!
    ]
    1$Z=[?$1-1[1r6 1z2 $1$Z! 5r6 $1$Z! 4r6 $1$1$Z!$Z! 2r6 $1$Z! 1r6 $1$Z!]b $z!]
    0$z=[1r6 1z2 >l  5r6 >l  4r6 >>l    2r6 >l  1r6 >l ]

    1$S=,[?$1-1[    $1$S! 1r6   $1$SI!      2r6 $1$SI!  5r6 $1$S!  4r6 $1$1$S!$S! 5r6 $1$SI!]b $s!]
    1$SI=[?$1-1[5r6 $1$S! 1r6 $1$1$SI!$SI!  2r6 $1$SI!  1r6 $1$S!  4r6   $1$S!    5r6 $1$SI!]b $si!]
    0$s=,[2z5     >l 1r6  >l  2r6 >l  5r6 >l  4r6 >>l  5r6 >l]
    0$si=[2z5 5r6 >l 1r6 >>l  2r6 >l  1r6 >l  4r6 >l   5r6 >l]
    ]
""")

zcurve = plot.compile(
    """
    $1$z! [$1$len!y>^] $1$z! (1r8 4:(>l)1r4)]

    1$z=[$1?[$1-1[L $1$z! [$1$len! y>^] L $1$z! [$2$len! x<] [v] L $1$z! [$1$len! y>^] L $1$z! ]b] >[<v]>l]

    1$len=2$1p*2-1
""")

plot.run(dragon, 15)
# plot.run(hilbert, 5)
# plot.run(gosper, 3)
# plot.run(zcurve, 4)
plot.show()

# dragon_animation(hilbert, 8, size=(6,6), filename="hilbert.mp4")
