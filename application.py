import logging
import sys
import os
here = os.path.dirname(os.path.realpath(__file__))
site_pkgs = os.path.join(
    here,
    "penv",
    "lib",
    "python3.6",
    "site-packages")
for p in [site_pkgs, here]:
    sys.path.append(p)
from src.config.application import create_app, swagger_template
from flask import Blueprint, request
from flasgger import Swagger, NO_SANITIZER

# Model specific imports
from src.ml_model_api.models.defaults_prediction_v1 import DefaultsModelPreProcessing
from src.ml_model_api.models.manual_approval_prediction_v1 import ManualApprovalModelPreProcessing

logger = logging.getLogger(__name__)
logging.basicConfig(level=(os.environ.get('LOG_LEVEL') or "INFO"))

# Application Configuration
api_blueprint = Blueprint('api', __name__)
configuration_name = os.getenv('APP_SETTINGS')
ai_engine, url_prefix = create_app(configuration_name)

swagger_template = swagger_template(configuration_name)
swagger = Swagger(ai_engine, sanitizer=NO_SANITIZER, template=swagger_template)

with ai_engine.test_request_context():
    print(request.environ)

from src.ml_model_api.routes.routes import home_api
from src.ml_model_api.routes.routes import default_prediction_api
from src.ml_model_api.routes.routes import manual_approval_prediction_api

# Blueprint configuration
ai_engine.register_blueprint(home_api)
ai_engine.register_blueprint(default_prediction_api,  url_prefix=url_prefix)
ai_engine.register_blueprint(manual_approval_prediction_api,  url_prefix=url_prefix)

if __name__ == '__main__':
    # Local host on port 5001
    ai_engine.run(debug=ai_engine.config["DEBUG"], host=os.getenv("HOST"), port=int(os.getenv("PORT")))
