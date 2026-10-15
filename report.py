import numpy as np


def print_known_data(y_known, x_known):
    print("Known half-outline data")
    print(f"{'y':>8}{'x':>8}")
    for y, x in zip(y_known, x_known):
        print(f"{y:8.1f}{x:8.1f}")
    print()


def print_intermediate_values(y_known, x_known, methods, y_samples):
    names = list(methods)
    header = f"{'y':>8}" + "".join(f"{name:>16}" for name in names)
    columns = [methods[name](y_known, x_known, y_samples) for name in names]
    print("Interpolated x at intermediate y values")
    print(header)
    print("-" * len(header))
    for row, y in enumerate(y_samples):
        print(f"{y:8.2f}" + "".join(f"{column[row]:16.4f}" for column in columns))
    print()


def print_checks(y_known, x_known, methods, curves):
    print("Verification")
    for name, method in methods.items():
        node_error = np.max(np.abs(method(y_known, x_known, y_known) - x_known))
        minimum = np.min(curves[name][1])
        print(f"{name:<14} max error at given points: {node_error:.2e}   smallest x on curve: {minimum:.4f}")
    gap = np.max(np.abs(curves["Lagrange"][1] - curves["Newton"][1]))
    print(f"Lagrange vs Newton max difference: {gap:.2e}")
    print()


def print_symmetry_check(left_x, right_x):
    deviation = np.max(np.abs(left_x + right_x))
    print(f"Symmetry check (max |left_x + right_x|): {deviation:.2e}")
    print()
