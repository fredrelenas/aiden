from flask import make_response

class AppResponse(object):
    """The parent class to provide responses"""

    @staticmethod
    def success_response(status=200, data='', headers=None):
        if headers and 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'
            headers['Cache-Control'] = 'no-store'
        return make_response(data, status, headers)