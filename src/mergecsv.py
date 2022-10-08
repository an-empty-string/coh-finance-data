import csv
import sys

data = []
header = None

for i in sys.argv[1:-1]:
    with open(i) as f:
        r = csv.reader(f)
        for row in r:
            if not row:
                continue

            if row[0] == "fund":
                header = row
                continue

            data.append(row)

# date, account, vendor, invoice
data.sort(key=lambda row: (row[8], row[3], row[4], row[5]))

data.insert(0, header)
with open(sys.argv[-1], "w") as d:
    w = csv.writer(d)
    w.writerows(data)
