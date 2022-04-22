import matplotlib.pyplot as plt
import numpy as np
import time
from IPython.display import display, clear_output
import Matrcies.frame as fr

#units are in mm

delay = 1

arm = defineArm()

def defineArm():
    R3 = fr.rotateJoint("R3", [-1,0,0], [0,0,0])
    L2 = fr.linkage("L2", [0,0,0], [0,0,105])
    L2.addFrame(R3)
    R2 = fr.rotateJoint("R2", [1,0,0], [0,0,0])
    R2.addFrame(L2)
    L1 = fr.linkage("L1", [[0,0,0], [0, 0, 80]])
    L1.addFrame(R2)
    R1 = fr.rotateJoint("R1", [0,0,1], [0,0,0], [])
    R1.addFrame(L1)



data = R1.getPoints()


fig = plt.figure()




for d in data:
    ax = fig.add_subplot(projection='3d')
    eps = 1e-16
    ax.axes.set_xlim3d(left=-10.-eps, right=10+eps)
    ax.axes.set_ylim3d(bottom=-10.-eps, top=10+eps) 
    ax.axes.set_zlim3d(bottom=-10.-eps, top=10+eps) 
    for i in d:
        ax.scatter(i[0], i[1], i[2], marker='o')
    display(fig)
    clear_output(wait = True)
    plt.pause(delay)
plt.show()
