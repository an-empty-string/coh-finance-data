# CoH finance data and tools

This repository contains historical data released by the City of Huntsville finance department, and tools to parse it. Here's what everything does:

* `src/scrape.py`: Run as `python src/scrape.py data/some.pdf out/some.csv`, hopefully get a CSV with all the transaction data from the PDF.
* `src/getall.py`: Output a list of council meeting dates and likely finance committee report URLs. (You can pipe this to a shell script that invokes wget, etc.) Only works for meetings on Legistar, meetings on NovusAGENDA aren't included.
* `src/legistar.py`: Legistar API wrapper.
* `data/`: Source PDFs. Filenames are dates of council meetings when reports were released. TXT data is from poppler `pdftotext`
* `out/`: CSVs containing finance data. Filenames match source PDF filenames. Data in here has been minimally quality checked (i.e. I've made sure the totals match up)

## Known issues

* `tabula-py` misses transactions if they are the only transaction on the last page of the transactions list. We have to add them back ourselves.
