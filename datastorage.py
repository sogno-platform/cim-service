
from dataclasses import dataclass
from models import Model


@dataclass
class record:
    id: int
    name: str
    files: [str]


class Datastorage:
    """This class is a poor mans Database and should be replaced by a proper
    database later
    """
    # TODO: Custom Exceptions
    _data: {}

    def __init__(self):
        self._data = {}

    def contains(self, id):
        """Checks if the given ID is in the Datastorage
        """
        if id in self._data:
            return True
        else:
            return False

    def insert(self, id, name, files):
        self._data[id] = record(id, name, files)

    # def append(self, id, files):

    # def remove(self, id):

    # def update(self, id, name):

    def get_model(self, id):
        """Returns the entry specified by `id` as `Model`
        """
        record = self._data[id]
        return Model(id=record.id, name=record.name)

    def get_model_list(self):
        """Returns a list with all models. The models form a dict with the
        values "id" and "name"
        """
        if self._data == {}:
            raise RuntimeError("No models in Datastorage")
        model_list = []
        for m, v in self._data.items():
            model_list.append({'id': v.id, "name": v.name})
        return model_list
