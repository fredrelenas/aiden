import yaml
from flask import Blueprint, request
from flasgger import swag_from

from src.ml_model_api.handlers.default_prediction import defaults_handler
from src.ml_model_api.handlers.manual_approval_prediction import manual_approval_handler

home_api = Blueprint('home_api', __name__)
@home_api.route('/', endpoint='get_home', methods=['GET'])
def get_home():
    print('Successfully connected to AI engine')
    return 'Successfully connected to AI engine'


default_prediction_api = Blueprint('default_prediction_api', __name__)
@swag_from(yaml.load(open('src/ml_model_api/specs/default_prediction.yml', 'r')))
@default_prediction_api.route('/default_prediction',
                              endpoint='get_default_prediction', methods=['POST'])
def get_default_prediction():
    return defaults_handler(request)


manual_approval_prediction_api = Blueprint('manual_approval_prediction_api', __name__)
@swag_from(yaml.load(open('src/ml_model_api/specs/manual_approval_prediction.yml', 'r')))
@manual_approval_prediction_api.route('/manual_approval_prediction',
                                      endpoint='get_manual_approval_prediction', methods=['POST'])
def get_manual_approval_prediction():
    return manual_approval_handler(request)
