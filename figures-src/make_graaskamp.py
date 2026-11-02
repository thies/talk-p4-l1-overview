"""Graaskamp spiral: development analysis cycles inward through four fields, house style.

The canvas is cropped tightly to the diagram (title, cross, labels); the slide places it
in the right-hand column of a two-column layout. No frame around the diagram.

The spiral is Archimedean: it starts outside, below the centre (market analysis) and
turns counter-clockwise through physical, political and financial analysis, narrowing
towards a decision at the centre.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from make_4qm import FONT, INK, HIGHLIGHT  # noqa: E402

W, H = 700, 775             # tight crop around title, cross and labels
CX, CY = 350, 425           # centre of the cross
ARM = 330                   # half-length of the cross lines
R_OUT, R_IN = 175, 50       # spiral start / end radius
TURNS = 2.15

LABELS = {  # (x, y, anchor, lines) -- one per quadrant
    "pol": (CX - 40, CY - 262, "end", ["Political and", "Legal Analysis"]),
    "phy": (CX + 40, CY - 262, "start", ["Physical and", "Design Analysis"]),
    "fin": (CX - 40, CY + 222, "end", ["Financial", "Analysis"]),
    "mkt": (CX + 40, CY + 222, "start", ["Market and", "Competitive", "Analysis"]),
}


def spiral_points(n=400):
    pts = []
    for i in range(n + 1):
        t = i / n
        theta = -math.pi / 2 + t * TURNS * 2 * math.pi       # start at the bottom, counter-clockwise
        r = R_OUT + (R_IN - R_OUT) * t
        pts.append((CX + r * math.cos(theta), CY - r * math.sin(theta)))
    return pts


def build():
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}" font-family="{FONT}">',
           '<title>The Graaskamp spiral</title>',
           '<defs><marker id="arr" viewBox="0 0 10 10" refX="7" refY="5" '
           'markerWidth="4" markerHeight="4" orient="auto">'
           f'<path d="M0,0 L10,5 L0,10 z" fill="{HIGHLIGHT}"/></marker></defs>']
    # transparent background: the slide's own white shows through

    # the cross
    out.append(f'<line x1="{CX - ARM}" y1="{CY}" x2="{CX + ARM}" y2="{CY}" stroke="{INK}" stroke-width="4"/>')
    out.append(f'<line x1="{CX}" y1="{CY - ARM}" x2="{CX}" y2="{CY + ARM}" stroke="{INK}" stroke-width="4"/>')

    # the spiral, ending in an arrowhead at the centre
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in spiral_points())
    out.append(f'<polyline points="{pts}" fill="none" stroke="{HIGHLIGHT}" stroke-width="7" '
               f'stroke-linecap="round" stroke-linejoin="round" marker-end="url(#arr)"/>')

    # figure title, centred over the cross
    out.append(f'<text x="{CX}" y="{CY - ARM - 40}" font-size="44" font-weight="bold" '
               f'fill="{INK}" text-anchor="middle">The “Graaskamp Spiral”</text>')

    # quadrant labels
    for x, y, anchor, lines in LABELS.values():
        for i, s in enumerate(lines):
            out.append(f'<text x="{x}" y="{y + 42 * i}" font-size="36" font-weight="bold" '
                       f'fill="{INK}" text-anchor="{anchor}">{s}</text>')
    out.append('</svg>')
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    outdir = Path(sys.argv[1])
    (outdir / "graaskamp-spiral.svg").write_text(build())
    print("wrote", outdir / "graaskamp-spiral.svg")
