# CoH finance data and tools

This repository contains historical data released by the City of Huntsville finance department, and tools to parse it. Here's what everything does:

* `src/scrape.py`: Run as `python src/scrape.py data/some.pdf out/some.csv`, hopefully get a CSV with all the transaction data from the PDF.
* `src/getall.py`: Output a list of council meeting dates and likely finance committee report URLs. (You can pipe this to a shell script that invokes wget, etc.) Only works for meetings on Legistar, meetings on NovusAGENDA aren't included.
* `src/legistar.py`: Legistar API wrapper.
* `data/`: Source PDFs. Filenames are dates of council meetings when reports were released. TXT data is from poppler `pdftotext`
* `out/`: CSVs containing finance data. Filenames match source PDF filenames. Data in here has been minimally quality checked (i.e. I've made sure the totals match up)

## Sample workflow

* Run `nix develop` to get into a shell with dependencies. You can get Nix at https://nixos.org/download/ -- you only need the package manager, not NixOS
* Run `python3 src/getall.py | tee data/meetings.txt`. You will get a file `data/meetings.txt` with a list of dates followed by the PDF reports they correspond to. Some dates won't have reports (they might be special meetings or someone forgot to upload a finance committee report). Some dates may have multiple PDFs (in this case you will need to disambiguate). Join the lines with the dates and the lines with the PDF URLs together so that they look like the example in this repository.
* Take a subset of `data/meetings.txt` you want to work with and write it to e.g. `data/fy23.txt`. Then run `while read date url; do wget -O data/$date.pdf $url; done < data/fy23.txt` to download all the reports.
* Run `scrape.py` on each day manually, like this: `day=2023-10-26; pdftotext data/$day.pdf; python3 src/scrape.py data/$day.pdf out/$day.csv`
* The script will often stop when it doesn't know who to attribute a transaction to. It will prompt you. Look at the last parsed line it output and find the matching transaction in the PDF. If the vendor matches, you can just hit enter. Otherwise type the vendor name (all caps probably) and hit enter.
* At the end, you will see a message like "Wrote $13,433,187.53 of txs". This number should match the "Grand Total" in the PDF. If it does not, something may have gone wrong, see the known issues section below.

## Known issues

* `tabula-py` misses transactions if they are the only transaction on the last page of the transactions list. We have to add them back ourselves.
