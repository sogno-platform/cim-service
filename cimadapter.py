import cimpy
import connexion
import json
import shelve
from models import Error
from models import Model
from models import ModelElementUpdate
from models import ModelUpdate
from models import NewModel
from models import NewModelElement
from dataclasses import dataclass
#  import pdb
import random
from os import urandom
from xml.etree.ElementTree import ParseError

random.seed(int.from_bytes(urandom(4), byteorder='big'))


@dataclass
class record:
    name: str
    cimobj: dict


# We do not use Writeback mode here, so beware
models = shelve.open("cimpy.db")


def add_element(id, new_model_element):
    """Add element to model

    :param id: Model id
    :type id: int
    :param new_model_element: Element to be added to model
    :type new_model_element: dict | bytes

    :rtype: ModelElement
    """
    if connexion.request.is_json:
        new_model_element = NewModelElement.from_dict(
            connexion.request.get_json())
    raise Exception('Unimplemented')


def add_model():
    """Add a new network model
    """
    global models

    try:
        new_model = NewModel.from_request(connexion.request)
    except ParseError:
        return Error(code=400, message="Invalid XML files"), 400

    # generate a new UUID which is the model ID
    new_id = random.getrandbits(32)
    # Ensure ID is unique
    while str(new_id) in models:
        new_id = random.getrandbits(32)

    # TODO: cgmes version?
    cimpy_data = cimpy.cim_import(new_model.files,
                                  cgmes_version="cgmes_v2_4_15")
    models[str(new_id)] = record(new_model.name, cimpy_data)

    # Return the model as "Model" JSON
    return Model(new_id, new_model.name)


def get_models():
    """Get a list of all network models

    :rtype: dict
    """
    global models
    if models == {}:
        return Error(code=404, message="No models in to database"), 404
    model_list = []
    for key, v in models.items():
        model_list.append({'id': int(key), "name": v.name})
    return model_list


def delete_element(id, id_):
    """Delete element of model


    :param id: model id
    :type id: int
    :param id: element id
    :type id: int

    :rtype: ModelElement
    """
    raise Exception('Unimplemented')


def delete_model(id_):
    """Delete a network model

    :param id: Model id
    :type id: int

    :rtype: Model
    """
    global models

    if str(id_) in models:
        model = Model.from_dict({'name': models[str(id_)].name, 'id': id_})
        del models[str(id_)]
        return model
    else:
        return Error(code=404, message="No models in to database"), 404


def export_model(id_):
    """Export model to file

    Returns an archive containing the grid data in CIM formatted files and
    profile files that might have been imported previously.

    :param id: Model id
    :type id: int

    :rtype: file
    """
    raise Exception('Unimplemented')


def get_element(id, id_):
    """Get element of model

    :param id: Model id
    :type id: int
    :param id: Element id
    :type id: int

    :rtype: ModelElementAttributes
    """
    raise Exception('Unimplemented')


def get_elements(id_):
    """Get all elements of a model


    :param id: Model id
    :type id: int

    :rtype: List[ModelElement]
    """
    raise Exception('Unimplemented')


def get_model(id_):
    """Get a network model


    :param id: Model id
    :type id: int

    :rtype: Model
    """
    global models
    try:
        return Model.from_dict({'name': models[str(id_)].name, 'id': id_})
    except KeyError:
        return Error(code=404, message="Model not found"), 404


def get_model_image(id_):
    """Render and return image of network model

    Returns an SVG image of the network based on CIM information. # noqa: E501

    :param id: Model id
    :type id: int

    :rtype: file
    """
    raise Exception('Unimplemented')


def import_model(id, body):
    """Import model from file

    The input file should be an archive containing the grid data in the CIM
    format. Optionally, profiles or stochastic parameters can be given as
    additional files, where file and column name should correspond to the CIM
    component uuid and attribute name. # noqa: E501

    :param id: Model id
    :type id: int
    :param body: Files defining the model
    :type body: str

    :rtype: Model
    """
    raise Exception('Unimplemented')


def update_element(id, elem_id, model_element_update):
    """Update element of model


    :param id: model id
    :type id: int
    :param elem_id: element id
    :type elem_id: int
    :param model_element_update: Model Element attributes to be updated
    :type model_element_update: dict | bytes

    :rtype: ModelElement
    """
    if connexion.request.is_json:
        model_element_update = ModelElementUpdate.from_dict(
            connexion.request.get_json())
    raise Exception('Unimplemented')


def update_model(id, model_update):
    """Update a network model


    :param id: Model id
    :type id: int
    :param model_update: Network model to be updated
    :type model_update: dict | bytes

    :rtype: Model
    """
    if connexion.request.is_json:
        model_update = ModelUpdate.from_dict(connexion.request.get_json())
    raise Exception('Unimplemented')


def apikey_auth(apikey, required_scopes=None):
    if apikey == '123':
        return {'sub': 'admin'}

    # optional: raise exception for custom error response
    return None
