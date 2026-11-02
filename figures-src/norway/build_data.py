"""Build data/norway_house_prices.csv: Norwegian real house prices, 1819 = 100.

Inputs (downloaded to data/raw/ if missing):
  - Norges Bank HMFS house price workbook, sheet "Composite HPIs", column "Total"
    (Eitrheim & Erlandsen repeat-sales index to 1985, NEF/ECON hedonic 1985-2005,
    Statistics Norway from 2005; nominal, 1912 = 100).
    https://www.norges-bank.no/en/topics/Statistics/Historical-monetary-statistics/
  - Norges Bank HMS CPI workbook, sheet "p1_c3_table_14" (annual CPI, 2015 = 100, to 2017).
  - Statistics Norway table 03014 (annual CPI, 2015 = 100) for the years after 2017;
    it equals the Norges Bank series in 2017 (105.5), so no rebasing is needed.

Usage:  python3 build_data.py        (needs openpyxl)
"""
import json
import urllib.request
from pathlib import Path

import openpyxl

HERE = Path(__file__).parent
RAW = HERE / "data" / "raw"
OUT = HERE / "data" / "norway_house_prices.csv"
NB = "https://www.norges-bank.no/globalassets/upload/hms/data/"
HPI_FILE = "hmfs-houseprice-indices-norway_1819-2023.xlsx"
CPI_FILE = "cpi.xlsx"
SSB_API = "https://data.ssb.no/api/v0/en/table/03014"


def fetch(name):
    path = RAW / name
    if not path.exists():
        RAW.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(NB + name, path)
    return path


def read_sheet(path, sheet):
    """{year: value} from the first two columns, keeping rows that start with a year"""
    ws = openpyxl.load_workbook(path, data_only=True, read_only=True)[sheet]
    out = {}
    for row in ws.iter_rows(values_only=True):
        if row and str(row[0]).strip().isdigit() and isinstance(row[1], (int, float)):
            out[int(row[0])] = float(row[1])
    return out


def ssb_cpi(years):
    query = {"query": [
        {"code": "Konsumgrp", "selection": {"filter": "item", "values": ["TOTAL"]}},
        {"code": "ContentsCode", "selection": {"filter": "item", "values": ["KpiAar"]}},
        {"code": "Tid", "selection": {"filter": "item", "values": [str(y) for y in years]}}],
        "response": {"format": "json-stat2"}}
    req = urllib.request.Request(SSB_API, json.dumps(query).encode(),
                                 {"Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req))
    return {int(y): float(v) for y, v in zip(d["dimension"]["Tid"]["category"]["index"], d["value"])}


def main():
    hpi = read_sheet(fetch(HPI_FILE), "Composite HPIs")
    cpi = read_sheet(fetch(CPI_FILE), "p1_c3_table_14")
    later = [y for y in hpi if y > max(cpi)]
    if later:
        cpi.update(ssb_cpi(sorted(later)))
    years = sorted(y for y in hpi if y in cpi)
    assert years == list(range(years[0], years[-1] + 1)), "gap in the series"
    real = {y: hpi[y] / cpi[y] for y in years}
    with open(OUT, "w") as f:
        f.write("year,hpi_nominal_1912eq100,cpi_2015eq100,hpi_real_1819eq100\n")
        for y in years:
            f.write(f"{y},{hpi[y]:.4f},{cpi[y]:.4f},{100 * real[y] / real[1819]:.2f}\n")
    print(f"wrote {OUT} ({years[0]}-{years[-1]})")


if __name__ == "__main__":
    main()
