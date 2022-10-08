import csv
import sys

data = []
header = None

def spnorm(s):
    return " ".join(s.split())

for i in sys.argv[1:-1]:
    if i == sys.argv[-1]:
        continue

    with open(i) as f:
        r = csv.reader(f)
        for row in r:
            if not row:
                continue

            if row[0] == "fund":
                header = row
                continue

            fund, account, subaccount, long_account, vendor, invoice, line_item_desc, check, date, amount = row

            vendor = spnorm(vendor)
            invoice = spnorm(invoice)
            line_item_desc = spnorm(line_item_desc)
            if check.endswith(".0"):
                check = check[:-2]

            row = fund, account, subaccount, long_account, vendor, invoice, line_item_desc, check, date, amount

            data.append(row)

# date, account, vendor, invoice
data.sort(key=lambda row: (row[8], row[3], row[4], row[5]))

data.insert(0, header)
with open(sys.argv[-1], "w") as d:
    w = csv.writer(d)
    w.writerows(data)
