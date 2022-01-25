from cmath import sqrt
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import math

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1) 

Point1 = [1,1]
Point2 = [4,3]
Point3 = [3,4]
Point4 = [2,2]
PauseTime = 1

def path(start_point, end_point, speed):
    distance = math.sqrt(math.pow(end_point[1] - start_point[1],2) + math.pow(end_point[0] - start_point[0],2))
    distance_covered = 0
    if start_point[0] == end_point[0]:
        moving_vertical = 1
        if end_point[1] < start_point[1]:
            moving_vertical = -1
        for t in range(int(distance/speed) + 1):
            x_coord = start_point[0]
            y_coord = distance_covered * moving_vertical + start_point[1]
            ax.plot(x_coord, y_coord, marker='.')
            display(fig) 
            clear_output(wait = True)
            plt.pause(PauseTime)
            distance_covered += speed
    else:
        moving_horizontal = 1
        if end_point[0] - start_point[0] < 0:
                moving_horizontal = -1
        slope = (end_point[1] - start_point[1])/(abs(end_point[0] - start_point[0]))
        theta = math.atan(slope)
        for t in range(int(distance/speed) + 1):
            x_coord = math.cos(theta) * distance_covered * moving_horizontal + start_point[0]
            y_coord = math.sin(theta) * distance_covered + start_point[1]
            ax.plot(x_coord, y_coord, marker='.')
            display(fig) 
            clear_output(wait = True)
            plt.pause(PauseTime)
            distance_covered += speed
ax.set_xlim(-1, 5)
ax.set_ylim(-1, 5)
path(Point1, Point2, 1)
path(Point2, Point3, 1)
path(Point3, Point4, 1)
path(Point4, Point1, 1)
plt.pause(100);