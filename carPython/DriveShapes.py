import math
import time
import sched
import numpy as np
#import mecanum_py_by_wheel_encodeSpeed as drive
import original_mecanum as drive
from scipy import interpolate



s = sched.scheduler(time.time, time.sleep)
point1 = [0, 0]
point2 = [25, 25]
point3 = [50, 50]
point4 = [50, 0]
Path_Points = [[0, 0]]
IntervalTime = 0
travel_speed = 55
speed_mult = 1
base_speed = 0

robot_width = 1
robot_length = 1


def length(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1])


def dist(v, w):
    return math.sqrt(math.pow(v[1] - w[1], 2) + math.pow(v[0] - w[0], 2))


def midpoint(x1, x2):
    return [(x1[0] + x2[0]) / 2, (x1[1] + x2[1]) / 2]


def path(end_point):
    # calculate the distance between the start and end points
    start_point = [0, 0]
    if(end_point == [0, 0]):
        return
    angle = math.atan2(end_point[1], end_point[0])
    distance = dist(start_point, end_point)
    t = distance / travel_speed
    # determines if the lines grows in the positive or negative y direction
    forward_speed = np.sin(angle) * travel_speed + base_speed
    horizontal_speed = np.cos(angle) * travel_speed + base_speed
    rotational_speed = 0
    ab = robot_length / 2 + robot_width / 2
    print("" + str(forward_speed) + "  " + str(horizontal_speed))
    drive.fl.move(forward_speed + horizontal_speed - rotational_speed * ab)
    drive.fr.move(forward_speed - horizontal_speed + rotational_speed * ab)
    drive.rl.move(forward_speed - horizontal_speed - rotational_speed * ab)
    drive.rr.move(forward_speed + horizontal_speed + rotational_speed * ab)
    time.sleep(t/100)


def semi_circle(p1, p2, carryover=0):
    diameter = dist(p1, p2)
    radius = diameter / 2
    center = midpoint(p2, p1)
    vector = [p1[0] - center[0], p1[1] - center[1]]
    initial_angle = math.atan2(vector[1], vector[0])
    carryover_angle = carryover / radius
    arc_measure = travel_speed / radius    # in radians
    for t in range(int(np.pi / arc_measure)):
        angle_change = carryover_angle + initial_angle + (t + 1) * arc_measure
        x_coord = np.cos(angle_change) * radius + center[0]
        y_coord = np.sin(angle_change) * radius + center[1]
        Path_Points.add([x_coord, y_coord])
    return radius * np.pi % travel_speed


def draw_circle():
    center = point1
    prev_point = point2
    radius = dist(prev_point, center)
    vector = [prev_point[0] - center[0], prev_point[1] - center[1]]
    initial_angle = np.arctan2(vector[1], vector[0])
    print(initial_angle*180/np.pi)
    arc_measure = travel_speed / 100 / radius    # in radians
    for t in range(int(2 * np.pi / arc_measure)):
        x_coord = np.cos(initial_angle + (t + 1) * arc_measure) * radius + center[0]
        y_coord = np.sin(initial_angle + (t + 1) * arc_measure) * radius + center[1]
        next_point = [x_coord, y_coord]
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

def draw_spline():
    sleep(1)

def main():
    draw_circle()
    print(Path_Points)
    for x in Path_Points:
        path(x)
    drive.stop_car()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        drive.stop_car() # stop movement
        drive.destroy()  # clean up GPIO
        print("\nStopped and cleanup done")