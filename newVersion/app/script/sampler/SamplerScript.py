import json

from flask import request, render_template

from app.modules.service.SamplerService import SamplerService
from app.script import script
from lib.Helper import responseJson


@script.route('/info', methods=['GET'])
def getInfo():
    """
    Sampling data information
    using job_id to inquire single data
    :return:
    """
    page = int(request.args.get('page', 1))
    jobId = int(request.args.get('job_id', 1))
    if jobId is None:
        return responseJson(False, message='job_id cannot be empty!')
    result = SamplerService().getInfo(page, jobId)
    return render_template('table/info.html', data=result)


@script.route('/info', methods=['POST'])
def saveInfo():
    """
    Modify sampling data
    :return:
    """
    data = json.loads(request.get_data())
    result = SamplerService().save(data['id'], data['preferences'])
    if result is not None:
        return responseJson(False, message='job_id cannot be empty!')
    return responseJson(True, data=data, message='Success')
