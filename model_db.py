
from models import Model
from models import ModelReply
from models import Error
from dataclasses import dataclass
import redis
from tempfile import SpooledTemporaryFile

@dataclass
class record:
    model: Model
    cimobj: dict
    files: []

# The hostname "redis" is set for development as an alias
# in the docker-compose.yaml file. For production this will
# resolve via the kubernetes service name
try:
    redis_connection = redis.Redis("redis-master")
except redis.exceptions.ConnectionError:
    redis_connection = None
    print("WARNING: Unable to connect to redis.")

# TEST ONLY
def overwrite_connection(connection):
    global redis_connection
    redis_connection = connection

def get_model(model_id):
    """Get a network model
    This is only useful at the moment to get the name of the model

    :param id: Model id
    :type id: int

    :rtype: Model
    """
    model = redis_connection.get(model_id).decode("utf-8")
    cimpy_data = redis_connection.get(str(model_id) + "_cimpy").decode('utf-8')
    files_len = int(redis_connection.get(str(model_id) + "_files_len").decode('utf-8'))
    files = []
    for index in range(files_len):
        data_addr = str(model_id) + "_file_" + str(index)
        data = redis_connection.get(data_addr)
        files.append(data.decode("utf-8"))
    return record( model, cimpy_data, files )

def get_models():
    """Get a list of all network models

    :rtype: dict
    """
    def decode(a):
        print(a)
        model_id_char   = a.decode('utf-8')
        model_bytes     = redis_connection.get(model_id_char)
        if model_bytes != None:
            model       = eval(model_bytes.decode('utf-8'))
        else:
            model       = { "name"    : "NOT FOUND",
                            "version" : "cgmes_v2_4_15",
                            "profiles": [] }
        model['id']     = int(model_id_char)
        return model

    if redis_connection.smembers("models") != None:
        return list(map(decode, redis_connection.smembers("models")))
    else:
        return []

def get_record(model_id):
    """Get the full record of a stored model. This includes the cimobj and the xml files.

    :param model_id: Model id fs
    :type model_id: int

    :rtype: record
    """
    global models
    try:
        return models[str(model_id)]
    except KeyError:
        return Non

def put_model(new_model, cimpy_data, files):
    """Store a model in the db

    :param new_model: Model object (see models/base_model.py)
    :param cimpy_data: data extracted from files by cimpy
    :rtype: integer
    """
    # atomic increment the model_instance
    # variable to get a unique id
    new_id = redis_connection.incr("model_instance")
    redis_connection.sadd("models", str(new_id))
    redis_connection.set(str(new_id), new_model.__repr__())
    redis_connection.set(str(new_id) + "_cimpy", cimpy_data.__repr__())
    redis_connection.set(str(new_id) + "_files_len", len(files))
    for index,file_ in enumerate(files):
        file_.seek(0)
        data = file_.read()
        data_addr = str(new_id) + "_file_" + str(index)
        redis_connection.set(data_addr, data)
    return new_id

def delete_model(model_id):
    """Delete a network model

    :param id: Model id
    :type id: int

    :rtype: Model
    """
    model_bytes     = redis_connection.get(model_id)
    if model_bytes != None:
        print("MODEL_BYTES: ", model_bytes)
        model       = eval(model_bytes.decode('utf-8'))
        model['id'] = int(model_id)
    else:
        return Error(code=404, message="Cannot delete model with id: " + str(model_id) + ", not found in database"), 404

    files_len_bytes = redis_connection.get(str(model_id) + "_files_len")
    files_len       = int(files_len_bytes.decode('utf-8'))
    redis_connection.delete(str(model_id))
    redis_connection.delete(str(model_id) + "_cimpy")
    redis_connection.delete(str(model_id) + "_files_len")
    for index in range(files_len):
        redis_connection.delete(str(model_id) + "_file_" + str(index))
    redis_connection.srem("models", model_id)
    return model
