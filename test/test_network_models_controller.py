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
            '/models/{modelid}/elements'.format(modelid=56),
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
        cim_xml = open(
            "test/sampledata/CIGRE_MV/Rootnet_FULL_NE_24J13h_DI.xml", "rb")
        modelname = "test_rootnet_full_ne_24j13h_di"
        response = self.client.open(
            '/models',
            method='POST',
            data={'name': modelname, 'files': cim_xml},
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        returned_model = Model.from_dict(json.loads(response.get_data()))
        assert returned_model.name == modelname
        assert isinstance(returned_model.id, int)

    def test_add_models(self):
        """Test case for add_model

        Add a network model
        """
        cim_xml = [
            open("test/sampledata/CIGRE_MV/Rootnet_FULL_NE_24J13h_DI.xml",
                 "rb"),
            open("test/sampledata/CIGRE_MV/Rootnet_FULL_NE_24J13h_EQ.xml",
                 "rb"),
            open("test/sampledata/CIGRE_MV/Rootnet_FULL_NE_24J13h_SV.xml",
                 "rb"),
            open("test/sampledata/CIGRE_MV/Rootnet_FULL_NE_24J13h_TP.xml",
                 "rb")
        ]
        modelname = "test_rootnet_full_ne_24j13h"
        response = self.client.open(
            '/models',
            method='POST',
            data={'name': modelname, 'files': cim_xml},
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        returned_model = Model.from_dict(json.loads(response.get_data()))
        assert returned_model.name == modelname
        assert isinstance(returned_model.id, int)

    def test_add_model_faulty(self):
        """Test case for add_model

        Post faulty requests and expect error responses
        """
        response = self.client.open(
            '/models',
            method='POST',
            data={'name': 'no_file'},
            content_type='multipart/form-data')
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        cim_xml = open("test/sampledata/Broken_CIM.xml", "rb")
        response = self.client.open(
            '/models',
            method='POST',
            data={'name': "broken_xml", 'file': cim_xml},
            content_type='multipart/form-data')
        print(self.assert400(response,
                             'Response body is : ' + response.data.decode('utf-8')))

        cim_xml = [
            open("test/sampledata/testfile1.txt", "rb"),
            open("test/sampledata/testfile2.txt", "rb")
        ]
        modelname = "test_rootnet_full_ne_24j13h"
        response = self.client.open(
            '/models',
            method='POST',
            data={'name': modelname, 'files': cim_xml},
            content_type='multipart/form-data')
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_and_get_model(self):
        """Test case for add_model

        Add a network model and then get it back by id. Must be the same data
        """
        cim_xml = open(
            "test/sampledata/CIGRE_MV/Rootnet_FULL_NE_24J13h_DI.xml", "rb")
        modelname = "test_rootnet_full_ne_24j13h_di"
        post_response = self.client.open(
            '/models',
            method='POST',
            data={'name': modelname, 'file': cim_xml},
            content_type='multipart/form-data')
        self.assert200(post_response,
                       'Response is : ' + post_response.data.decode('utf-8'))
        post_response_json = Model.from_dict(
            json.loads(post_response.get_data()))

        # Check if model is avail
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        get_response = self.client.open(
            '/models/{id}'.format(id=post_response_json.id),
            method='GET',
            headers=headers)
        self.assert200(get_response,
                       'Response is : ' + get_response.data.decode('utf-8'))
        get_response_json = Model.from_dict(
            json.loads(get_response.get_data()))
        assert get_response_json == post_response_json

    def test_delete_element(self):
        """Test case for delete_element

        Delete element of model
        """
        headers = {
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/models/{modelid}/elements/{id}'.format(
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
            '/models/{id}'.format(id=56),
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
            '/models/export/{id}'.format(id=56),
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
            '/models/{modelid}/elements/{id}'.format(
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
            '/models/{modelid}/elements'.format(modelid=56),
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
            '/models/{id}'.format(id=56),
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
            '/models/image/{id}'.format(id=56),
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
            '/models',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

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
            '/models/import/{id}'.format(id=56),
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
            '/models/{modelid}/elements/{id}'.format(
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
            '/models/{id}'.format(id=56),
            method='PUT',
            headers=headers,
            data=json.dumps(model_update),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
