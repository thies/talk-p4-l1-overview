"""Build data/amsterdam_rent_price.csv: Amsterdam rent/price ratio, 1650-2009.

Input: data/ael2013_amsterdam_rent_prices.csv, a snapshot of
~/research/jmcb_ambrose_eichholtz_lindenthal/data_amsterdam_rent_prices.csv
(Ambrose, Eichholtz & Lindenthal 2013, JMCB 45(2-3), 477-491): Herengracht house price
index and Amsterdam rent index, 1649-2009. If the research folder exists, the snapshot is
refreshed from it first.

The two indices only give the ratio up to a constant. As in the paper's Stata code
(stata/AmbroseEichholtzLindenthal.do), rents are scaled so that the ratio is 4.5% in 2002:
    rent/price_t = 0.045 * (R_t / P_t) / (R_2002 / P_2002)
CPI cancels, so the ratio is the same in real and nominal terms.

Usage:  python3 build_data.py
"""
import csv
import shutil
from pathlib import Path

HERE = Path(__file__).parent
SOURCE = Path.home() / "research/jmcb_ambrose_eichholtz_lindenthal/data_amsterdam_rent_prices.csv"
SNAPSHOT = HERE / "data" / "ael2013_amsterdam_rent_prices.csv"
OUT = HERE / "data" / "amsterdam_rent_price.csv"
FIRST_YEAR = 1650
SCALE_YEAR, SCALE_LEVEL = 2002, 0.045


def main():
    if SOURCE.exists():
        shutil.copyfile(SOURCE, SNAPSHOT)
    with open(SNAPSHOT) as f:
        rows = {int(r["year"]): (float(r["house price index"]), float(r["rent index"]))
                for r in csv.DictReader(f)}
    p0, r0 = rows[SCALE_YEAR]
    k = SCALE_LEVEL / (r0 / p0)
    years = [y for y in sorted(rows) if y >= FIRST_YEAR]
    assert years == list(range(years[0], years[-1] + 1)), "gap in the series"
    with open(OUT, "w") as f:
        f.write("year,house_price_index,rent_index,rent_price_pct\n")
        for y in years:
            p, r = rows[y]
            f.write(f"{y},{p:.2f},{r:.2f},{100 * k * r / p:.4f}\n")
    print(f"wrote {OUT} ({years[0]}-{years[-1]})")


if __name__ == "__main__":
    main()
