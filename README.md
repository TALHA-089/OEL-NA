# Lab 7 - Numerical Interpolation (Advanced Applications)

Reconstructs a symmetrical face outline from half of its data using numerical interpolation.

## Setup

```
pip install -r requirements.txt
```

## Run

```
python main.py
```

Opens the four figure windows and prints the tables in the terminal. Figures are also saved in the `outputs` folder.

Useful options:

```
python main.py --method Lagrange
python main.py --method Newton
python main.py --method "Cubic Spline"
python main.py --no-show
```

## Files

| File | Purpose |
|------|---------|
| `data.py` | Given lab data and sampling settings |
| `interpolation.py` | Lagrange, Newton divided difference and natural cubic spline, written from scratch |
| `outline.py` | Builds the left half, mirrors it to the right half, joins both into one outline |
| `plotting.py` | All figures |
| `report.py` | Terminal tables and verification checks |
| `main.py` | Entry point |

## Outputs

| File | Content |
|------|---------|
| `outputs/01_given_points.png` | The six given points |
| `outputs/02_method_comparison.png` | Left half from all three methods |
| `outputs/03_full_face_outline.png` | Complete face outline |
| `outputs/04_all_methods_gallery.png` | Complete face for each method side by side |
| `outputs/outline_points.csv` | Reconstructed left and right coordinates |
