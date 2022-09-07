import json
from abc import ABC, abstractmethod


class JsonObject(ABC):
    @abstractmethod
    def to_json(self):
        pass

    def __str__(self):
        return json.dumps(self.to_json(), indent=4)

    def __repr__(self):
        return self.__str__()
