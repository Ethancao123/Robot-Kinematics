import numpy as np


def x(points, angle):
    a = np.deg2rad(angle)
    matrix = ([1, 0, 0], [0, np.cos(a), -1 * np.sin(a)], [0, np.sin(a), np.cos(a)])
    return np.matmul(matrix, points)


def y(points, angle):
    a = np.deg2rad(angle)
    matrix = ([cos(a), 0, sin(a)], [0, 1, 0], [-1 * sin(a), 0, cos(a)])
    return np.matmul(matrix, points)


def z(points, angle):
    a = np.deg2rad(angle)
    matrix = ([cos(a), -1 * sin(a), 0], [sin(a), cos(a), 0], [0, 0, 1])
    return np.matmul(matrix, points)

def rotate(points, anglex, angley, anglez):
    g = np.deg2rad(anglex)
    b = np.deg2rad(angley)
    a = np.deg2rad(anglez)
    matrix = ([cos(a) * cos(b), cos(a) * sin(b) * sin(g) - sin(a) * cos(g), cos(a) * sin(b) * cos(g) + sin(a) * sin(g)],
              [sin(a) * cos(b), sin(a) * sin(b) * sin(g) + cos(a) * cos(g), sin(a) * sin(b) * cos(g) - cos(a) * sin(g)], 
              [-sin(b), cos(b) * sin(g), cos(b) * cos(g)])
    print(matrix)
    return np.matmul(matrix, points)

def sin(a):
    return np.sin(a)

def cos(a):
    return np.cos(a)