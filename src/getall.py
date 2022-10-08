import datetime
from legistar import LegistarAPI

for event in LegistarAPI("huntsvilleal").events:
    if event.body_name != "City Council Regular Meeting":
        continue

    if event.timestamp > datetime.datetime.now():
        continue

    print(event.timestamp.date().strftime("%Y-%m-%d"))
    for item in event.items:
        if not item["EventItemTitle"]:
            continue

        if "authorizing expenditures for payment" not in item["EventItemTitle"]:
            continue

        for att in item["EventItemMatterAttachments"]:
            if att["MatterAttachmentFileName"].endswith(".pdf"):
                break

        else:
            continue

        print(att["MatterAttachmentHyperlink"])
