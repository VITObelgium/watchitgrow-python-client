import json

from pywig.api.models import JsonObject


class MeteoStat(JsonObject):
    def __init__(self, date: str, value: float):
        self.date = date
        self.value = value

    def to_json(self) -> dict:
        stat = dict()
        stat['date'] = self.date
        stat['value'] = self.value
        return stat
