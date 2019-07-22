import json
from flask import jsonify
import logging
import pandas as pd
import pickle
import dill

from src import AppResponse

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)


model_folder = 'src/ml_model_api/models/defaults_prediction_v1/'
loaded_pipe_preprocess = pickle.load(open(model_folder+'pipe_preprocess.pkl', 'rb'))
loaded_pipe_imputeScale = pickle.load(open(model_folder+'pipe_imputeScale.pkl', 'rb'))
loaded_model_xgb = pickle.load(open(model_folder+'model_xgb.pkl', 'rb'))
loaded_lime_explainer = dill.load(open(model_folder+'lime_explainer', 'rb'))

def defaults_handler(request):
    """
    Function to predict the probability of default using ML models
    :return: Response object containing decision, probability and interpretation
    """
    body = json.loads(request.data)
    df_raw_tmp = pd.read_json(body['input'], orient='index')

    df_tm_1 = loaded_pipe_preprocess.transform(df_raw_tmp)
    df_tm_2 = pd.DataFrame(loaded_pipe_imputeScale.transform(df_tm_1), columns=df_tm_1.columns)
    y_xgb = loaded_model_xgb.predict_proba(df_tm_2)

    # Prediction functions for LIME explanations
    predict_fn_xgb = lambda x: loaded_model_xgb.predict_proba(
        pd.DataFrame(loaded_pipe_imputeScale.transform(x), columns=df_tm_2.columns.values))

    y_prob = y_xgb[0][1]
    exp_list = loaded_lime_explainer.explain_instance(df_tm_2.loc[0], predict_fn_xgb).as_list()

    # Decision - set threshold values here
    thres_low = 0.35
    thres_high = 0.8
    if y_prob < thres_low:
        decision = "approve"
    elif y_prob > thres_high:
        decision = "decline"
    else:
        decision = "manual"

    predicted = {"decision": decision, "probability": str(y_prob),
                 "interpretation": exp_list}

    return AppResponse.success_response(status=200, data=jsonify(predicted))


