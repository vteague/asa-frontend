import tablib
from numpy import genfromtxt

from app.models.sampler.Sampler import Sampler
from app.modules.RepositoryBase import RepositoryBase


class SamplerRepository(RepositoryBase):
    def targetModelClass(self):
        return Sampler

    def model(self):
        return Sampler()

    def importSampler(self, filename, jobId):
        """
        importing the data of sampling
        """
        return self.model().importSampler(filename, jobId)

    def exportSampler(self, jobId):
        """
        exporting the sampling data after the alternation complete
        using the tablib to import the data
        getting the Header of the table
        traversing the data in the database to get the required data for creating CSV
        :return: CSV DATA
        """
        data = self.model().getById(jobId)
        if data is None:
            raise BaseException('Job import data does not exist')
        result = tablib.Dataset(headers=['ElectorateNm', 'VoteCollectionPointNm', 'VoteCollectionPointId', 'BatchNo', 'PaperNo', 'Preferences'])
        for item in data:
            datasetItem = [item.electorate_nm, item.vote_collection_point_nm, item.vote_collection_point_id,
                           item.batch_no, item.paper_no, ",,,," if item.preferences_after_audit is None else item.preferences_after_audit]
            result.append(datasetItem)
        return result.csv