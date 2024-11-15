from draw3 import *

def dragon_animation(prog, itr, size=(8, 6), filename=None):
    plot.run(prog, 0)
    codes, verts = plot.get_path()

    fig, ax = plt.subplots(figsize=size, dpi=100)
    pp1 = mpatches.PathPatch(Path(verts, codes), zorder=2, fill=False)

    patch = ax.add_patch(pp1)
    # ax.plot(*list(zip(*verts)), ".", zorder=1, color="#ff000040")

    ax.set_aspect('equal')

    xmin = verts[:,0].min()
    xmax = verts[:,0].max()
    ymin = verts[:,1].min()
    ymax = verts[:,1].max()
    by = (ymax - ymin) * 0.1
    bx = (xmax - xmin) * 0.1
    xlims = (xmin - bx, xmax + bx)
    ylims = (ymin - by, ymax + by)
    ax.set_xlim(*xlims)
    ax.set_ylim(*ylims)

    plt.axis('off')
    plt.tight_layout()

    def animate(i):
        if i < itr:
            print(f"animate {i:2} ", end="")
            plot.run(prog, i)

            by = (ymax - ymin) * 0.1
            bx = (xmax - xmin) * 0.1
            xlims = (xmin - bx, xmax + bx)
            ylims = (ymin - by, ymax + by)
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
