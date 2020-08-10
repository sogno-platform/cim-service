import cimpy
import connexion
from models import Error
from models import Model
from models import ModelElementUpdate
from models import ModelUpdate
from models import NewModel
from models import NewModelElement
#  import pdb
import random
from os import urandom
from xml.etree.ElementTree import ParseError

random.seed(int.from_bytes(urandom(4), byteorder='big'))

models = {}


def add_element(modelid, new_model_element):
    """Add element to model

    :param modelid: Model id
    :type modelid: int
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
    print("dumdidum")

    request = connexion.request
    cim_xml = request.files.getlist("files")
    id = request.form["name"]

    try:
        new_model = NewModel(name=id, files=cim_xml)
    except ParseError:
        return Error(code=400, message="Invalid XML files"), 400
    # TODO: Import the model using Cimpy
    # generate a new UUID which is the model ID
    newid = random.getrandbits(32)
    # Return the model as "Model" JSON
    new_model = Model(id=newid, name=new_model.name)
    global models
    models[newid] = new_model
    return new_model


def get_models():
    """Get all network models

    :rtype: str
    """
    global models
    # print("globalvar is %d" globalvar)
    return models



def delete_element(modelid, id_):
    """Delete element of model


    :param modelid: model id
    :type modelid: int
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
    raise Exception('Unimplemented')


def export_model(id_):
    """Export model to file

    Returns an archive containing the grid data in CIM formatted files and
    profile files that might have been imported previously.

    :param id: Model id
    :type id: int

    :rtype: file
    """
    raise Exception('Unimplemented')


def get_element(modelid, id_):
    """Get element of model

    :param modelid: Model id
    :type modelid: int
    :param id: Element id
    :type id: int

    :rtype: ModelElementAttributes
    """
    raise Exception('Unimplemented')


def get_elements(modelid_):
    """Get all elements of a model


    :param modelid: Model id
    :type modelid: int

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
    print("== Model ID", id_)
    if id_ in models:
        return models[id_]
    else:
        return Error(code=404, message="Model not found")


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


def update_element(modelid, id, model_element_update):
    """Update element of model


    :param modelid: model id
    :type modelid: int
    :param id: element id
    :type id: int
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
