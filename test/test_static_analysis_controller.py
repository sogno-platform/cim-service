# coding: utf-8

from __future__ import absolute_import
import unittest

# from models.analysis_response import AnalysisResponse  # noqa: E501
from test.basetestcase import BaseTestCase


class TestStaticAnalysisController(BaseTestCase):
    """StaticAnalysisController integration test stubs"""

    @unittest.skip("multipart/form-data not supported by Connexion")
    def test_dpsimadapter_add_analysis(self):
        """Test case for dpsimadapter_add_analysis

        Add a new analysis
        """
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'multipart/form-data',
        }
        response = self.client.open(
            '/analysis',
            method='POST',
            headers=headers,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_dpsimadapter_delete_analysis(self):
        """Test case for dpsimadapter_delete_analysis

        Delete specific analysis including results
        """
        headers = {
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/analysis/{id}'.format(id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_dpsimadapter_get_all_analysis(self):
        """Test case for dpsimadapter_get_all_analysis

        Get all network models
        """
        headers = {
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/analysis',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_dpsimadapter_get_analysis(self):
        """Test case for dpsimadapter_get_analysis

        Get specific analysis status and results
        """
        headers = {
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/analysis/{id}'.format(id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
