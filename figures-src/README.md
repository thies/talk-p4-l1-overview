# Figure sources

Scripts that build the redrawn figures in `../imgs/`. All follow the house style in
[`../figure-style.md`](../figure-style.md): the 8-colour palette, Source Sans Pro, black axes,
one base colour (indigo) with red for emphasis, thin sky-blue guides.

Run each from the repo root with the output folder as argument, e.g.

```sh
python3 figures-src/make_occupier.py imgs
```

| Slide | Output in `imgs/` | Script |
|:---|:---|:---|
| A Conceptual Framework | `4qm-red.svg` | `make_4qm.py` |
| The Investment / Development Market, Property Market Stock Adjustment | `investment-market.svg`, `development-market.svg`, `adjustment-market.svg` | `make_4qm.py` |
| The Occupier Market (short- and long-run supply) | `occupier.svg` | `make_occupier.py` |
| Durable supply | `kinked_supply.svg` | `make_kinked_supply.py` |
| Reaching the development decision | `graaskamp-spiral.svg` | `make_graaskamp.py` |
| Investment Market (rent/price) | `rent-price-amsterdam.svg` | `amsterdam-rent-price/` |
| Growth US house prices? | `us-house-prices.svg` | `us-house-prices/` |
| Norway? | `norway.svg` | `norway/` |
| Netherlands? | `amsterdam-house-prices.svg` | `amsterdam-house-prices/` |

`make_4qm.py` also writes `4qm.svg` and `space-market.svg`, which are used by the
lecture 4 deck (`talk-p4-l4-occupier-market`), and the single-market figures that lectures 2
and 3 use. Copy those over by hand after a change.

## Data-driven charts

Each folder holds a `build_data.py` (raw data → tidy CSV), a `make_figure.py` (CSV → SVG) and a
`data/` folder with the raw snapshots and the CSV, so the charts rebuild without network access.

```sh
python3 figures-src/norway/build_data.py          # needs openpyxl; fetches SSB CPI
python3 figures-src/norway/make_figure.py imgs
```

| Folder | Sources | Notes |
|:---|:---|:---|
| `norway/` | Norges Bank HMFS house prices and CPI; Statistics Norway table 03014 | real, 1819 = 100; trends 1875–2000 and 1995–2023 |
| `us-house-prices/` | Shiller, `Fig3-1.xls` (shillerdata.com) | needs xlrd; annual averages, last year partial |
| `amsterdam-rent-price/` | Ambrose, Eichholtz & Lindenthal (2013) | ratio scaled to 4.5% in 2002, as in the paper's Stata code |
| `amsterdam-house-prices/` | AEL (2013) to 2009; CBS 85792NED (Amsterdam) and 83131NED (CPI) after | `build_data.py --refresh` re-downloads CBS data |

The two Amsterdam builders refresh their AEL snapshot from
`~/research/jmcb_ambrose_eichholtz_lindenthal/` when that folder exists.
