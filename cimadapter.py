import json
from types import SimpleNamespace
import cimpy
import connexion
from models import Error
from models import Model
from models import ModelReply

# from models import ModelElementUpdate
# from models import ModelUpdate
# from models import NewModelElement
#  import pdb
from xml.etree import ElementTree
import model_db


def add_element(id_):
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
    raise Exception("Unimplemented")


def add_model():
    """Add a new network model"""

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

    # create cimpy objects
    try:
        cimpy_data = cimpy.cim_import(files, new_model.version)
    except Exception:
        return Error(code=422, message="Invalid CIM files"), 422

    new_id = model_db.put_model(new_model, cimpy_data, files)

    # Return the model as `ModelReply`
    return ModelReply.from_model(new_model, new_id)


def delete_element(id_, elem_id):
    """Delete element of model


    :param id: model id
    :type id: int
    :param elem_id: element id
    :type elem_id: int

    :rtype: ModelElement
    """
    raise Exception("Unimplemented")


def delete_model(id_):
    """Delete a network model

    :param id: Model id
    :type id: int

    :rtype: Model
    """
    return model_db.delete_model(id_)


def export_model(id_):
    """Export model to file

    Returns an archive containing the grid data in CIM formatted files and
    profile files that might have been imported previously.

    :param id: Model id
    :type id: int

    :rtype: file
    """
    model_record = model_db.get_model(id_)

    if isinstance(model_record, model_db.record):
        model_files = model_record.files
        # TODO: Which Profiles? Profile in Request?
        return cimpy.cimexport.generate_xml(
            model.cimobj,
            "cgmes_v2_4_15",
            cimpy.cgmes_v2_4_15.Base.Profile["EQ"],
            ["DI", "EQ", "SV", "TP"],
        )
    else:
        return (
            Error(
                code=404, message="No model with id: " + str(id_) + " found in database"
            ),
            404,
        )


def get_element(id_, elem_id):
    """Get element of model

    :param id: Model id
    :type id: int
    :param elem_id: Element id
    :type elem_id: int

    :rtype: ModelElementAttributes
    """
    raise Exception("Unimplemented")


def get_elements(id_):
    """Get all elements of a model


    :param id: Model id
    :type id: int

    :rtype: List[ModelElement]
    """
    raise Exception("Unimplemented")


def get_model(id_):
    """Get a network model
    This is only useful at the moment to get the name of the model

    :param id: Model id
    :type id: int

    :rtype: Model
    """
    try:
        record = model_db.get_record(id_)
        # Temporary Hack: manipulate the stored json so that it can be deserialized into a model again
        model_str = record.model.replace("\n", "").replace("'", '"')
        model = json.loads(model_str, object_hook=lambda d: SimpleNamespace(**d))
        return ModelReply.from_model(model, id_)
    except KeyError:
        return Error(code=404, message="Model not found"), 404


def get_models():
    """Get a list of all network models

    :rtype: dict
    """
    return model_db.get_models()


def update_element(id_, elem_id, model_element_update):  # noqa: E501
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
    raise Exception("Unimplemented")


def update_model(id_):  # noqa: E501
    """Update a network model


    :param id: Model id
    :type id: int


    :rtype: Model
    """
    # if connexion.request.is_json:
    # model_update = ModelUpdate.from_dict(connexion.request.get_json())
    raise Exception("Unimplemented")


def apikey_auth(apikey, required_scopes=None):
    if apikey == "123":
        return {"sub": "admin"}

    # optional: raise exception for custom error response
    return None
