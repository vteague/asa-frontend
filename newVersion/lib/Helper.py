import json
from flask import Response


def responseJson(succ=True, data=None, code='', message=""):
    """
    Respond to Json data
    """
    result = {
        'succ': succ,
        'data': data,
        'code': code,
        'message': message
    }
    return Response(json.dumps(result), mimetype='application/json')