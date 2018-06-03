import os

from flask import url_for, current_app
from sqlalchemy import and_

from app.models.jobs.Job import Job
from app.modules.RepositoryBase import RepositoryBase


class JobRepository(RepositoryBase):
    def targetModelClass(self):
        return Job

    def getList(self, page=1, conditions={}, pageSize=10):
        """
        Returning the result list
        Using the primary key to get the path for the download file
        adding isDownload to identify whether the download button is available
        using os.path.exist to judge if the file exists
        """
        ands = self.validateAndGetListConditions(conditions)
        result = self.model().paginate(page, pageSize, *ands)
        for item in result.items:
            path = '/static/data/audit_{0}.csv'.format(item.job_id)
            item.isDownload = os.path.exists(current_app.config.get('PROJECT_DIR') + "/app" + path)
            item.url = path
        return result

    def model(self):
        return Job()
