import argparse
from pathlib import Path
import matplotlib.pyplot as plt

from data import POINTS_PER_UNIT, X_KNOWN, Y_KNOWN, Y_SAMPLES
from interpolation import METHODS
from outline import export_outline_csv, left_half, reconstruct_half_outline, right_half
from plotting import (
    plot_full_outline,
    plot_known_points,
    plot_method_comparison,
    plot_method_gallery,
    save_figure,
)
from report import print_checks, print_intermediate_values, print_known_data, print_symmetry_check

OUTPUT_DIR = Path(__file__).parent / "outputs"


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Face outline reconstruction using numerical interpolation")
    parser.add_argument(
        "--method",
        choices=list(METHODS),
        default="Cubic Spline",
        help="Method used for the main face outline figure",
    )
    parser.add_argument("--no-show", action="store_true",
                        help="Save figures without opening windows")
    return parser.parse_args()


def main():
    arguments = parse_arguments()

    curves = {
        name: reconstruct_half_outline(
            Y_KNOWN, X_KNOWN, method, POINTS_PER_UNIT)
        for name, method in METHODS.items()
    }
    y_dense, x_dense = curves[arguments.method]
    left_x, _ = left_half(y_dense, x_dense)
    right_x, _ = right_half(y_dense, x_dense)

    print_known_data(Y_KNOWN, X_KNOWN)
    print_intermediate_values(Y_KNOWN, X_KNOWN, METHODS, Y_SAMPLES)
    print_checks(Y_KNOWN, X_KNOWN, METHODS, curves)
    print_symmetry_check(left_x, right_x)

    figures = {
        "01_given_points.png": plot_known_points(Y_KNOWN, X_KNOWN),
        "02_method_comparison.png": plot_method_comparison(Y_KNOWN, X_KNOWN, curves),
        "03_full_face_outline.png": plot_full_outline(Y_KNOWN, X_KNOWN, y_dense, x_dense, arguments.method),
        "04_all_methods_gallery.png": plot_method_gallery(Y_KNOWN, X_KNOWN, curves),
    }
    for name, figure in figures.items():
        path = save_figure(figure, OUTPUT_DIR, name)
        print(f"Saved {path.name}")

    export_outline_csv(OUTPUT_DIR / "outline_points.csv", y_dense, x_dense)
    print("Saved outline_points.csv")

    if not arguments.no_show:
        plt.show()


if __name__ == "__main__":
    main()
