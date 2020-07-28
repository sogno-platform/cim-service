
def add_model(new_model):  # noqa: E501
    """Add a network model

     # noqa: E501

    :param new_model: Network model to be added
    :type new_model: dict | bytes

    :rtype: Model
    """
    if connexion.request.is_json:
        new_model = NewModel.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'



def get_models():  # noqa: E501
    """Get all network models

    :rtype: str
    """
    return 'do some magic!'


def add_element(modelid, new_model_element):
    """Add element to model

    :param modelid: Model id
    :type modelid: int
    :param new_model_element: Element to be added to model
    :type new_model_element: dict | bytes

    :rtype: ModelElement
    """
    if connexion.request.is_json:
        new_model_element = NewModelElement.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_element(modelid, id_):
    """Delete element of model


    :param modelid: model id
    :type modelid: int
    :param id: element id
    :type id: int

    :rtype: ModelElement
    """
    return 'do some magic!'


def delete_model(id_):
    """Delete a network model

    :param id: Model id
    :type id: int

    :rtype: Model
    """
    return 'do some magic!'


def export_model(id_):
    """Export model to file

    Returns an archive containing the grid data in CIM formatted files and
    profile files that might have been imported previously.

    :param id: Model id
    :type id: int

    :rtype: file
    """
    return 'do some magic!'


def get_element(modelid, id_):
    """Get element of model

    :param modelid: Model id
    :type modelid: int
    :param id: Element id
    :type id: int

    :rtype: ModelElementAttributes
    """
    return 'do some magic!'


def get_elements(modelid_):
    """Get all elements of a model


    :param modelid: Model id
    :type modelid: int

    :rtype: List[ModelElement]
    """
    return 'do some magic!'


def get_model(id_):
    """Get a network model


    :param id: Model id
    :type id: int

    :rtype: Model
    """
    print("== Model ID", id_)
    return 'do some magic!'


def get_model_image(id_):
    """Render and return image of network model

    Returns an SVG image of the network based on CIM information. # noqa: E501

    :param id: Model id
    :type id: int

    :rtype: file
    """
    return 'do some magic!'


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
    return 'do some magic!'


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
    return 'do some magic!'


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
    return 'do some magic!'


def apikey_auth(apikey, required_scopes=None):
    if apikey == '123':
        return {'sub': 'admin'}

    # optional: raise exception for custom error response
    return None
