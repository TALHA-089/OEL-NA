import numpy as np


def lagrange_interpolate(nodes, values, query):
    nodes = np.asarray(nodes, dtype=float)
    values = np.asarray(values, dtype=float)
    query = np.asarray(query, dtype=float)
    result = np.zeros_like(query)
    for i in range(len(nodes)):
        basis = np.ones_like(query)
        for j in range(len(nodes)):
            if i != j:
                basis *= (query - nodes[j]) / (nodes[i] - nodes[j])
        result += values[i] * basis
    return result


def divided_difference_coefficients(nodes, values):
    nodes = np.asarray(nodes, dtype=float)
    coefficients = np.array(values, dtype=float)
    for order in range(1, len(nodes)):
        numerator = coefficients[order:] - coefficients[order - 1:-1]
        denominator = nodes[order:] - nodes[:-order]
        coefficients[order:] = numerator / denominator
    return coefficients


def newton_interpolate(nodes, values, query):
    nodes = np.asarray(nodes, dtype=float)
    query = np.asarray(query, dtype=float)
    coefficients = divided_difference_coefficients(nodes, values)
    result = np.full_like(query, coefficients[-1])
    for k in range(len(nodes) - 2, -1, -1):
        result = result * (query - nodes[k]) + coefficients[k]
    return result


def second_derivatives_natural(nodes, values):
    count = len(nodes)
    spacing = np.diff(nodes)
    slopes = np.diff(values) / spacing
    matrix = np.zeros((count, count))
    rhs = np.zeros(count)
    matrix[0, 0] = 1.0
    matrix[-1, -1] = 1.0
    for i in range(1, count - 1):
        matrix[i, i - 1] = spacing[i - 1]
        matrix[i, i] = 2.0 * (spacing[i - 1] + spacing[i])
        matrix[i, i + 1] = spacing[i]
        rhs[i] = 6.0 * (slopes[i] - slopes[i - 1])
    return np.linalg.solve(matrix, rhs)


def cubic_spline_interpolate(nodes, values, query):
    nodes = np.asarray(nodes, dtype=float)
    values = np.asarray(values, dtype=float)
    query = np.asarray(query, dtype=float)
    spacing = np.diff(nodes)
    curvature = second_derivatives_natural(nodes, values)
    segment = np.clip(np.searchsorted(nodes, query, side="right") - 1, 0, len(nodes) - 2)
    offset = query - nodes[segment]
    h = spacing[segment]
    a = values[segment]
    b = (values[segment + 1] - values[segment]) / h - h * (2.0 * curvature[segment] + curvature[segment + 1]) / 6.0
    c = curvature[segment] / 2.0
    d = (curvature[segment + 1] - curvature[segment]) / (6.0 * h)
    return a + b * offset + c * offset ** 2 + d * offset ** 3


METHODS = {
    "Lagrange": lagrange_interpolate,
    "Newton": newton_interpolate,
    "Cubic Spline": cubic_spline_interpolate,
}
