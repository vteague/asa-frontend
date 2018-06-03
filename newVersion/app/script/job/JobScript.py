from flask import request, session, render_template

from app.models.jobs.Job import Job
from app.modules.repositorys.JobRepository import JobRepository
from app.modules.service.ASARunnerService import ASARunnerService
from app.modules.service.UserManage import UserManage
from app.script import script
from lib.Helper import responseJson
from app.exceptions.BaseException import BaseException

__prefix = 'job'


@script.route('audit', methods=['GET'])
def audit():
    """
    Audit Job Page
    """
    page = int(request.args.get('page', 1))
    data = JobRepository().getList(page, {'job_type': 'audit'})
    return render_template('table/audit.html', data=data)


@script.route('sampler')
def sampler():
    """
    Sample Job Page
    """
    page = int(request.args.get('page', 1))
    data = JobRepository().getList(page, {'job_type': 'sampler'})
    return render_template('table/sampler.html', data=data)


@script.route('addAudit', methods=['GET'])
def addAudit():
    """
    New Audit Job
    """
    jobId = int(request.args.get('job_id'))
    if jobId is None:
        raise BaseException('Job Id cannot be empty!')
    job = JobRepository().findById(jobId)
    if job is None:
        raise BaseException('Job does not exist!')
    return render_template('table/addAudit.html', job=job)


@script.route('addAudit', methods=['POST'])
def saveAudit():
    """
    Save audit
    """
    jobName = request.form['jobName']
    if jobName is None:
        return responseJson(succ=False, message='Job Name cannot be empty!')

    state = request.form['state']
    if state is None:
        return responseJson(False, message='State cannot be empty!')

    seed = request.form['seed']
    if seed is None:
        return responseJson(False, message='Seed cannot be empty!')

    increment = request.form['increment']
    if increment is None:
        return responseJson(False, message='Increment cannot be empty!')

    jobId = request.form['jobId']
    if jobId is None:
        return responseJson(False, message='Job Id cannot be empty!')

    user = UserManage.getCurrent()
    result = ASARunnerService().runAudit(jobId, user.user_id, jobName, state, int(seed), int(increment))
    if result is None:
        return responseJson(True, message='Success')
    return responseJson(False, message='Failed to extract data')


@script.route('addSampler', methods=['GET'])
def addSampler():
    """
    Sampling page
    """
    return render_template('table/addSampler.html')


@script.route('addSampler', methods=['POST'])
def saveSampler():
    """
    Add Sample Job
    """
    jobName = request.form['jobName']
    if jobName is None:
        return responseJson(succ=False, message='Job Name cannot be empty!')

    state = request.form['state']
    if state is None:
        return responseJson(False, message='State cannot be empty!')

    seed = request.form['seed']
    if seed is None:
        return responseJson(False, message='Seed cannot be empty!')

    increment = request.form['increment']
    if increment is None:
        return responseJson(False, message='Increment cannot be empty!')

    user = UserManage.getCurrent()
    result = ASARunnerService().runSampler(user.user_id, jobName, state, int(seed), int(increment))
    if result is None:
        return responseJson(True, message='Success')
    return responseJson(False, message='Failed to extract data')

