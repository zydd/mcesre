import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from draw3 import *

class Gui:
    def __init__(self, prog, func, args=()):
        self.prog = prog
        self.func = func
        self.args = args
        self.plot = Plot()
        self._init_plot()
        self._init_gui()

    def _init_plot(self):
        fig, ax = plt.subplots(figsize=(8,6), dpi=100)
        pp1 = mpatches.PathPatch(Path([(0, 0)], [Path.MOVETO]), zorder=2, fill=False)

        patch = ax.add_patch(pp1)
        # ax.plot(*list(zip(*verts)), ".", zorder=1, color="#ff000040")

        ax.set_aspect('equal')

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        fig.tight_layout()

        self.ax = ax
        self.fig = fig
        self.patch = patch

    def _redraw(self, *args):
        t0 = time.time()
        self._update_plot()
        self.canvas.draw()
        print(f"rdr time: {time.time() - t0:.2f}")

    def _init_gui(self):
        self.window = tkinter.Tk()

        self.window.protocol("WM_DELETE_WINDOW", self.window.quit)
        self.w2 = tkinter.Scale(self.window, from_=0, to=15, orient=tkinter.HORIZONTAL, command=self._redraw, length=600)
        self.w2.set(5)
        self.w2.pack()

        self.canvas = FigureCanvasTkAgg(self.fig, self.window)
        self.canvas.get_tk_widget().pack()
        # self.canvas.draw()

    def _update_plot(self):
        itr = self.w2.get()

        codes, verts = self.plot.run(prog, self.func, itr, *self.args)

        t0 = time.time()

        xmin = verts[:,0].min()
        xmax = verts[:,0].max()
        ymin = verts[:,1].min()
        ymax = verts[:,1].max()
        by = (ymax - ymin) * 0.1
        bx = (xmax - xmin) * 0.1
        xlims = (xmin - bx, xmax + bx)
        ylims = (ymin - by, ymax + by)
        self.ax.set_xlim(*xlims)
        self.ax.set_ylim(*ylims)

        if len(codes) > 500000:
            codes = codes[:500000]
            verts = verts[:500000]

        self.patch.set_path(Path(verts, codes))
        print(f"upd time: {time.time() - t0:.2f}")

    def run(self):
        return self.window.mainloop()

