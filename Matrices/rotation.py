import numpy as np


def x(points, angle):
    a = np.deg2rad(angle)
    matrix = ([1, 0, 0], [0, np.cos(a), -1 * np.sin(a)], [0, np.sin(a), np.cos(a)])
    return np.matmul(matrix, points)


def y(points, angle):
    a = np.deg2rad(angle)
    matrix = ([np.cos(a), 0, np.sin(a)], [0, 1, 0], [-1 * np.sin(a), 0, np.cos(a)])
    return np.matmul(matrix, points)


def z(points, angle):
    a = np.deg2rad(angle)
    matrix = ([np.cos(a), -1 * np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1])
    return np.matmul(matrix, points)