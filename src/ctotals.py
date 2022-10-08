import decimal
import glob
import csv

for f in glob.glob("*.csv"):
    with open(f) as g:
        next(g)
        amt = 0

        for line in g:
            fields = line.strip().split(",")
            amt += decimal.Decimal(fields[-1])

    print(f, amt)
