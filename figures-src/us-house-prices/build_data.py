"""Build data/us_house_prices.csv: US real home price index (1890 = 100), annual.

Input: Robert Shiller, "Fig3-1.xls" (U.S. Home Price and Related Data, from
Irrational Exuberance), sheet "Data", column B "Real Home Price Index".
Annual to 1952, monthly from 1953; monthly values are averaged by calendar year.
The final year may be partial; its number of months is recorded in the CSV.
https://shillerdata.com/

Usage:  python3 build_data.py        (needs xlrd; the .xls must be in data/raw/)
"""
from collections import defaultdict
from pathlib import Path

import xlrd

HERE = Path(__file__).parent
RAW = HERE / "data" / "raw" / "Fig3-1.xls"
OUT = HERE / "data" / "us_house_prices.csv"


def main():
    sh = xlrd.open_workbook(RAW).sheet_by_name("Data")
    by_year = defaultdict(list)
    for r in range(sh.nrows):
        date, val = sh.cell_value(r, 0), sh.cell_value(r, 1)
        if isinstance(date, float) and isinstance(val, float) and date >= 1890:
            by_year[int(date + 1e-6)].append(val)
    years = sorted(by_year)
    assert years == list(range(years[0], years[-1] + 1)), "gap in the series"
    with open(OUT, "w") as f:
        f.write("year,hpi_real_1890eq100,n_obs\n")
        for y in years:
            v = by_year[y]
            f.write(f"{y},{sum(v) / len(v):.3f},{len(v)}\n")
    print(f"wrote {OUT} ({years[0]}-{years[-1]}, last year {len(by_year[years[-1]])} obs)")


if __name__ == "__main__":
    main()
