import datetime
import requests

from dataclasses import dataclass, field, fields
from functools import cached_property
from typing import Optional


def get_event_timestamp(props):
    date = datetime.datetime.strptime(
        props["EventDate"].split("T")[0], "%Y-%m-%d").date()

    time = datetime.datetime.strptime(
        props["EventTime"], "%I:%M %p").time()

    return datetime.datetime.combine(date, time)


class LegistarObject():
    _id_field = None

    def __init__(self, api, props):
        self.id = props[self._id_field]
        self.api = api
        self.props = props

        for field in fields(self):
            meta = field.metadata

            if "key" in meta:
                value = props[meta["key"]]
            elif "call" in meta:
                value = meta["call"](props)

            setattr(self, field.name, value)


@dataclass
class LegistarEventItem(LegistarObject):
    _id_field = "EventItemId"

    def __init__(self, api, props):
        super().__init__(api, props)

    title: str = field(metadata={"key": "EventItemTitle"})
    matter_id: int = field(metadata={"key": "EventItemMatterId"})


@dataclass
class LegistarEvent(LegistarObject):
    _id_field = "EventId"

    def __init__(self, api, props):
        super().__init__(api, props)

    timestamp: datetime.datetime = field(metadata={"call": get_event_timestamp})
    body_id: int = field(metadata={"key": "EventBodyId"})
    body_name: str = field(metadata={"key": "EventBodyName"})
    agenda_url: Optional[str] = field(metadata={"key": "EventAgendaFile"})
    minutes_url: Optional[str] = field(metadata={"key": "EventMinutesFile"})
    ui_url: Optional[str] = field(metadata={"key": "EventInSiteURL"})

    @cached_property
    def items(self):
        return requests.get(
            f"{self.api.url}/Events/{self.id}/EventItems",
            params={"AgendaNote": "1", "MinutesNote": "1",
                    "Attachments": "1"},
         ).json()


class LegistarAPI():
    def __init__(self, client):
        self.url = f"https://webapi.legistar.com/v1/{client}"

    @cached_property
    def events(self):
        return [LegistarEvent(self, e) for e in
                requests.get(f"{self.url}/Events").json()]
