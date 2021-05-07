# plot graph utility

from utils import *
import matplotlib.pyplot as plt

def PlotCatesianPoints(pl):
    listx = []
    listy = []
    for p in pl:
        x,y = p.getdata()
        listx.append(x)
        listy.append(y)
    plt.scatter(listx, listy)
    plt.show()

def PlotPolarPoints(pl):
    cpl = []
    for p in pl:
        cp = CartesianPoint(Polar2Cartesian(p.getdata()))
        cpl.append(cp)
    PlotCatesianPoints(cpl)