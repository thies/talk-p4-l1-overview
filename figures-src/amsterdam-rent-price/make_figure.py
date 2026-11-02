"""Amsterdam rent/price ratio, 1650-2009, house style (same look as the Norway chart).

Data: data/amsterdam_rent_price.csv, made by build_data.py (Ambrose, Eichholtz &
Lindenthal 2013; ratio scaled to 4.5% in 2002, see there).
The dashed line is the 1650-2009 mean.

Usage:  python3 make_figure.py <outdir>
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).parent

# house style (see figure-style.md)
FONT = "'Source Sans Pro', Helvetica, sans-serif"
INK = "#000000"
BASE = "#3d4d99"
HIGHLIGHT = "#d0205e"
GRID = "#c8c8c8"

W, H = 1150, 560
L, R, T, B = 100, 110, 30, 70      # wide right margin holds the mean label
X0, X1 = 1650, 2010
Y0, Y1, YSTEP = 0, 15, 3                 # percent


def load():
    with open(HERE / "data" / "amsterdam_rent_price.csv") as f:
        return [(int(r["year"]), float(r["rent_price_pct"])) for r in csv.DictReader(f)]


def sx(year):
    return L + (year - X0) / (X1 - X0) * (W - L - R)


def sy(v):
    return H - B - (v - Y0) / (Y1 - Y0) * (H - T - B)


def text(x, y, s, anchor="middle", size=26, color=INK, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}"{extra}>{s}</text>')


def dotted(x1, y1, x2, y2):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GRID}" '
            f'stroke-width="2" stroke-dasharray="0 7" stroke-linecap="round"/>')


def build(data):
    mean = sum(v for _, v in data) / len(data)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" font-family="{FONT}">',
           f'<title>Amsterdam rent/price ratio, {data[0][0]}–{data[-1][0]}</title>',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
           f'<clipPath id="plot"><rect x="{L}" y="{T}" width="{W - L - R}" height="{H - T - B}"/></clipPath>']

    for v in range(Y0, Y1 + 1, YSTEP):
        if Y0 < v < Y1:
            out.append(dotted(L, sy(v), W - R, sy(v)))
        out.append(text(L - 14, sy(v) + 9, f"{v}%", "end"))
    for yr in range(1650, X1 + 1, 50):
        if X0 < yr < X1:
            out.append(dotted(sx(yr), T, sx(yr), H - B))
        out.append(f'<line x1="{sx(yr):.1f}" y1="{H - B}" x2="{sx(yr):.1f}" y2="{H - B + 10}" '
                   f'stroke="{INK}" stroke-width="2.5"/>')
        out.append(text(sx(yr), H - B + 40, str(yr)))
    cy = (T + H - B) / 2
    out.append(text(30, cy, "Rent / price", extra=f' transform="rotate(-90 30 {cy:.1f})"'))

    # long-run mean (dashed, crimson) with label
    out.append(f'<line x1="{L}" y1="{sy(mean):.1f}" x2="{W - R}" y2="{sy(mean):.1f}" '
               f'stroke="{HIGHLIGHT}" stroke-width="3" stroke-dasharray="14 9"/>')
    # label outside the plot area, at the right end of the line
    out.append(text(W - R + 12, sy(mean) - 6, "Mean", "start", color=HIGHLIGHT, extra=' font-weight="bold"'))
    out.append(text(W - R + 12, sy(mean) + 24, f"~{mean:.0f}%", "start", color=HIGHLIGHT, extra=' font-weight="bold"'))

    pts = " ".join(f"{sx(y):.1f},{sy(v):.1f}" for y, v in data)
    out.append(f'<polyline points="{pts}" fill="none" stroke="{BASE}" stroke-width="3" '
               f'stroke-linejoin="round" stroke-linecap="round" clip-path="url(#plot)"/>')

    out.append(f'<rect x="{L}" y="{T}" width="{W - L - R}" height="{H - T - B}" fill="none" '
               f'stroke="{INK}" stroke-width="2.5"/>')
    out.append('</svg>')
    print(f"{data[0][0]}-{data[-1][0]}, mean {mean:.2f}%")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    outdir = Path(sys.argv[1])
    (outdir / "rent-price-amsterdam.svg").write_text(build(load()))
    print("wrote", outdir / "rent-price-amsterdam.svg")
