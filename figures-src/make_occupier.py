"""Occupier market: short-run vs long-run supply response to a demand shock.

  D  : R = 500 - S            initial demand
  D' : R = 700 - S            demand after a positive shock (shift right by 200)
  S  : R = 200 + 3 (S - 300)  short-run supply, steep (stock barely adjusts)
  S' : R = 200 + 0.4 (S - 300) long-run supply, flat (new construction)

Equilibria (model units = SVG pixels from the origin):
  E1 = D  & S  = (300, 200)   -> S1, P1
  E2 = D' & S  = (350, 350)   -> S2, P2  rents jump in the short run
  E3 = D' & S' = (442.9, 257.1) -> S3, P3  supply catches up, rents ease
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from make_4qm import FONT, INK, BASE, HIGHLIGHT, COL  # noqa: E402  shared house style

W, H = 1180, 620
OX, OY = 110, 540          # origin in SVG pixels

D = lambda s: 500 - s
D2 = lambda s: 700 - s
SR = lambda s: 200 + 3 * (s - 300)
LR = lambda s: 200 + 0.4 * (s - 300)
E = {1: (300, 200), 2: (350, 350), 3: (620 / 1.4, 700 - 620 / 1.4)}


def pt(x, y):
    return OX + x, OY - y


def line(p, q, color, width=6, dash=None, marker=False):
    (x1, y1), (x2, y2) = pt(*p), pt(*q)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = ' marker-end="url(#arr)"' if marker else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" '
            f'stroke-width="{width}" stroke-linecap="round"{d}{m}/>')


def text(x, y, s, color=INK, anchor="middle", size=32):
    sx, sy = pt(x, y)
    return (f'<text x="{sx:.1f}" y="{sy:.1f}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}" font-weight="bold">{s}</text>')


def subscripted(x, y, s, sub, color=INK):
    """letter + subscript as two text elements joined at x (renderer-independent)"""
    return [text(x, y, s, color, "end"), text(x + 1, y - 9, str(sub), color, "start", 22)]


def build():
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" font-family="{FONT}">',
           '<title>Occupier market: short- and long-run supply adjustment</title>',
           '<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" '
           'markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
           f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>']

    # guides from each equilibrium to the axes (thin, solid, sky blue)
    for s, r in E.values():
        out.append(line((0, r), (s, r), COL["eq"], 2.5))
        out.append(line((s, 0), (s, r), COL["eq"], 2.5))

    # axes
    out.append(line((0, 0), (0, 480), INK, 4, marker=True))
    out.append(line((0, 0), (820, 0), INK, 4, marker=True))
    out.append(text(0, 495, "Rent"))
    out.append(text(832, -10, "Stock (m²)", anchor="start"))

    # curves: demand in the base colour, supply in red; long-run supply dashed
    out.append(line((120, D(120)), (480, D(480)), BASE))
    out.append(line((300, D2(300)), (680, D2(680)), BASE))
    out.append(line((240, SR(240)), (370, SR(370)), HIGHLIGHT))
    out.append(line((120, LR(120)), (760, LR(760)), HIGHLIGHT, dash="18 14"))
    out += [text(490, D(480) - 10, "D", BASE, "start"),
            text(690, D2(680) - 10, "D′", BASE, "start"),
            text(378, SR(370) + 8, "S", HIGHLIGHT, "start"),
            text(772, LR(760) - 10, "S′", HIGHLIGHT, "start")]

    # equilibrium labels on the axes
    for i, (s, r) in E.items():
        out += subscripted(-34, r - 10, "P", i)
        out += subscripted(s + 4, -42, "S", i)
    out.append('</svg>')
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    outdir = Path(sys.argv[1])
    (outdir / "occupier.svg").write_text(build())
    print("wrote", outdir / "occupier.svg")
