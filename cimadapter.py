import cimpy
import connexion
import shelve
from models import Error
from models import Model
from models import ModelReply
# from models import ModelElementUpdate
# from models import ModelUpdate
# from models import NewModelElement
from dataclasses import dataclass
#  import pdb
import random
from os import urandom
from xml.etree import ElementTree

random.seed(int.from_bytes(urandom(4), byteorder='big'))


@dataclass
class record:
    model: Model
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
    # if connexion.request.is_json:
    #     new_model_element = NewModelElement.from_dict(
    #         connexion.request.get_json())
    raise Exception('Unimplemented')


def add_model():
    """Add a new network model
    """
    global models

    # parse the json request
    new_model = Model.from_dict(connexion.request.form)
    try:
        # parse the attached xml files
        req_files = connexion.request.files.getlist("files")
        files = []
        for f in req_files:
            # Validate xml input
            filestr = f.stream.read()
            ElementTree.fromstring(filestr)
            f.stream.seek(0)
            files.append(f.stream)
    except ElementTree.ParseError:
        return Error(code=422, message="Invalid XML files"), 422

    # generate a new UUID which will be the model ID
    new_id = random.getrandbits(32)
    # Ensure ID is unique
    while str(new_id) in models:
        new_id = random.getrandbits(32)

    # create cimpy objects
    try:
        cimpy_data = cimpy.cim_import(files, new_model.version)
    except Exception:
        return Error(code=422, message="Invalid CIM files"), 422

    models[str(new_id)] = record(new_model, cimpy_data)

    # Return the model as `ModelReply`
    return ModelReply.from_model(new_model, new_id)


def delete_element(id, elem_id):
    """Delete element of model


    :param id: model id
    :type id: int
    :param elem_id: element id
    :type elem_id: int

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
        model_reply = ModelReply.from_model(models[str(id_)].model, id_)
        del models[str(id_)]
        return model_reply
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
    global models

    if str(id_) in models:
        # TODO: Which Profiles? Profile in Request?
        return cimpy.generate_xml(models[str(id_)].cimobj,
                                  'cgmes_v2_4_15',
                                  cimpy.cgmes_v2_4_15.Base.Profile['EQ'],
                                  ['DI', 'EQ', 'SV', 'TP'])
    else:
        return Error(code=404, message="No models in to database"), 404


def get_element(id, elem_id):
    """Get element of model

    :param id: Model id
    :type id: int
    :param elem_id: Element id
    :type elem_id: int

    :rtype: ModelElementAttributes
    """
    raise Exception('Unimplemented')


def get_elements(id):
    """Get all elements of a model


    :param id: Model id
    :type id: int

    :rtype: List[ModelElement]
    """
    raise Exception('Unimplemented')


def get_model(id_):
    """Get a network model
    This is only useful at the moment to get the name of the model

    :param id: Model id
    :type id: int

    :rtype: Model
    """
    global models
    try:
        return ModelReply.from_model(models[str(id_)].model, id_)
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


def update_element(id, elem_id, model_element_update):  # noqa: E501
    """Update element of model


    :param id: model id
    :type id: int
    :param elem_id: element id
    :type elem_id: int
    :param model_element_update: Model Element attributes to be updated
    :type model_element_update: dict | bytes

    :rtype: ModelElement
    """
    # if connexion.request.is_json:
    #     model_element_update = ModelElementUpdate.from_dict(
    #         connexion.request.get_json())
    raise Exception('Unimplemented')


def update_model(id):  # noqa: E501
    """Update a network model


    :param id: Model id
    :type id: int


    :rtype: Model
    """
    # if connexion.request.is_json:
    # model_update = ModelUpdate.from_dict(connexion.request.get_json())
    raise Exception('Unimplemented')


def apikey_auth(apikey, required_scopes=None):
    if apikey == '123':
        return {'sub': 'admin'}

    # optional: raise exception for custom error response
    return None
