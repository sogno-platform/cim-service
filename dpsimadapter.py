import connexion
import six

from models.analysis_response import AnalysisResponse  # noqa: E501
from models.error import Error  # noqa: E501
import util


def add_analysis():  # noqa: E501
    """Add a new analysis

     # noqa: E501


    :rtype: AnalysisResponse
    """
    return 'do some magic!'


def delete_analysis(id):  # noqa: E501
    """Delete specific analysis including results

     # noqa: E501

    :param id: Analysis id
    :type id: int

    :rtype: AnalysisResponse
    """
    return 'do some magic!'


def get_all_analysis():  # noqa: E501
    """Get all network models

     # noqa: E501


    :rtype: List[AnalysisResponse]
    """
    return 'do some magic!'


def get_analysis(id):  # noqa: E501
    """Get specific analysis status and results

     # noqa: E501

    :param id: Analysis id
    :type id: int

    :rtype: AnalysisResponse
    """
    return 'do some magic!'
