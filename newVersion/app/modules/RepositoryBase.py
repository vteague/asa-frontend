from sqlalchemy import select, and_, desc

from app.script import script
from app.models.BaseModel import BaseModel
import six
import abc


@six.add_metaclass(abc.ABCMeta)
class RepositoryBase:
    """
     base class for repository
     Provides basic database operation for model
     In order to avoid the downward dependencies in the repository base class, all the model classes used here are the abstract base class of Model.
     Subclasses explain the current operation of specific classes and entities to the base class by reconstructing the targetModelClass() and model() methods
    """
    @abc.abstractmethod
    def targetModelClass(self):
        """
        Returns the current Model type
        :return: BaseModel
        """
        return BaseModel

    def findById(self, id):
        """
        Use the primary key to filter data
        :return: List<BaseModel>
        """
        return self.model().get(id)

    def getAll(self):
        """
        Return all data
        """
        return self.model().getAll()

    def getList(self, page=1, conditions={}, pageSize=10):
        """
        Use Pagination for query
        :param page: page number
        :param conditions: conditions for query
        :param pageSize: Page size
        """
        ands = self.validateAndGetListConditions(conditions)
        return self.model().paginate(page, pageSize, *ands)

    def create(self, model):
        """
        Create a new data
        :param model: BaseModel
        :return: BaseModel
        """
        return self.model().create(model)

    def update(self, model):
        """
        Update
        It is not the same as other operation such as adding as the update need to be executed with its own instance for Model.
        :param model: BaseModel
        """
        return model.update()

    def validateAndGetListConditions(self, conditions={}):
        """
        Set query conditions
        gathering the received query conditions and it use "and" as a query (where) gathering condition
        :param conditions: Query conditions
        :return: List
        """
        ands = []
        for key, value in conditions.items():
            ands.append(and_(getattr(self.targetModelClass(),
                                     key) == value))  # Use getattr method to dynamically obtain the current Model property as well as value to form a query condition. There may have multiple conditions and therefore, using and_ to connect with each other.
        return ands

    def model(self):
        """
        Return the Model entity for current operation
        """
        return BaseModel()
