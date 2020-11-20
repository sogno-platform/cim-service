
from models import Model
from models import ModelReply
from models import Error
import shelve
from dataclasses import dataclass
import random
from os import urandom
import redis
random.seed(int.from_bytes(urandom(4), byteorder='big'))
from tempfile import SpooledTemporaryFile

@dataclass
class record:
    model: Model
    cimobj: dict
    files: []

# The hostname "redis" is set for development as an alias
# in the docker-compose.yaml file. For production this will
# resolve via the kubernetes service name
connection = redis.Redis("redis")

def get_model(model_id):
    """Get a network model
    This is only useful at the moment to get the name of the model

    :param id: Model id
    :type id: int

    :rtype: Model
    """
    model = connection.get(model_id).decode("utf-8")
    cimpy_data = connection.get(str(model_id) + "_cimpy").decode('utf-8')
    files_len = int(connection.get(str(model_id) + "_files_len").decode('utf-8'))
    files = []
    for index in range(files_len):
        data_addr = str(model_id) + "_file_" + str(index)
        data = connection.get(data_addr)
        newfile = SpooledTemporaryFile()
        newfile.write(data)
        files.append(newfile)
    return record( model, cimpy_data, files )

def get_models():
    """Get a list of all network models

    :rtype: dict
    """
    def decode(a):
        print(a)
        model_id_char   = a.decode('utf-8')
        model_bytes     = connection.get(model_id_char)
        if model_bytes != None:
            model       = eval(model_bytes.decode('utf-8'))
        else:
            model       = { "name"    : "NOT FOUND",
                            "version" : "cgmes_v2_4_15",
                            "profiles": [] }
        model['id']     = int(model_id_char)
        return model

    if connection.smembers != None:
        return list(map(decode, connection.smembers("models")))
    else:
        return []


def put_model(new_model, cimpy_data, files):
    """Store a model in the db

    :param new_model: Model object (see models/base_model.py)
    :param cimpy_data: data extracted from files by cimpy
    :rtype: integer
    """
    # atomic increment the model_instance
    # variable to get a unique id
    new_id = connection.incr("model_instance")
    connection.sadd("models", str(new_id))
    connection.set(str(new_id), new_model.__repr__())
    connection.set(str(new_id) + "_cimpy", cimpy_data.__repr__())
    connection.set(str(new_id) + "_files_len", len(files))
    for index,file_ in enumerate(files):
        file_.seek(0)
        data = file_.read()
        data_addr = str(new_id) + "_file_" + str(index)
        connection.set(data_addr, data)
    return new_id

def delete_model(model_id):
    """Delete a network model

    :param id: Model id
    :type id: int

    :rtype: Model
    """
    model_bytes     = connection.get(model_id)
    if model_bytes != None:
        model       = eval(model_bytes.decode('utf-8'))
        model['id'] = int(model_id)
    else:
        return Error(code=404, message="Cannot delete model with id: " + str(model_id) + ", not found in database"), 404

    files_len_bytes = connection.get(str(model_id) + "_files_len")
    files_len       = int(files_len_bytes.decode('utf-8'))
    connection.delete(str(model_id))
    connection.delete(str(model_id) + "_cimpy")
    connection.delete(str(model_id) + "_files_len")
    for index in range(files_len):
        connection.delete(str(model_id) + "_file_" + str(index))
    connection.srem("models", model_id)
    return model
