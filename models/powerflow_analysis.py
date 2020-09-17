# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.analysis import Analysis
from openapi_server.models.any_type import AnyType
from openapi_server.models.powerflow_analysis_all_of import PowerflowAnalysisAllOf
from openapi_server import util

from openapi_server.models.analysis import Analysis  # noqa: E501
from openapi_server.models.any_type import AnyType  # noqa: E501
from openapi_server.models.powerflow_analysis_all_of import PowerflowAnalysisAllOf  # noqa: E501

class PowerflowAnalysis(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, name=None, type=None, modelid=None, param=None):  # noqa: E501
        """PowerflowAnalysis - a model defined in OpenAPI

        :param name: The name of this PowerflowAnalysis.  # noqa: E501
        :type name: str
        :param type: The type of this PowerflowAnalysis.  # noqa: E501
        :type type: str
        :param modelid: The modelid of this PowerflowAnalysis.  # noqa: E501
        :type modelid: int
        :param param: The param of this PowerflowAnalysis.  # noqa: E501
        :type param: Dict[str, AnyType]
        """
        self.openapi_types = {
            'name': str,
            'type': str,
            'modelid': int,
            'param': Dict[str, AnyType]
        }

        self.attribute_map = {
            'name': 'name',
            'type': 'type',
            'modelid': 'modelid',
            'param': 'param'
        }

        self._name = name
        self._type = type
        self._modelid = modelid
        self._param = param

    @classmethod
    def from_dict(cls, dikt) -> 'PowerflowAnalysis':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PowerflowAnalysis of this PowerflowAnalysis.  # noqa: E501
        :rtype: PowerflowAnalysis
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self):
        """Gets the name of this PowerflowAnalysis.

        Name of analysis case  # noqa: E501

        :return: The name of this PowerflowAnalysis.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PowerflowAnalysis.

        Name of analysis case  # noqa: E501

        :param name: The name of this PowerflowAnalysis.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def type(self):
        """Gets the type of this PowerflowAnalysis.

        Type of analysis, e.g. PowerflowAnalysis  # noqa: E501

        :return: The type of this PowerflowAnalysis.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this PowerflowAnalysis.

        Type of analysis, e.g. PowerflowAnalysis  # noqa: E501

        :param type: The type of this PowerflowAnalysis.
        :type type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def modelid(self):
        """Gets the modelid of this PowerflowAnalysis.

        Model to consider for analysis  # noqa: E501

        :return: The modelid of this PowerflowAnalysis.
        :rtype: int
        """
        return self._modelid

    @modelid.setter
    def modelid(self, modelid):
        """Sets the modelid of this PowerflowAnalysis.

        Model to consider for analysis  # noqa: E501

        :param modelid: The modelid of this PowerflowAnalysis.
        :type modelid: int
        """
        if modelid is None:
            raise ValueError("Invalid value for `modelid`, must not be `None`")  # noqa: E501

        self._modelid = modelid

    @property
    def param(self):
        """Gets the param of this PowerflowAnalysis.

        attribute map, e.g. strings and numbers to define solver settings etc.  # noqa: E501

        :return: The param of this PowerflowAnalysis.
        :rtype: Dict[str, AnyType]
        """
        return self._param

    @param.setter
    def param(self, param):
        """Sets the param of this PowerflowAnalysis.

        attribute map, e.g. strings and numbers to define solver settings etc.  # noqa: E501

        :param param: The param of this PowerflowAnalysis.
        :type param: Dict[str, AnyType]
        """

        self._param = param