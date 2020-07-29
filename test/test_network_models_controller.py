# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from models.error import Error  # noqa: E501
from models.model import Model  # noqa: E501
from models.model_element import ModelElement  # noqa: E501
from models.model_element_attributes import ModelElementAttributes  # noqa: E501
from models.model_element_update import ModelElementUpdate  # noqa: E501
from models.model_update import ModelUpdate  # noqa: E501
from models.new_model import NewModel  # noqa: E501
from models.new_model_element import NewModelElement  # noqa: E501
from test.basetestcase import BaseTestCase


class TestNetworkModelsController(BaseTestCase):
    """NetworkModelsController integration test stubs"""

    def test_add_element(self):
        """Test case for add_element

        Add element to model
        """
        new_model_element = {
            "param": {
                "key": ""
            },
            "name": "name",
            "type": "type"
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/CIM/0.0.1/models/{modelid}/elements'.format(modelid=56),
            method='POST',
            headers=headers,
            data=json.dumps(new_model_element),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_model(self):
        """Test case for add_model

        Add a network model
        """
        new_model = {
            "name": "name"
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/CIM/0.0.1/models',
            method='POST',
            headers=headers,
            data=json.dumps(new_model),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_element(self):
        """Test case for delete_element

        Delete element of model
        """
        headers = {
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/CIM/0.0.1/models/{modelid}/elements/{id}'.format(
                modelid=56, id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_model(self):
        """Test case for delete_model

        Delete a network model
        """
        headers = {
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/CIM/0.0.1/models/{id}'.format(id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_export_model(self):
        """Test case for export_model

        Export model to file
        """
        headers = {
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/CIM/0.0.1/models/export/{id}'.format(id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_element(self):
        """Test case for get_element

        Get element of model
        """
        headers = {
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/CIM/0.0.1/models/{modelid}/elements/{id}'.format(
                modelid=56, id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_elements(self):
        """Test case for get_elements

        Get all elements of a model
        """
        headers = {
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/CIM/0.0.1/models/{modelid}/elements'.format(modelid=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_model(self):
        """Test case for get_model

        Get a network model
        """
        headers = {
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/CIM/0.0.1/models/{id}'.format(id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_model_image(self):
        """Test case for get_model_image

        Render and return image of network model
        """
        headers = {
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/CIM/0.0.1/models/image/{id}'.format(id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_models(self):
        """Test case for get_models

        Get all network models
        """
        headers = {
            'Accept': 'text/plain',
        }
        response = self.client.open(
            '/CIM/0.0.1/models',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("Connexion does not support multiple consummes. See https://github.com/zalando/connexion/pull/760")
    def test_import_model(self):
        """Test case for import_model

        Import model from file
        """
        body = (BytesIO(b'some file data'), 'file.txt')
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/octet-stream',
        }
        response = self.client.open(
            '/CIM/0.0.1/models/import/{id}'.format(id=56),
            method='POST',
            headers=headers,
            data=json.dumps(body),
            content_type='application/octet-stream')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_element(self):
        """Test case for update_element

        Update element of model
        """
        model_element_update = {
            "param": {
                "key": ""
            },
            "name": "name",
            "type": "type"
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/CIM/0.0.1/models/{modelid}/elements/{id}'.format(
                modelid=56, id=56),
            method='PUT',
            headers=headers,
            data=json.dumps(model_element_update),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_model(self):
        """Test case for update_model

        Update a network model
        """
        model_update = {
            "name": "name"
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/CIM/0.0.1/models/{id}'.format(id=56),
            method='PUT',
            headers=headers,
            data=json.dumps(model_update),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
