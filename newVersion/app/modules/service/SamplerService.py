from collections import defaultdict

from pandas import read_csv

from app.modules import modules
from flask import current_app

from app.modules.repositorys.JobRepository import JobRepository
from app.modules.repositorys.SamplerRepository import SamplerRepository


class SamplerService:
    """
    Used to display the Sampler data page
    Provide getInfo method for detailed data as well as paginating
    Provide save method for user to save the modified data for each page
    """
    def getInfo(self, page, jobId):
        """
         Loading Sampler data
         1. First import the csv file for candidates and parties in 2016
         2. Get the chosen Sampler information for the job
         3. According to the state of current data to obtain the parties and candidates of the state
         4. Get the data length for the preferences field according to the number of parties, for example, if there are three parties, we can get the preferences index between 0 and 2
         5. Then the remaining data is split and obtained in the order of the parties, and one party needs to be completed before obtain the data of the next party.
         6. Finally, gathering the result to what the page requires

        :param page: page number
        :param jobId: sampler job_id
        """
        templateSrc = '{0}/app/data/original/template.csv'.format(current_app.config.get('PROJECT_DIR'))
        template = read_csv(templateSrc)  # Loading each state to display the data in a paper ballot style
        samplerPage = SamplerRepository().getList(page, {'job_id': jobId}, 1)  # use job_id to read modified data in a paginate way
        if samplerPage.items[0].preferences_after_audit is None:
            preferences = samplerPage.items[0].preferences.split(',')
        else:
            preferences = samplerPage.items[0].preferences_after_audit.split(',')
        job = JobRepository().findById(jobId)
        if job is None:
            raise BaseException('Job does not exist')
        select = template[template['StateAb'] == job.state].fillna(value='-')  # Filter the data according to the state of the data
        groupby = select.groupby('Ticket')
        above = {
            'header': [],
            'body': []
        }  # Party table
        below = defaultdict(dict)  # Candidate table
        belowIndex = len(groupby.groups) - 1  # According to the total length of the party’s preference data, obtain the initial index of the candidate’s preference data
        lenBelow = 0
        for index, item in enumerate(groupby.groups):  # Using group to initialize Party and Party table
            parryName = select[(select['Ticket'] == item) & (select['BallotPosition'] != 0)].values[0][5]  # Get party name

            if item != 'UG':
                above['header'].append({'name': item, 'parry': parryName})
                above['body'].append({"value": preferences[index], 'dataIndex': index})
                lenParry = len(select[(select['Ticket'] == item) & (select['BallotPosition'] != 0)].values)
                lenBelow = lenBelow if lenBelow > lenParry else lenParry

            else:  # special treatment for people without a group
                lenParry = len(select[(select['Ticket'] == item) & (
                    select['BallotPosition'] != 0)].values)
                lenBelow = lenBelow if lenBelow > lenParry else lenParry
                parryName = 'UG'
                header = {'name': 'UG', 'parry': 'UG'}
                if header not in above['header']:
                    above['header'].append(header)
                    above['body'].append(
                        {"value": -1,
                         'dataIndex': index})  # The people with no groups is set to default that have no preference for the UG party

            below[parryName] = []
            dataIndex = 0
            for bIndex, bitem in enumerate(  # Get the candidate data
                    select[(select['Ticket'] == item) & (select['BallotPosition'] != 0)].values):
                dataIndex = belowIndex + bIndex + index
                bpreferences = ""
                if len(preferences) > dataIndex:
                    bpreferences = preferences[dataIndex]
                model = {'name': bitem[4], 'preferences': bpreferences, 'dataIndex': dataIndex}
                below[parryName].append(model)
            belowIndex = belowIndex + len(
                select[(select['Ticket'] == item) & (select['BallotPosition'] != 0)].values) - 1

        above['header'].sort(key=lambda x: len(x['name']))  # Sort by length

        return {'above': above, 'below': {'data': below, 'number': lenBelow}, 'sampler': samplerPage, 'jobId': jobId}

    def save(self, id, preferences):
        """
        Save the modified data by user
        """
        model = SamplerRepository().findById(id)
        if model is None:
            raise BaseException('Sampler data does not exist.')
        model.preferences_after_audit = ','.join(preferences)
        return SamplerRepository().update(model)
