from matplotlib import pyplot as pl
import numpy as np
import time





class GetXY:
    def __init__(self, ax, nstars):
        self.nstars = nstars
        self.ax = ax
        self.xs = []
        self.ys = []
        self.cid = ax.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        if len(self.xs) == 2*self.nstars-1:
            self.ax.figure.canvas.mpl_disconnect(self.cid)
            pl.show(block=False)
            time.sleep(0.2)
            pl.close('all')
        print('click', event)
        self.ax.axvline(event.xdata, color='red')
        self.ax.figure.canvas.draw_idle()
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)


def plot_and_collect_xvals(x, y, nstars):

    fig = pl.figure()
    ax=fig.add_subplot(111)
    ax.plot(x, y)
    ax.set_title(f"Select bounds for stars in order")
    xy = GetXY(ax, nstars)
    pl.show()
    return xy.xs

if __name__ == '__main__':
    plot_and_collect_xvals(np.linspace(0,10, 100), np.sin(np.linspace(0,10, 100)), 2)


