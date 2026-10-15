import numpy as np


def reconstruct_half_outline(y_known, x_known, method, points_per_unit):
    span = y_known[-1] - y_known[0]
    count = int(round(span * points_per_unit)) + 1
    y_dense = np.linspace(y_known[0], y_known[-1], count)
    x_dense = method(y_known, x_known, y_dense)
    return y_dense, x_dense


def left_half(y_dense, x_dense):
    return -x_dense, y_dense


def right_half(y_dense, x_dense):
    return x_dense.copy(), y_dense.copy()


def full_outline(y_dense, x_dense):
    left_x, left_y = left_half(y_dense, x_dense)
    right_x, right_y = right_half(y_dense, x_dense)
    outline_x = np.concatenate([left_x, right_x[::-1]])
    outline_y = np.concatenate([left_y, right_y[::-1]])
    return outline_x, outline_y


def export_outline_csv(path, y_dense, x_dense):
    left_x, left_y = left_half(y_dense, x_dense)
    right_x, right_y = right_half(y_dense, x_dense)
    table = np.column_stack([left_x, left_y, right_x, right_y])
    header = "left_x,left_y,right_x,right_y"
    np.savetxt(path, table, delimiter=",", header=header, comments="", fmt="%.6f")
