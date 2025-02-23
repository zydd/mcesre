import collections
import copy
import operator
import re
import sys
import time

import numpy as np

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
        self.iteration = 0
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


class Program:
    def __init__(self, prog, functions):
        self.mem = dict()
        self.prog = prog
        self.functions = functions
        self.debug = False

    def _exec(self, plot, state, ip, stack_top, single_statement=False):
        # print(f"exec > \"{''.join(map(str, prog[ip:ip+4]))}\"", itr)
        initial_state = state.clone()
        stack_drop = 0

        def _args(n):
            assert len(state.stack) >= n
            args = state.stack[-n:]
            state.stack = state.stack[:-n]
            return args

        while ip < len(self.prog):
            self.debug and print(f"{self.prog[ip]:<4} {ip} {state.pos}  {state.stack}")

            if type(self.prog[ip]) in [int, float]:
                state.stack.append(self.prog[ip])
                ip += 1
                continue

            match self.prog[ip]:
                case " " | "\n":
                    if single_statement:
                        break

                case "$":
                    arg, = _args(1)
                    if arg:
                        state.stack.append(state.stack[stack_top+arg-1])
                    else:
                        state.stack.append(state.iteration)

                case "|":
                    pos = state.pos
                    state = initial_state.clone()
                    state.pos = pos

                case "[":
                    tm = state.transformation_matrix
                    state, ip = self._exec(plot, state, ip + 1, stack_top)
                    state.transformation_matrix = tm

                case "]":
                    break

                case "(":
                    _, ip = self._exec(plot, state.clone(), ip + 1, stack_top)
                    plot.add_point(Path.MOVETO, state.pos)

                case ")":
                    break

                case "{":
                    p0 = len(plot.verts)
                    st, ip = self._exec(plot, state.clone(), ip + 1, stack_top)
                    state.pos = st.pos
                    pos = plot.verts[-1]
                    plot.cmds = plot.cmds[:p0]
                    plot.verts = plot.verts[:p0]
                    plot.add_point(Path.MOVETO, pos)

                case "}":
                    break

                case ">":
                    plot.add_point(Path.LINETO, state.translate(state.transform((1, 0))))

                case "v":
                    plot.add_point(Path.LINETO, state.translate(state.transform((0, -1))))

                case "<":
                    plot.add_point(Path.LINETO, state.translate(state.transform((-1, 0))))

                case "^":
                    plot.add_point(Path.LINETO, state.translate(state.transform((0, 1))))

                case ";":
                    plot.add_point(Path.MOVETO, state.translate(state.transform((1, 0))))

                case "M":
                    plot.add_point(PATH_MOVE_CUR, plot.verts[-1])

                case "C":
                    if plot.cmds[-1] == Path.MOVETO:
                        plot.add_point(PATH_LINK_LAST, state.pos)

                case "s":
                    assert len(plot.verts) >= 4

                    path = plot.verts[-4:]
                    plot.verts = plot.verts[:-3]
                    plot.cmds = plot.cmds[:-3]

                    v1 = path[1]
                    p = path[0] + path[2] - path[1]
                    v2 = p - path[3] + path[2]

                    plot.add_point(Path.CURVE4, v1)
                    plot.add_point(Path.CURVE4, v2)
                    plot.add_point(Path.CURVE4, p)
                    state.pos = p

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

                        plot.add_point(Path.CURVE3, curve[0][1] - 0.25 * v)
                        plot.add_point(Path.CURVE3, curve[0][1])

                        for i in range(1, len(curve)-1):
                            plot.add_point(Path.CURVE4, curve[i-1][1] + 0.25 * v)
                            v1 = v2
                            v2 = curve[i+1][1] - curve[i][1]
                            v = v1 + v2
                            plot.add_point(Path.CURVE4, curve[i][1] - 0.25 * v)
                            plot.add_point(Path.CURVE4, curve[i][1])


                        plot.add_point(Path.CURVE3, curve[-2][1] + 0.25 * v)
                        plot.add_point(Path.CURVE3, curve[-1][1])

                case "x":
                    state.stretch_x(_args(1)[0])
                case "y":
                    state.stretch_y(_args(1)[0])
                case "z":
                    v, = _args(1)
                    state.stretch_x(v)
                    state.stretch_y(v)
                case "r":
                    state.rotate(-_args(1)[0])
                case "l":
                    state.rotate(_args(1)[0])
                case "R":
                    state.rotate(-0.5+_args(1)[0])
                case "L":
                    state.rotate(0.5-_args(1)[0])
                case "i":
                    state.shear_x(_args(1)[0])
                case "j":
                    state.shear_y(_args(1)[0])
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
                case "G":
                    lhs, rhs = _args(2)
                    state.stack.append(lhs > rhs)

                case ":":
                    start = ip + 1
                    for n in range(*_args(1)):
                        state.iteration = n
                        state, ip = self._exec(plot, state, start, stack_top, single_statement=True)
                    ip -= 1

                case "=":
                    stack_drop, *_ = _args(1)
                    stack_top = len(state.stack) - stack_drop

                case "!":
                    addr, *_ = _args(1)
                    state, _ = self._exec(plot, state, addr, stack_top, single_statement=True)

                case "@":
                    addr, idx = _args(2)
                    state.stack.append(self.prog[addr + idx])

                case "`":
                    addr, argc = _args(2)
                    key = (addr, tuple(state.stack[len(state.stack)-argc:]))

                    if self.mem is not None and key in self.mem:
                        tra, dpos, verts, cmds, ret = self.mem[key]

                        # for c, p in zip(cmds, verts):
                        #     plot.add_point(c, state.pos + state.transform(p))

                        if len(verts):
                            verts = state.transformation_matrix @ verts
                            verts[0,:] += state.pos[0]
                            verts[1,:] += state.pos[1]

                        plot.cmds.extend(cmds)
                        plot.verts.extend(verts.T)

                        state.pos = state.pos + state.transform(dpos)
                        state.transformation_matrix = state.transformation_matrix @ tra

                        arg0 = len(state.stack)
                        # print("callm del", state.stack[arg0-argc:arg0], "stack=", state.stack)
                        del state.stack[arg0-argc:arg0]
                        state.stack.extend(ret)
                    else:
                        p0 = len(plot.verts)
                        tra0 = np.linalg.inv(state.transformation_matrix)
                        pos0 = state.pos
                        arg0 = len(state.stack) - argc

                        state, _ = self._exec(plot, state, addr, stack_top, single_statement=True)

                        if self.mem is not None:
                            tra = state.transformation_matrix @ tra0
                            # verts = [tra0 @ (p - pos0) for p in plot.verts[p0:]]
                            verts = np.array(plot.verts[p0:], dtype="double")
                            if len(verts):
                                verts[:,0] -= pos0[0]
                                verts[:,1] -= pos0[1]
                                verts = tra0 @ verts.T

                            dpos = tra0 @ (state.pos - pos0)
                            ret = state.stack[arg0:]

                            self.mem[key] = (tra, dpos, verts, plot.cmds[p0:], ret)

                case "?":
                    cond, stmt_end = _args(2)

                    if not cond:
                        ip = stmt_end - 1

                case "P":
                    _args(1)

                case "b":
                    break

                case _:
                    assert False, self.prog[ip]

            ip += 1

        # print("exec del:", state.stack[stack_top:stack_top + stack_drop], state.stack)
        del state.stack[stack_top:stack_top + stack_drop]

        # print(f"exec {ip}:", state.stack)
        return state, ip


class Compiler:
    @staticmethod
    def _tokenize(prog):
        tokens = [" "]
        i = 0

        while i < len(prog):
            if ident := re.match(r"^#.*\n", prog[i:]):
                if tokens[-1] != " ":
                    tokens.append(" ")

                i += ident.end()

            elif string := re.match(r'^".*?(?<!\\)"', prog[i:]):
                tokens.extend(map(ord, string[0][1:-1]))
                i += string.end()

            elif sep := re.match(r"^,\s*", prog[i:]):
                i += sep.end()

            elif eq := re.match(r"^=\s*", prog[i:]):
                tokens.append("=")
                i += eq.end()

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

            elif prog[i] == "\n":
                tokens.append("\n")
                i += 1

            elif space := re.match(r"^\s+", prog[i:]):
                if tokens[-1] != " ":
                    tokens.append(" ")
                i += space.end()

            else:
                tokens.append(prog[i])
                i += 1

        tokens.append(" ")

        return tokens

    @staticmethod
    def _preprocess(prog):
        functions = collections.OrderedDict()
        conditionals = list()
        references = list()
        calls = list()

        operations = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            "p": operator.pow,
            "G": operator.gt,
        }

        i = 1
        while i < len(prog)-1:
            # print(f"{i:<3}: {prog[i]:<3} ", prog[i-3:i+3])

            # infix
            if prog[i] in ["+", "-", "*", "/", "p", "G", "@"]:
                if type(prog[i+1]) in [int, float] and type(prog[i-1]) in [int, float]:
                    prog[i-1] = operations[prog[i]](prog[i-1], prog[i+1])
                    del prog[i:i+2]
                    i -= 1
                elif type(prog[i+1]) in [int, float]:
                    prog[i:i+2] = [prog[i+1], prog[i]]
                    i += 1
                elif type(prog[i+1]) is str and prog[i+1].startswith("$"):
                    if prog[i+1][1:].isdigit():
                        prog[i:i+2] = [int(prog[i+1][1:]), "$", prog[i]]
                        i += 2
                    else:
                        prog[i:i+2] = [prog[i+1], prog[i]]
                        references.append(i)
                        i += 1

            elif prog[i] in ["x", "y", "z", "l", "r", "L", "R"] and type(prog[i+1]) in [int, float]:
                if type(prog[i-1]) in [int, float]:
                    prog[i-1] /= prog[i+1]
                    del prog[i+1]
                else:
                    prog[i:i+2] = [1 / prog[i+1], prog[i]]
                    i += 1

            elif type(prog[i]) is str and prog[i].startswith("$"):
                if prog[i][1:].isdigit():
                    prog[i] = int(prog[i][1:])
                    prog.insert(i+1, "$")
                    i += 1
                else:
                    references.append(i)

            elif prog[i] == "=":
                assert prog[i-1].startswith("$")
                name = prog[i-1]

                del prog[i-1]
                i -= 1

                if type(prog[i-1]) is int:
                    argc = prog[i-1]
                    addr = i-1
                else:
                    argc = 0
                    addr = i

                    del prog[i]
                    i -= 1

                functions[name] = (addr, argc)
                references.pop()

            elif prog[i] == "?":
                prog.insert(i, None)
                conditionals.append(i)
                i += 1

            elif prog[i] == "!":
                if type(prog[i-1]) is str and prog[i-1].startswith("$") and len(prog[i-1]) > 1:
                    prog[i] = "`"
                    calls.append(i)
                    prog.insert(i, None)
                    i += 1

            i += 1

        for i in conditionals:
            level = 0
            for j, c in enumerate(prog[i+1:], start=i+1):
                if c == " " and level == 0:
                    break
                elif c in ["{", "[", "("]:
                    level += 1
                elif c in ["}", "]", ")"]:
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

        return prog, functions

    @staticmethod
    def compile(code):
        tokens = Compiler._tokenize(code)
        prog, functions = Compiler._preprocess(tokens)
        return Program(prog, functions)


class Plot:
    def __init__(self):
        self.reset()

    def reset(self, reset_pos=True):
        self.state = State()

        self.verts = [self.state.pos]
        self.cmds = [Path.MOVETO]

    def condense_path(self, path):
        r = P(0, 0)
        for p in path:
            r += p
        return r

    def add_point(self, cmd, point):
        self.verts.append(point)
        self.cmds.append(cmd)

    def run(self, prog, fn=None, *args):
        ip = 0
        if fn is not None:
            ip, argc = prog.functions[fn]
            # assert len(args) == argc

        self.state.stack = list(args)

        # if not memoize:
        #     self.mem = None
        # elif memoize and not self.mem:
        #     self.mem = dict()

        prog._exec(self, self.state, ip, 0, single_statement=bool(ip))
        return self.state.stack

    def run_code(self, prog, *args):
        return self.run(Compiler.compile(prog), *args)

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
        codes[:-1][links[1:]] = Path.LINETO

        nlinks = np.logical_not(links)
        codes = codes[nlinks]
        verts = verts[nlinks]

        if codes[0] != Path.MOVETO:
            codes = np.hstack([[Path.MOVETO], codes])
            verts = np.vstack([[self.verts[0]], verts])

        assert len(codes) == len(verts)

        # print(f"gen time: {time.time() - t0:.2f} points: {len(codes)}")
        return codes, verts

    def show(self, scale=1):
        codes, verts = self.get_path()

        # t0 = time.time()

        fig, ax = plt.subplots(figsize=(8*scale, 6*scale))
        pp1 = mpatches.PathPatch(Path(verts, codes), zorder=2, fill=False)

        ax.add_patch(pp1)
        # ax.plot(*list(zip(*verts)), ".", zorder=1, color="#ff000040")

        xmin = verts[:,0].min()
        xmax = verts[:,0].max()
        ymin = verts[:,1].min()
        ymax = verts[:,1].max()
        by = (ymax - ymin) * 0.1
        bx = (xmax - xmin) * 0.1

        if bx == 0 and by == 0:
            return

        ax.set_xlim(xmin - bx, xmax + bx)
        ax.set_ylim(ymin - by, ymax + by)
        ax.grid(zorder=-1, color="#111")
        ax.set_aspect('equal')

        plt.tight_layout()

        # print(f"plt time: {time.time() - t0:.2f}")
        plt.show()


if __name__ == "__main__":
    with open(sys.argv[1], "r", encoding="utf8") as f:
        prog = Compiler.compile(f.read())

    print(*prog.prog)

    plot = Plot()

    t0 = time.time()
    res = plot.run(prog)
    print(f"run time: {time.time() - t0:.2f} points: {len(plot.verts)}")
    print(f"result: {res}")

    plot.show()
