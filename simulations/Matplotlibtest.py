import numpy as np
import matplotlib.pyplot as plt
# from IPython.display import display, clear_output

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1) 

for t in range(360):
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.plot(np.cos(t*np.pi/180), np.sin(t*np.pi/180), marker='.')
    # display(fig)    
    # clear_output(wait = True)
    # plt.pause(1)
plt.savefig('foo.jpg')