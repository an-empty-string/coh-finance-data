from datetime import datetime, date

import csv
import decimal
import tabula
import re
import sys

def read_file(fname):
    tables = tabula.read_pdf(fname, pages="all")

    fund = 1000
    vendor = ""

    broken = False

    for table in tables:
        if broken:
            break

        rows = list(table.iterrows())
        rows.insert(0, (0, [i for i in table.columns if not i.startswith("Unnamed")]))

        skip = 0
        for row in rows:

            if skip > 0:
                skip -= 1
                continue

            data = list(row[1])
            data = [i.replace("\r", " ") if isinstance(i, str) else i for i in data if str(i) != "nan"]

            print(data)

            if "$" in data:
                break

            # 2022-05-26 tabula fix
            hmcbg = "HUNTSVILLE MADISON COUNTY BOTANICAL GARDENS"
            if len(data) == 6 and isinstance(data[0], str) and data[0].startswith(f"{hmcbg} "):
                data[0] = data[0][len(hmcbg) + 1:]
                data.insert(0, hmcbg)

            # 2022-02-10 tabula fix
            def unsquish(i):
                if not isinstance(data[i], str):
                    return

                m = re.match(r'^(.{8,}) (\d{4}-\d{2}-\d{5}-\d{6}-\d{8}-(\d{5})?)$', data[i])
                if m:
                    vend, acct = m.group(1), m.group(2)
                    data[i] = vend
                    data.insert(i + 1, acct)

            unsquish(1)
            unsquish(0)

            # if len(data) == 7 and data[1] == "COMMUNITY ACTION PARTNERSHIP 2101-70-70100-515520-00000000-00130":
            #     data[1] = "COMMUNITY ACTION PARTNERSHIP"
            #     data.insert(2, "2101-70-70100-515520-00000000-00130")
            #     skip = 1

            # if len(data) == 6 and data[0] == "HAPPI HEALTH 2101-70-70100-515520-00000000-00119":
            #     data[0] = "HAPPI HEALTH"
            #     data.insert(1, "2101-70-70100-515520-00000000-00119")

            if data[0] == "Fund":
                continue

            if "Total Paid by Vendor" in data or (isinstance(data[0], str) and "Total Paid by Vendor" in data[0]):
                continue

            if isinstance(data[0], str) and data[0].startswith("Total by Fund "):
                continue

            if isinstance(data[1], str) and data[1].startswith("Total by Fund "):
                continue

            if "Grand Total" in data or "CK RUN" in data or "CK AMT" in data:
                broken = True
                break

            if len(data) == 7 and isinstance(data[0], str) and len(data[0]) == 4 and data[0].isnumeric():
                # fund, but missing column -- 2021-12-16
                data.insert(4, data[3])

            if len(data) == 8:
                # 2022-09-22 page 36 ("Page N 6" in data)
                if isinstance(data[0], str) and " Page N" in data[0]:
                    data[0] = data[0][:4]
                fund = int(data.pop(0))

            print(data)
            if isinstance(data[0], str) and not (data[0][:4].isnumeric() and data[0][4] == "-"):
                vendor = data.pop(0)

            if len(data) == 5:
                line_item_desc = ""
                long_account, invoice, check, date, amount = data

            elif len(data) == 6:
                long_account, invoice, line_item_desc, check, date, amount = data

            else:
                print(data, "all done")
                broken = True
                break

            date = datetime.strptime(date, "%m/%d/%Y").date()

            amount = str(amount)
            if amount.startswith("("):
                amount = f"-{amount[1:-1]}"

            amount = decimal.Decimal(amount.replace(",", ""))

            results = []

            subs = long_account.split("-")
            fund = subs[0]
            account = subs[1]
            subaccount = "-".join(subs[2:])

            yield fund, account, subaccount, long_account, vendor, invoice, line_item_desc, check, date, amount


def write_csv(data, out=sys.stdout, missed=None):
    w = csv.writer(out)
    w.writerow(["fund","account","subaccount","long_account","vendor","invoice","line_item_desc","check","date","amount"])


    total = 0
    for row in data:
        w.writerow(row)
        total += row[-1]

    if missed is not None:
        for row in missed:
            w.writerow(row)
            total += row[-1]

    return total


with open(sys.argv[2], "w") as f:
    missed = []

    # fix for one tx on last page
    if "2022-03-10" in sys.argv[1]:
        missed.append(("7000", "16", "00000-517020-00000000-", "7000-16-00000-517020-00000000-", "BLUE CROSS AND BLUE SHIELD OF ALABAMA", "GROUP INV DUE 3-1-22", "GROUP INV DUE 3/1/2022", "72324", date(2022, 2, 24), decimal.Decimal("13108.44")))

    if "2022-04-28" in sys.argv[1]:
        missed.append(("7000", "16", "00000-517040-00000000-", "7000-16-00000-517040-00000000-", "PARTNERS MANAGING GENERAL UNDERWRITERS", "US1181644-031922", "CITY'S GROUP HEALTH REINSUR. US1181644 4/22", "73970", date(2022, 4, 11), decimal.Decimal("14636.19")))

    total = write_csv(read_file(sys.argv[1]), f, missed)

    print(f"Wrote ${total:,} of txs")
