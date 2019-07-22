import os
import requests
import json
import pandas as pd

def headers():
    return {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
    }

class get_data():

    def __init__(self):
        self.test_data_folder = "./test_data/"

    def default_prediction(self):
        df = pd.read_csv(self.test_data_folder+'default_prediction_test1.csv')
        df_json = df.to_json(orient='index', force_ascii=False)
        data = {
            "input": df_json,
            "end_point": "default_prediction"
        }
        return data

    def manual_approval_prediction(self):
        df = pd.read_csv(self.test_data_folder+'manual_approval_prediction_test1.csv')
        df_json = df.to_json(orient='index', force_ascii=False)
        data = {
            "input": df_json,
            "end_point": "manual_approval_prediction"
        }
        return data

def test_fulfillment(data, ai_service_url):
    body = json.dumps(data)
    #print(body)
    url = "%s/%s" % (ai_service_url, data['end_point'])
    response = requests.request('POST', url, data=body, headers=headers())
    print('\n Fulfillment response for endpoint', data['end_point'], response.status_code)
    """
    Response 500 => invalid "data"; change the keys/values in the data dictionary above
    Response 404 => endpoint is wrong
    """
    try:
        fulfilment_response = json.loads(response.text)
        print(fulfilment_response)
    except ValueError:
        pass

if __name__ == '__main__':

    ai_service_url = os.environ.get('AI_SERVICE_URL')
    method_list = [func for func in dir(get_data) if not func.startswith("__")]

    # copy the body (from above, after json.dumps()..) between '' in the below line
    # curl -d 'BODY' -H "Content-Type: application/json" -X POST http://localhost:5001/aiden/v1/default_prediction

    for func in method_list:
        # getattr(x, func) is equivalent to x.func
        data = getattr(get_data(),func)()
        test_fulfillment(data, ai_service_url)