import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots()
x_coords = np.array([0])
y_coords = np.array([0])
for t in range(360):
    x_coords.extend(np.cos(t))
    y_coords.extend(np.sin(t))
    plt.scatter(x_coords, y_coords)
    