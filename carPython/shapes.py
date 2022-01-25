import math
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, clear_output


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_xlim(0, 6)
ax.set_ylim(0, 6)
point1 = [3, 3]
point2 = [4, 2]
point3 = [3, 3]
point4 = [1, 0]
IntervalTime = 0.5
travel_speed = 1


def length(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1])


def distance(v, w):
    return math.sqrt(math.pow(v[1] - w[1], 2) + math.pow(v[0] - w[0], 2))


def angle_clockwise(A, B):
    inner = inner_angle(A, B)
    det = determinant(A, B)
    if det > 0:
        return inner
    else:
        return 2 * np.pi - inner


def dot_product(v, w):
    return v[0] * w[0] + v[1] * w[1]


def determinant(v, w):
    return v[0] * w[1] - v[1] * w[0]


def inner_angle(v, w):
    return math.acos(dot_product(v, w) / (length(v) * length(w)))


def path(start_point, end_point):
    # calculate the distance between the start and end points
    distance = math.sqrt(math.pow(end_point[1] - start_point[1], 2) + math.pow(end_point[0] - start_point[0], 2))
    distance_covered = 0
    # determines if the lines grows in the positive or negative y direction
    moving_vertical = 1
    if end_point[1] < start_point[1]:
        moving_vertical = -1
    # determines if the lines grows in the positive or negative x direction
    moving_horizontal = 1
    if end_point[0] - start_point[0] < 0:
        moving_horizontal = -1
    # special case for vertical lines
    if start_point[0] == end_point[0]:
        for t in range(int(distance/travel_speed) + 1):
            x_coord = start_point[0]
            y_coord = distance_covered * moving_vertical + start_point[1]
            display_point(x_coord, y_coord)
            distance_covered += travel_speed
    else:
        slope = (end_point[1] - start_point[1])/(abs(end_point[0] - start_point[0]))
        theta = math.atan(slope)
        for t in range(int(distance/travel_speed) + 1):
            x_coord = math.cos(theta) * distance_covered * moving_horizontal + start_point[0]
            y_coord = math.sin(theta) * distance_covered + start_point[1]
            display_point(x_coord, y_coord)
            distance_covered += travel_speed


def display_point(x_coord, y_coord):
    ax.plot(x_coord, y_coord, marker='.')
    display(fig)
    clear_output(wait=True)
    plt.pause(IntervalTime)


def draw_circle():
    center = point1
    prev_point = point2
    radius = distance(prev_point, center)
    vector = [prev_point[0] - center[0], prev_point[1] - center[1]]
    initial_angle = angle_clockwise([3, 0], vector)
    arc_measure = travel_speed / radius    # in radians
    display_point(prev_point[0], prev_point[1])
    for t in range(int(2 * np.pi / arc_measure)):
        x_coord = np.cos(1 + initial_angle + t * arc_measure) * radius + center[0]
        y_coord = np.sin(1 + initial_angle + t * arc_measure) * radius + center[1]
        next_point = [x_coord, y_coord]
        display_point(x_coord, y_coord)
        prev_point = next_point
    plt.show()


def draw_quad():
    path(point1, point2)
    path(point2, point3)
    path(point3, point4)
    path(point4, point1)
    plt.show()


draw_circle()
# draw_quad()
