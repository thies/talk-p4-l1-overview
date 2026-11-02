"""Norwegian real house prices, 1819 = 100, with two log-linear trend lines.

Reads data/norway_house_prices.csv (made by build_data.py) and writes norway.svg.
Trends are least-squares fits of log(index) on year, i.e. constant real growth rates,
labelled with that rate per year.

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
HIGHLIGHT = "#d0205e"  # crimson: the trends
GRID = "#c8c8c8"       # light grey, dotted

W, H = 1150, 560
L, R, T, B = 120, 30, 30, 70          # plot-area margins
X0, X1 = 1819, 2026
Y0, Y1, YSTEP = 0, 3000, 500
TRENDS = [(1875, 2000), (1995, 2023)]  # fit windows (inclusive)


def load():
    with open(HERE / "data" / "norway_house_prices.csv") as f:
        return [(int(r["year"]), float(r["hpi_real_1819eq100"])) for r in csv.DictReader(f)]


def sx(year):
    return L + (year - X0) / (X1 - X0) * (W - L - R)


def sy(v):
    return H - B - (v - Y0) / (Y1 - Y0) * (H - T - B)


def text(x, y, s, anchor="middle", size=26, color=INK, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}"{extra}>{s}</text>')


def loglinear(data, a, b):
    """fit log(v) = c + g*year on a <= year <= b; return (c, g)"""
    pts = [(y, math.log(v)) for y, v in data if a <= y <= b]
    n = len(pts)
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    g = sum((x - mx) * (y - my) for x, y in pts) / sum((x - mx) ** 2 for x, _ in pts)
    return my - g * mx, g


def build(data):
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" font-family="{FONT}">',
           f'<title>Norwegian real house prices, {data[0][0]}–{data[-1][0]} (1819 = 100)</title>',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
           f'<clipPath id="plot"><rect x="{L}" y="{T}" width="{W - L - R}" height="{H - T - B}"/></clipPath>']

    # dotted light-grey gridlines + y tick labels
    for v in range(Y0, Y1 + 1, YSTEP):
        if Y0 < v < Y1:
            out.append(f'<line x1="{L}" y1="{sy(v):.1f}" x2="{W - R}" y2="{sy(v):.1f}" stroke="{GRID}" '
                       f'stroke-width="2" stroke-dasharray="0 7" stroke-linecap="round"/>')
        out.append(text(L - 14, sy(v) + 9, f"{v:,}", "end"))
    for yr in range(1825, X1 + 1, 25):
        if X0 < yr < X1:
            out.append(f'<line x1="{sx(yr):.1f}" y1="{T}" x2="{sx(yr):.1f}" y2="{H - B}" stroke="{GRID}" '
                       f'stroke-width="2" stroke-dasharray="0 7" stroke-linecap="round"/>')
        out.append(f'<line x1="{sx(yr):.1f}" y1="{H - B}" x2="{sx(yr):.1f}" y2="{H - B + 10}" '
                   f'stroke="{INK}" stroke-width="2.5"/>')
        out.append(text(sx(yr), H - B + 40, str(yr)))
    cy = (T + H - B) / 2
    out.append(text(34, cy, "Real house prices (1819 = 100)",
                    extra=f' transform="rotate(-90 34 {cy:.1f})"'))

    # trend lines (dashed, crimson) with growth-rate labels
    for a, b in TRENDS:
        c, g = loglinear(data, a, b)
        pts = " ".join(f"{sx(y):.1f},{sy(math.exp(c + g * y)):.1f}" for y in range(a, b + 1))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{HIGHLIGHT}" stroke-width="3.5" '
                   f'stroke-dasharray="14 9" clip-path="url(#plot)"/>')
        rate = 100 * (math.exp(g) - 1)
        last = data[-1][0] if b > data[-1][0] else b
        label = f"{a}–{last}: {rate:+.1f}% p.a.".replace("-", "−", 1) if rate < 0 else \
            f"{a}–{last}: +{rate:.1f}% p.a."
        if b == 2000:   # in the empty space under the long trend
            out.append(text(sx(1950), sy(140), label, color=HIGHLIGHT, extra=' font-weight="bold"'))
        else:           # left of the recent trend, near its top
            xm = 2012
            out.append(text(sx(xm) - 14, sy(math.exp(c + g * xm)) - 6, label, "end", color=HIGHLIGHT,
                            extra=' font-weight="bold"'))
        print(f"trend {a}-{b}: {rate:.2f}% p.a.")

    # the series
    pts = " ".join(f"{sx(y):.1f},{sy(v):.1f}" for y, v in data)
    out.append(f'<polyline points="{pts}" fill="none" stroke="{BASE}" stroke-width="4" '
               f'stroke-linejoin="round" stroke-linecap="round" clip-path="url(#plot)"/>')

    # box around the plot area
    out.append(f'<rect x="{L}" y="{T}" width="{W - L - R}" height="{H - T - B}" fill="none" '
               f'stroke="{INK}" stroke-width="2.5"/>')
    out.append('</svg>')
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    outdir = Path(sys.argv[1])
    (outdir / "norway.svg").write_text(build(load()))
    print("wrote", outdir / "norway.svg")
