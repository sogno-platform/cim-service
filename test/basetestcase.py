import logging

import connexion
from flask_testing import TestCase

#  from ...server import create_server
from encoder import JSONEncoder


class BaseTestCase(TestCase):

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        #  return create_server()
        app = connexion.App(__name__, specification_dir='../')
        app.app.json_encoder = JSONEncoder
        app.add_api('cimpy_api.yaml', pythonic_params=True)
        return app.app
