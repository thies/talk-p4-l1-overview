# Figure style

House standards for all figures, charts and diagrams in the talks and papers.

## Colours

```r
# a few standardisations for all figures in our paper
colours <- c("#bac33e","#1b8579","#49c4ea","#3d4d99","#803c8e","#d0205e","#ff862c","#ffd44a")
```

| # | Hex | Colour | Good for |
|---|---|---|---|
| 1 | `#bac33e` | lime | fills, areas; not text |
| 2 | `#1b8579` | teal | lines, text |
| 3 | `#49c4ea` | sky blue | lines, dashed guides; weak as text |
| 4 | `#3d4d99` | indigo | lines, text |
| 5 | `#803c8e` | purple | lines, text |
| 6 | `#d0205e` | crimson | lines, text, emphasis |
| 7 | `#ff862c` | orange | highlights, outlines; not text |
| 8 | `#ffd44a` | yellow | highlight fills (e.g. 30% opacity); not text |

- Lime, orange and yellow are too light for text on white. Use them for fills, highlights and guides.
- Use black (`#000000`) for axes and axis labels, and near-black (`#222222`) for body text.
- Draw guide lines, such as equilibrium boxes, solid and thin (about 2.5 px) in sky blue (`#49c4ea`).
- Give a label the same colour as the series it names.
- Set labels upright, not in italics.

### Diagrams that build across slides

Don't give each element its own colour. Draw everything in one base colour, indigo `#3d4d99`. Draw only the element under discussion in red, crimson `#d0205e`: its line, its label and a light red tint (8%) over its area's background, bounded by the axes. Don't draw an outline box. The quadrant-model figures follow this rule.

## Font

```
Source Sans Pro, Helvetica, sans-serif
```

Source Sans Pro is installed locally (`~/.fonts`). SVGs shown via `<img>` use it on this machine and fall back to Helvetica elsewhere.

## Snippets

**R / ggplot2**

```r
scale_colour_manual(values = colours) +
theme(text = element_text(family = "Source Sans Pro"))
```

**Python / matplotlib**

```python
import matplotlib.pyplot as plt
from cycler import cycler
plt.rcParams["axes.prop_cycle"] = cycler(color=["#bac33e","#1b8579","#49c4ea","#3d4d99",
                                                "#803c8e","#d0205e","#ff862c","#ffd44a"])
plt.rcParams["font.family"] = ["Source Sans Pro", "Helvetica", "sans-serif"]
```

**SVG / CSS**

```html
<svg ... font-family="'Source Sans Pro', Helvetica, sans-serif">
```

## Example

`figures-src/make_4qm.py` generates the quadrant-model figures in this style.
