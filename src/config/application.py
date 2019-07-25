import os
import warnings
import operator
from flask import Flask
from .environments import app_config
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from . import MyJSONEncoder

ma = Marshmallow()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=False)
    CORS(app)

    app.config.from_object(app_config[config_name])
    app.json_encoder = MyJSONEncoder
    app.config.from_pyfile('environments.py')
    app.config['SWAGGER'] = {
                    'swagger_version': '2.0',
                    'title': 'AI Engine - %s' % swagger_env(),
                    'uiversion': 3,
                    "consumes": [
                        "application/json",
                    ],
                    "produces": [
                        "application/json",
                    ],
                    "specs": [
                        {
                            "endpoint": 'apispec_1',
                            "route": "/aiden/apispec_v1.json",
                            "rule_filter": lambda rule: True,  # all in
                            "model_filter": lambda tag: True,  # all in
                        }
                    ],
                    'headers': [
                        ('Access-Control-Allow-Origin', '*'),
                        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
                        ('Access-Control-Allow-Credentials', False),
                        ('Access-Control-Allow-Headers', 'Content-Type'),
                        ('Cache-Control', 'no-store'),
                        ('X-API-Version', app.config['API_VERSION_V1'])
                    ]
                }

    ma.init_app(app)

    print("REST_URL_PREFIX: %s" % app.config['REST_URL_PREFIX'])

    url_prefix = '{prefix}/v{version}'.format(prefix=app.config['REST_URL_PREFIX'],
                                              version=app.config['API_VERSION_V1'])

    from application import api_blueprint

    app.register_blueprint(
        api_blueprint,
        url_prefix=url_prefix
    )

    return app, url_prefix


def routes(app):
    'Display registered routes'
    rules = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        rules.append((rule.endpoint, methods, str(rule)))

    sort_by_rule = operator.itemgetter(2)
    for endpoint, methods, rule in sorted(rules, key=sort_by_rule):
        route = '{:50s} {:25s} {}'.format(endpoint, methods, rule)
        print(route)


def swagger_template(configuration_name):
    if configuration_name == "testing" or configuration_name == "development":
        return {
          "swagger": "2.0",
          "schemes": [
            "http"
          ],
          "host": "localhost:5001"
        }
    else:
        return {
          "swagger": "2.0",
          "schemes": [
            "https"
          ],
          "host": os.getenv('API_ENDPOINT')
        }


def swagger_env():
    if os.getenv('ENV'):
        return os.getenv('ENV').upper()
    else:
        return 'LOCAL'
