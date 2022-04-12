import numpy as np
import frame as fr

test = fr.Frame("test", np.array([[[0], [1], [0]], [[0], [2], [0]]]))
test.setOrigin([[0],[0],[0]])
a = np.deg2rad(90)
#test.rotateWithMatrix((np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])))
test.rotateAboutAxis([0,0,1], a)

test.print()
