#!/usr/bin/env python

import csv
import sqlite3
import sys


SCHEMA = """
CREATE TABLE penguins (
    species text,
    island text,
    bill_length_mm real,
    bill_depth_mm real,
    flipper_length_mm real,
    body_mass_g real,
    sex text
);
CREATE TABLE geography (
    island text,
    lat_s real,
    long_w real,
    area_km2 real,
    max_elevation_m real,
    shape text,
    features text
);
"""


def main():
    outfile = sys.argv[1]

    con = sqlite3.connect(outfile)
    con.executescript(SCHEMA)
    make_penguins(con, sys.argv[2])
    make_geography(con, sys.argv[3])
    con.close()


def make_penguins(con, filename):
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                row["species"],
                row["island"],
                float(row["bill_length_mm"]) if row["bill_length_mm"] else None,
                float(row["bill_depth_mm"]) if row["bill_depth_mm"] else None,
                float(row["flipper_length_mm"]) if row["flipper_length_mm"] else None,
                float(row["body_mass_g"]) if row["body_mass_g"] else None,
                row["sex"] if row["sex"] else None,
            )
            for row in reader
        ]

    con.executemany(
        "INSERT INTO penguins VALUES (?, ?, ?, ?, ?, ?, ?)", rows
    )
    con.commit()


def make_geography(con, filename):
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                row["island"],
                float(row["lat_s"]),
                float(row["long_w"]),
                float(row["area_km2"]),
                float(row["max_elevation_m"]),
                row["shape"],
                row["features"],
            )
            for row in reader
        ]

    con.executemany(
        "INSERT INTO geography VALUES (?, ?, ?, ?, ?, ?, ?)", rows
    )
    con.commit()


if __name__ == "__main__":
    main()
