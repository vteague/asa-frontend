from flask import current_app

from app.models.jobs.Job import Job
from app.models.sampler.Sampler import Sampler
from app.modules.repositorys.JobRepository import JobRepository
from app.modules.repositorys.SamplerRepository import SamplerRepository
from lib.ASARunner.AusSenateAudit import AusSenateAudit
import pandas as pd


class ASARunnerService:
    """
    Audit Core Services
     Mainly provides newly built sampling and audit job
     1. import data from Sampling CSV file
     2. After user's modification, the altered data is exported to CSV
     3. Run audit
    """
    DATA_DIR = '/app/data/original'  # Original data folder

    def runSampler(self, userId, jobName, state, seed, sampleIncrement, status='submitted'):
        """
         run sampling method
         Saving the used parameters input by user
         Execute the run_sampler method for data sampling
         run the data import function to import data into the database

        :param userId: user id
        :param jobName: job name
        :param seed: the start number for the random number generator
        :param sampleIncrement: the chosen size for number of selected ballots
        """
        job = Job(userId, jobName, 'sampler', state, seed, status, sampleIncrement)  # New job
        result = JobRepository().create(job)
        outputName = current_app.config.get('PROJECT_DIR') + '/app/data/sampler_{}'.format(result.job_id)  # Result output file
        if AusSenateAudit.run_sampler(state, current_app.config.get('PROJECT_DIR') + self.DATA_DIR, seed, sampleIncrement, outputName):  # checking the execution result
            return self.importSampler(result.job_id)
        return False

    def importSampler(self, jobId):
        """
         import data
         get the data file, save the data file as a copy of the original data file, use it for the following audit jobs for comparison.
        """
        csvPath = current_app.config.get('PROJECT_DIR') + '/app/data/sampler_{0}/rounds/round_1.csv'.format(jobId)   # CSV file path
        original = current_app.config.get('PROJECT_DIR') + '/app/data/sampler_{0}/selected_ballots.csv'.format(jobId)  # Source data path
        csv = pd.read_csv(csvPath)
        csv = csv[['ElectorateNm', 'VoteCollectionPointNm', 'VoteCollectionPointId', 'BatchNo', 'PaperNo', 'Preferences']]
        csv.to_csv(original, index=False)  # Generate the original data for merging manipulation by the lower level.
        return SamplerRepository().importSampler(csvPath, jobId)  # import data

    def runAudit(self, jobId, userId, jobName, state, seed, sampleIncrement):
        """
         Export audit data
         Extract the sampler data from the database according to jobId and export it as a CSV file.
         do the run method for audit
         Read the result and re-encapsulate the data that has zero value for match variable into a csv file for users to download.
        """
        job = JobRepository().findById(jobId)  # Get Job
        rounds = None
        ballots = None
        if job is None:
            raise BaseException("Job does not exist!")

        selectedBallots = current_app.config.get('PROJECT_DIR') + '/app/data/sampler_{}/selected_ballots.csv'.format(
            jobId)  # CSV file path for the altered sampling data
        outputFile = current_app.config.get('PROJECT_DIR') + '/app/data/sampler_{0}'.format(jobId)  # Result path
        try:
            self.exportSampler(jobId)  # Export the modification result of the selected job to csv file
            result = AusSenateAudit.run(state, data=current_app.config.get('PROJECT_DIR') + self.DATA_DIR, seed=seed, sample_increment=sampleIncrement, output_name=outputFile, selected_ballots=selectedBallots)  # Run audit
            ballots = result['sample_size']
            rounds = result['audit_stage']
            status = 'completed'
        except Exception:
            status = 'ERROR'

        job = Job(userId, jobName, 'audit', state, seed, status, sampleIncrement, rounds, ballots, jobId)
        jobResult = JobRepository().create(job)
        result = pd.read_csv("{}/rounds/round_1.csv".format(outputFile))
        match = result[result['Match'] == 0]  # Get the results that is not match
        if len(match.values) > 0:
            match.to_csv(current_app.config.get('PROJECT_DIR') + '/app/static/data/audit_{0}.csv'.format(jobResult.job_id), index=False)  # Export the results that is not match
        return jobResult

    def exportSampler(self, jobId):
        """
         Export the modification data for the selected ballots after sampling
         Call SamplerRepository to get modified data
         Export data to round_1.csv file again
        """
        csvPath = current_app.config.get('PROJECT_DIR') + '/app/data/sampler_{}/rounds/round_1.csv'.format(jobId)  # Export the modified data by user
        result = SamplerRepository().exportSampler(jobId)
        with open(csvPath, 'w') as file:
            file.write(result)
