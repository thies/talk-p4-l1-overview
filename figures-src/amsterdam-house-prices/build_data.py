"""Build data/amsterdam_house_prices.csv: real Amsterdam house prices, 1650 = 100, 1650-2025.

1650-2009  Ambrose, Eichholtz & Lindenthal (2013, JMCB): Herengracht house price index
           deflated by their CPI. Snapshot: data/ael2013_amsterdam_rent_prices.csv
           (copy of ~/research/jmcb_ambrose_eichholtz_lindenthal/data_amsterdam_rent_prices.csv;
           refreshed from there if that folder exists).
2010-2025  Statistics Netherlands (CBS), chained onto 2009:
           - table 85792NED, price index of existing owner-occupied homes, municipality of
             Amsterdam (GM0363), annual, 2020 = 100;
           - table 83131NED, CPI all items, annual, 2015 = 100.
           Snapshots: data/cbs_amsterdam_hpi.csv, data/cbs_cpi.csv. They are downloaded when
           missing, or always with --refresh.

The CBS index covers the whole city, so it is not the same market as the canal houses.
Over 1995-2009 it grew faster than the Herengracht index (x3.1 vs x2.2 nominal); the
splice only uses its growth after 2009.

Usage:  python3 build_data.py [--refresh]
"""
import csv
import json
import shutil
import sys
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / "data"
AEL_SOURCE = Path.home() / "research/jmcb_ambrose_eichholtz_lindenthal/data_amsterdam_rent_prices.csv"
AEL = DATA / "ael2013_amsterdam_rent_prices.csv"
CBS_HPI = DATA / "cbs_amsterdam_hpi.csv"
CBS_CPI = DATA / "cbs_cpi.csv"
OUT = DATA / "amsterdam_house_prices.csv"
API = "https://opendata.cbs.nl/ODataApi/odata/"
QUERIES = {
    CBS_HPI: ("85792NED", "RegioS eq 'GM0363'", "PrijsindexVerkoopprijzen_1"),
    CBS_CPI: ("83131NED", "Bestedingscategorieen eq 'T001112  '", "CPI_1"),
}
BASE_YEAR, SPLICE_YEAR = 1650, 2009


def fetch(path, table, filt, field):
    """annual values of one CBS series -> csv year,value"""
    q = f"{filt} and substringof('JJ',Perioden)"
    url = (f"{API}{table}/TypedDataSet?$filter={urllib.parse.quote(q)}"
           f"&$select=Perioden,{field}")
    rows = json.load(urllib.request.urlopen(url))["value"]
    with open(path, "w") as f:
        f.write("year,value\n")
        for r in rows:
            if r[field] is not None:
                f.write(f"{r['Perioden'][:4]},{r[field]}\n")


def read(path):
    with open(path) as f:
        return {int(r["year"]): float(r["value"]) for r in csv.DictReader(f)}


def main():
    if AEL_SOURCE.exists():
        shutil.copyfile(AEL_SOURCE, AEL)
    for path, q in QUERIES.items():
        if "--refresh" in sys.argv or not path.exists():
            fetch(path, *q)

    with open(AEL) as f:
        ael = {int(r["year"]): float(r["house price index"]) / float(r["CPI"]) for r in csv.DictReader(f)}
    hpi, cpi = read(CBS_HPI), read(CBS_CPI)
    real = {y: 100 * v / ael[BASE_YEAR] for y, v in ael.items() if y >= BASE_YEAR}
    anchor = hpi[SPLICE_YEAR] / cpi[SPLICE_YEAR]
    last = max(y for y in hpi if y in cpi)
    for y in range(SPLICE_YEAR + 1, last + 1):
        real[y] = real[SPLICE_YEAR] * (hpi[y] / cpi[y]) / anchor

    years = sorted(real)
    assert years == list(range(years[0], years[-1] + 1)), "gap in the series"
    with open(OUT, "w") as f:
        f.write("year,real_house_price_1650eq100,source\n")
        for y in years:
            f.write(f"{y},{real[y]:.2f},{'AEL2013' if y <= SPLICE_YEAR else 'CBS'}\n")
    print(f"wrote {OUT} ({years[0]}-{years[-1]}); {SPLICE_YEAR}: {real[SPLICE_YEAR]:.0f}, "
          f"{years[-1]}: {real[years[-1]]:.0f}")


if __name__ == "__main__":
    main()
