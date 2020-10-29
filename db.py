
from models import Model
import shelve
from dataclasses import dataclass
import random
from os import urandom
random.seed(int.from_bytes(urandom(4), byteorder='big'))

@dataclass
class record:
    model: Model
    cimobj: dict
    files: []


# We do not use Writeback mode here, so beware
models = shelve.open("cimpy.db")

def get_model(id_):
    """Get a network model
    This is only useful at the moment to get the name of the model

    :param id: Model id
    :type id: int

    :rtype: Model
    """
    global models
    try:
        return models[str(id_)]
    except KeyError:
        return Error(code=404, message="Model not found"), 404


def get_models():
    """Get a list of all network models

    :rtype: dict
    """
    global models
    if models == {}:
        return Error(code=404, message="No models in to database"), 404
    model_list = []
    for key, rec in models.items():
        model_list.append(ModelReply.from_model(rec.model, int(key)))
    return model_list


def put_model(new_model, cimpy_data, files):
    """Store a model in the db

    :param new_model: Model object (see models/base_model.py)
    :param cimpy_data: data extracted from files by cimpy
    :rtype: integer
    """
    global models

    # generate a new UUID which will be the model ID
    new_id = random.getrandbits(32)
    # Ensure ID is unique
    while str(new_id) in models:
        new_id = random.getrandbits(32)

    models[str(new_id)] = record(new_model, cimpy_data, files)

    return new_id


