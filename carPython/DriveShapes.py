import math
from sqlite3 import Time
import time
import sched
import numpy as np
import mecanum_py_by_wheel_encodeSpeed as drive

s = sched.scheduler(time.time, time.sleep)
point1 = [0, 0]
point2 = [30, 30]
point3 = [3, 3]
point4 = [1, 3]
Path_Points = [[0,0]]
IntervalTime = 0
travel_speed = 50
speed_mult = 1


def length(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1])


def distance(v, w):
    return math.sqrt(math.pow(v[1] - w[1], 2) + math.pow(v[0] - w[0], 2))


def midpoint(x1, x2):
    return [(x1[0] + x2[0]) / 2, (x1[1] + x2[1]) / 2]


def path(start_point, end_point, carryover=0):
    # calculate the distance between the start and end points
    distance = math.sqrt(math.pow(end_point[1] - start_point[1], 2) + math.pow(end_point[0] - start_point[0], 2))
    distance_covered = carryover
    vector = [end_point[0] - start_point[0], end_point[1] - start_point[1]]
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
        for t in range(int((distance-carryover)/travel_speed) + 1):
            x_coord = start_point[0]
            y_coord = distance_covered * moving_vertical + start_point[1]
            # display_point(x_coord, y_coord)
            distance_covered += travel_speed
    else:
        slope = (end_point[1] - start_point[1])/(abs(end_point[0] - start_point[0]))
        theta = math.atan(slope)
        for t in range(int((distance-carryover)/travel_speed) + 1):
            x_coord = math.cos(theta) * distance_covered * moving_horizontal + start_point[0]
            y_coord = math.sin(theta) * distance_covered + start_point[1]
            # display_point(x_coord, y_coord)
            distance_covered += travel_speed
    return distance % travel_speed

def path(end_point, carryover=0):
    # calculate the distance between the start and end points
    start_point = [0,0]
    if(end_point == [0,0]):
        return
    angle = math.atan2(end_point[1], end_point[0])
    distance = math.sqrt(math.pow(end_point[1] - start_point[1], 2) + math.pow(end_point[0] - start_point[0], 2))
    distance_covered = carryover
    t = distance / travel_speed
    # determines if the lines grows in the positive or negative y direction
    forward_speed = np.sin(angle) * distance / t
    print(forward_speed)
    horizontal_speed = np.cos(angle) * distance / t
    print(horizontal_speed)
    drive.fl.move(forward_speed + horizontal_speed)
    drive.fr.move(forward_speed - horizontal_speed)
    drive.rl.move(forward_speed - horizontal_speed)
    drive.rr.move(forward_speed + horizontal_speed)
    time.sleep(t/100)

def semi_circle(p1, p2, carryover=0):    # draws a counter-clockwise half circle
    diameter = distance(p1, p2)
    radius = diameter / 2
    center = midpoint(p2, p1)
    vector = [p1[0] - center[0], p1[1] - center[1]]
    initial_angle = math.atan2(vector[1], vector[0])
    carryover_angle = carryover / radius
    arc_measure = travel_speed / radius    # in radians
    for t in range(int(np.pi / arc_measure)):
        x_coord = np.cos(carryover_angle + initial_angle + (t + 1) * arc_measure) * radius + center[0]
        y_coord = np.sin(carryover_angle + initial_angle + (t + 1) * arc_measure) * radius + center[1]
        # display_point(x_coord, y_coord)
        Path_Points.add([x_coord, y_coord])
    return radius * np.pi % travel_speed


def draw_circle():
    center = point1
    prev_point = point2
    radius = distance(prev_point, center)
    vector = [prev_point[0] - center[0], prev_point[1] - center[1]]
    initial_angle = np.arctan2(vector[1], vector[0])
    print(initial_angle*180/np.pi)
    arc_measure = travel_speed / 100 / radius    # in radians
    # display_point(prev_point[0], prev_point[1])
    for t in range(int(2 * np.pi / arc_measure)):
        x_coord = np.cos(initial_angle + (t + 1) * arc_measure) * radius + center[0]
        y_coord = np.sin(initial_angle + (t + 1) * arc_measure) * radius + center[1]
        next_point = [x_coord, y_coord]
        # display_point(x_coord, y_coord)
        Path_Points.append([x_coord * speed_mult, y_coord * speed_mult])
        prev_point = next_point


def draw_quad():
    c = 0
    c = path(point1, point2, carryover=c)
    c = path(point2, point3, carryover=c)
    c = path(point3, point4, carryover=c)
    c = path(point4, point1, carryover=c)


def draw_loop():
    s.enter(0, 1, path(point1, point2))
    s.enter(0, 1, semi_circle(point2, point3))
    s.enter(0, 1, path(point3, point4))
    s.enter(0, 1, semi_circle(point4, point1))


def main():
    draw_circle()
    print(Path_Points)
    for x in Path_Points:
        path(x)
    drive.coastAll(1)

if __name__ == '__main__':
    try:
      main()
    except KeyboardInterrupt:
      drive.stop_car() #stop movement
      drive.destroy()  #clean up GPIO
      print("\nStopped and cleanup done")    

