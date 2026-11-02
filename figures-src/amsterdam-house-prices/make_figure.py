"""Real Amsterdam house prices, 1650 = 100, 1650-2025, house style (as the Norway chart).

Reads data/amsterdam_house_prices.csv (made by build_data.py) and writes amsterdam-house-prices.svg.
Optional dashed log-linear trend lines (TRENDS), currently none.

Usage:  python3 make_figure.py <outdir>
"""
import csv
import math
import sys
from pathlib import Path

HERE = Path(__file__).parent

# house style (see figure-style.md)
FONT = "'Source Sans Pro', Helvetica, sans-serif"
INK = "#000000"        # axes, frame, tick labels
BASE = "#3d4d99"       # indigo: the series
CBS_COL = "#1b8579"    # teal: the CBS extension after the splice
HIGHLIGHT = "#d0205e"  # crimson: the trends
GRID = "#c8c8c8"       # light grey, dotted

W, H = 1150, 560
L, R, T, B = 120, 30, 30, 70          # plot-area margins
X0, X1 = 1650, 2030
Y0, Y1, YSTEP = 0, 300, 50
TRENDS = []   # no trend lines; e.g. [(1650, 1995), (1995, 2025)] to add them back


def load():
    with open(HERE / "data" / "amsterdam_house_prices.csv") as f:
        return [(int(r["year"]), float(r["real_house_price_1650eq100"]), r["source"])
                for r in csv.DictReader(f)]


def sx(year):
    return L + (year - X0) / (X1 - X0) * (W - L - R)


def sy(v):
    return H - B - (v - Y0) / (Y1 - Y0) * (H - T - B)


def loglinear(pts, a, b):
    """fit log(v) = c + g*year on a <= year <= b; return (c, g)"""
    xy = [(y, math.log(v)) for y, v in pts if a <= y <= b]
    mx = sum(x for x, _ in xy) / len(xy)
    my = sum(y for _, y in xy) / len(xy)
    g = sum((x - mx) * (y - my) for x, y in xy) / sum((x - mx) ** 2 for x, _ in xy)
    return my - g * mx, g


def text(x, y, s, anchor="middle", size=26, color=INK, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}"{extra}>{s}</text>')


def build(data):
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" font-family="{FONT}">',
           f'<title>Real Amsterdam house prices, {data[0][0]}–{data[-1][0]} (1650 = 100)</title>',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
           f'<clipPath id="plot"><rect x="{L}" y="{T}" width="{W - L - R}" height="{H - T - B}"/></clipPath>']

    # dotted light-grey gridlines + y tick labels
    for v in range(Y0, Y1 + 1, YSTEP):
        if Y0 < v < Y1:
            out.append(f'<line x1="{L}" y1="{sy(v):.1f}" x2="{W - R}" y2="{sy(v):.1f}" stroke="{GRID}" '
                       f'stroke-width="2" stroke-dasharray="0 7" stroke-linecap="round"/>')
        out.append(text(L - 14, sy(v) + 9, f"{v:,}", "end"))
    for yr in range(1650, X1 + 1, 50):
        if X0 < yr < X1:
            out.append(f'<line x1="{sx(yr):.1f}" y1="{T}" x2="{sx(yr):.1f}" y2="{H - B}" stroke="{GRID}" '
                       f'stroke-width="2" stroke-dasharray="0 7" stroke-linecap="round"/>')
        out.append(f'<line x1="{sx(yr):.1f}" y1="{H - B}" x2="{sx(yr):.1f}" y2="{H - B + 10}" '
                   f'stroke="{INK}" stroke-width="2.5"/>')
        out.append(text(sx(yr), H - B + 40, str(yr)))
    cy = (T + H - B) / 2
    out.append(text(34, cy, "Real house prices (1650 = 100)",
                    extra=f' transform="rotate(-90 34 {cy:.1f})"'))

    # the series: Herengracht (AEL 2013) in indigo, CBS extension in teal, joined at the splice year
    ael = [(y, v) for y, v, src in data if src == "AEL2013"]
    cbs = [ael[-1]] + [(y, v) for y, v, src in data if src == "CBS"]
    for part, col in [(ael, BASE), (cbs, CBS_COL)]:
        pts = " ".join(f"{sx(y):.1f},{sy(v):.1f}" for y, v in part)
        out.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="4" '
                   f'stroke-linejoin="round" stroke-linecap="round" clip-path="url(#plot)"/>')

    # trend lines (dashed, crimson) with growth-rate labels
    series = [(y, v) for y, v, _ in data]
    for a, b in TRENDS:
        c, g = loglinear(series, a, b)
        pts = " ".join(f"{sx(y):.1f},{sy(math.exp(c + g * y)):.1f}" for y in range(a, b + 1))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{HIGHLIGHT}" stroke-width="3.5" '
                   f'stroke-dasharray="14 9" clip-path="url(#plot)"/>')
        rate = 100 * (math.exp(g) - 1)
        label = f"{a}–{b}: {'+' if rate >= 0 else '−'}{abs(rate):.1f}% p.a."
        if a == 1650:   # in the empty band above the flat 1800-1860 stretch
            out.append(text(sx(1842), sy(150), label, color=HIGHLIGHT, extra=' font-weight="bold"'))
        else:           # left of the recent trend
            out.append(text(sx(1990), sy(240), label, "end", color=HIGHLIGHT, extra=' font-weight="bold"'))
        print(f"trend {a}-{b}: {rate:.2f}% p.a.")

    # legend, top left inside the frame
    for i, (label, col) in enumerate([(f"Herengracht, {ael[0][0]}–{ael[-1][0]}", BASE),
                                      (f"CBS Amsterdam, {cbs[1][0]}–{cbs[-1][0]}", CBS_COL)]):
        y = T + 36 + 34 * i
        out.append(f'<line x1="{L + 20}" y1="{y - 8}" x2="{L + 60}" y2="{y - 8}" stroke="{col}" '
                   f'stroke-width="5" stroke-linecap="round"/>')
        out.append(text(L + 72, y, label, "start", color=col, extra=' font-weight="bold"'))

    # box around the plot area
    out.append(f'<rect x="{L}" y="{T}" width="{W - L - R}" height="{H - T - B}" fill="none" '
               f'stroke="{INK}" stroke-width="2.5"/>')
    out.append('</svg>')
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    outdir = Path(sys.argv[1])
    (outdir / "amsterdam-house-prices.svg").write_text(build(load()))
    print("wrote", outdir / "amsterdam-house-prices.svg")
