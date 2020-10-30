
from models import Model
from models import ModelReply
from models import Error
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

def get_model(model_id):
    """Get a network model
    This is only useful at the moment to get the name of the model

    :param id: Model id
    :type id: int

    :rtype: Model
    """
    global models
    try:
        return models[str(model_id)].model
    except KeyError:
        return None


def get_models():
    """Get a list of all network models

    :rtype: dict
    """
    global models
    if models == {}:
        return Error(code=404, message="No models found in database"), 404
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

def delete_model(model_id):
    """Delete a network model

    :param id: Model id
    :type id: int

    :rtype: Model
    """
    if str(model_id) in models:
        model_reply = ModelReply.from_model(models[str(model_id)].model, model_id)
        del models[str(model_id)]
        return model_reply
    else:
        return Error(code=404, message="Cannot delete model with id: " + str(model_id) + ", not found in database"), 404


