"""Durable housing: kinked supply (after Glaeser & Gyourko, 2005), house style.

Same canvas, axes and helpers as the occupier-market figure (make_occupier.py).

  S  : vertical at S0 up to C (the stock cannot shrink), flat at C beyond (new building)
  D  : R = 640 - S   through the kink (S0, C) = (380, 260)
  D' : R = 840 - S   boom:  meets the flat part at S1 = 580, rent stays at C
  D'': R = 480 - S   bust:  meets the vertical part at rent 100, well below C
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from make_4qm import FONT, INK, BASE, HIGHLIGHT, COL  # noqa: E402
from make_occupier import W, H, line, text, subscripted  # noqa: E402

S0, C, S1, R_BUST = 380, 260, 580, 100
XMAX = 880                 # end of the stock axis
D = lambda s: 640 - s
D_BOOM = lambda s: 840 - s
D_BUST = lambda s: 480 - s


def build():
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" font-family="{FONT}">',
           '<title>Durable housing: kinked supply (after Glaeser &amp; Gyourko, 2005)</title>',
           '<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" '
           'markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
           f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>']

    # guides (thin, solid, sky blue)
    out.append(line((0, C), (S0, C), COL["eq"], 2.5))           # construction cost level
    out.append(line((0, R_BUST), (S0, R_BUST), COL["eq"], 2.5))  # bust rent
    out.append(line((S1, 0), (S1, C), COL["eq"], 2.5))           # boom stock

    # axes, labelled as on the occupier-market slide
    out.append(line((0, 0), (0, 480), INK, 4, marker=True))
    out.append(line((0, 0), (XMAX, 0), INK, 4, marker=True))
    out.append(text(0, 495, "Rent"))
    out.append(text(XMAX + 12, -10, "Stock (m²)", anchor="start"))

    # demand curves (base colour) and the kinked supply curve (red)
    out.append(line((200, D(200)), (600, D(600)), BASE))
    out.append(line((410, D_BOOM(410)), (800, D_BOOM(800)), BASE))
    out.append(line((120, D_BUST(120)), (440, D_BUST(440)), BASE))
    out.append(f'<polyline points="{110 + S0},540 {110 + S0},{540 - C} {110 + 840},{540 - C}" '
               f'fill="none" stroke="{HIGHLIGHT}" stroke-width="6" stroke-linejoin="round" '
               f'stroke-linecap="round"/>')
    out += [text(610, D(600) - 10, "D", BASE, "start"),
            text(810, D_BOOM(800) - 10, "D′", BASE, "start"),
            text(450, D_BUST(440) - 10, "D″", BASE, "start"),
            text(852, C - 10, "S", HIGHLIGHT, "start")]

    # axis labels
    out.append(text(-18, C - 10, "C", anchor="end"))
    out += subscripted(S0 + 4, -42, "S", 0)
    out += subscripted(S1 + 4, -42, "S", 1)

    out.append('</svg>')
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    outdir = Path(sys.argv[1])
    (outdir / "kinked_supply.svg").write_text(build())
    print("wrote", outdir / "kinked_supply.svg")
