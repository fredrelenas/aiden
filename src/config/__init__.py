from flask.json import JSONEncoder
from decimal import Decimal


class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)