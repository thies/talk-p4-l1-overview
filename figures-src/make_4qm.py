"""Generate the DiPasquale-Wheaton four-quadrant diagrams as vector SVGs.

Geometry is built in model units around the origin so the dashed equilibrium
rectangle closes exactly on all four curves:
  occupier (NE):   demand  R = R* - (S - S*)          through (S*, R*)
  investment (NW): cap rate R = k P,  k = R*/P*
  development (SW): C = (P - P_min) / m, zero below P_min
  adjustment (SE): C = delta S,       delta = C*/S*
"""
import sys
from pathlib import Path

W, H = 1150, 690
OX, OY = 550, 330          # origin in SVG pixels
S_, R_, P_, C_ = 300, 220, 280, 200   # equilibrium (pixels from origin)
P_MIN = 120

# house palette, shared with the papers' figures:
# "#bac33e","#1b8579","#49c4ea","#3d4d99","#803c8e","#d0205e","#ff862c","#ffd44a"
PALETTE = ["#bac33e", "#1b8579", "#49c4ea", "#3d4d99", "#803c8e", "#d0205e", "#ff862c", "#ffd44a"]
FONT = "'Source Sans Pro', Helvetica, sans-serif"
INK = "#000000"            # axes and axis labels
# all markets share one colour; only the market under discussion is drawn in red
BASE, HIGHLIGHT = "#3d4d99", "#d0205e"
COL = {"eq": "#49c4ea", "axis": INK}
LABEL = {"occ": ("Occupier", "Market"), "inv": ("Investment", "Market"),
         "dev": ("Development", "Market"), "adj": ("Property Market", "Stock Adjustment")}


def pt(x, y):
    """model coords (x right, y up) -> svg coords"""
    return OX + x, OY - y


def line(p, q, color, width=6, dash=None):
    (x1, y1), (x2, y2) = pt(*p), pt(*q)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"{d}/>')


def text(x, y, s, size=32, color=INK, anchor="middle", italic=False):
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}" font-weight="bold"{st}>{s}</text>')


def build(highlight=None, base=BASE):
    k = R_ / P_
    m = (P_ - P_MIN) / C_
    delta = C_ / S_
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" font-family="{FONT}">',
           f'<title>Four-quadrant model (DiPasquale &amp; Wheaton)</title>',
           '<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" '
           'markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
           f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>']

    # quadrant highlight: tint the whole quadrant background, bounded by the axes (no outline)
    quads = {"inv": (0, 0, OX, OY), "occ": (OX, 0, W - OX, OY),
             "dev": (0, OY, OX, H - OY), "adj": (OX, OY, W - OX, H - OY)}
    if highlight:
        x, y, w, h = quads[highlight]
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                   f'fill="{HIGHLIGHT}" fill-opacity="0.08"/>')
    col = {q: HIGHLIGHT if q == highlight else base for q in LABEL}

    # axes, arrows pointing in each quadrant's positive direction
    for (x2, y2) in [(0, 292), (-422, 0), (422, 0), (0, -300)]:
        out.append(line((0, 0), (x2, y2), COL["axis"], 4).replace(
            '/>', ' marker-end="url(#arr)"/>'))
    out += [text(OX, 28, "Rent"),
            text(OX - 432, OY + 10, "Price", anchor="end"),
            text(OX + 432, OY + 10, "Stock (m²)", anchor="start"),
            text(OX, H - 14, "Construction (m²)")]

    # equilibrium rectangle
    corners = [(-P_, R_), (S_, R_), (S_, -C_), (-P_, -C_), (-P_, R_)]
    for a, b in zip(corners, corners[1:]):
        out.append(line(a, b, COL["eq"], 2.5))

    # curves
    out.append(line((240, R_ + 60), (440, R_ - 140), col["occ"]))            # demand, slope -1
    out.append(line((0, 0), (-360, 360 * k), col["inv"]))                    # R = kP
    out.append(line((-P_MIN, 0), (-(P_MIN + 300 * m), -300), col["dev"]))    # C = (P-Pmin)/m
    out.append(line((0, 0), (420, -420 * delta), col["adj"]))               # C = delta S

    # quadrant labels, in their curve's colour
    for q, (x, y) in {"inv": (360, 66), "occ": (1040, 112),
                      "dev": (150, 432), "adj": (1000, 470)}.items():
        a, b = LABEL[q]
        out += [text(x, y, a, 32, col[q]),
                text(x, y + 36, b, 32, col[q])]
    out.append('</svg>')
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    outdir = Path(sys.argv[1])
    for name, hl, base in [("4qm", None, BASE),
                           ("4qm-red", None, HIGHLIGHT),   # L1 "A Conceptual Framework" slide
                           ("space-market", "occ", BASE), ("investment-market", "inv", BASE),
                           ("development-market", "dev", BASE), ("adjustment-market", "adj", BASE)]:
        (outdir / f"{name}.svg").write_text(build(hl, base))
        print("wrote", outdir / f"{name}.svg")
