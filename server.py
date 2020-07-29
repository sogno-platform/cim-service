#!/usr/bin/env python3

import connexion
import encoder

from connexion.resolver import Resolver


def main():
    app = connexion.App(__name__, specification_dir='')
    app.app.json_encoder = encoder.JSONEncoder
    options = {"swagger_ui": True}

    app.add_api('cimpy_api.yaml',
                options=options,
                arguments={'title': 'ANM4L API'},
                resolver=Resolver(),
                pythonic_params=True)
    app.run(port=8080)


if __name__ == '__main__':
    main()
