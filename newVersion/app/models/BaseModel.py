from abc import ABCMeta
from six import add_metaclass
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declared_attr

from app import db


class BaseModel(db.Model):
    """
    Base class for Model，supporting basic manipulation for Model
    """
    __abstract__ = True

    """
    逻辑主键Key
    """
    primaryKey = 'id'

    @declared_attr
    def __tablename__(self):
        return self.__name__

    def getPrimaryKey(self):
        return self.primaryKey

    def get(self, id):
        """
        Returning data according to ID
        Args:
            id: Primary Key

        Returns:
            Return an object for Model and if there is no result, return Null

        """
        kwargs = [{self.primaryKey == id}]
        return self.query.filter(*kwargs).first()

    def create(self, model):
        """
        creating data
        :param model:
        :return:
        """
        db.session.add(model)
        self.session_commit()
        return model

    def update(self):
        """
        updating data
        :return:
        """
        return self.session_commit()

    def delete(self, id):
        """
        deleting data according to Primary Key
        :param id: Primary Key
        :return: the row number that needs to be deleted
        """
        deleteRow = self.query.filter_by(dict({self.primaryKey: id})).delete()
        self.session_commit()
        return deleteRow

    def paginate(self, page, per_page=10, *kwargs):
        """
        paginating the filtered records according to the conditions
        the default setting is using the descending order according to the primary key
        :param page: page number
        :param per_page: record size for each page
        :param kwargs: filtering conditions
        :return: Pagination object
        """
        return self.query.filter(*kwargs).order_by(desc(self.primaryKey)).paginate(page, per_page, error_out=False)

    def getAll(self, *kwargs):
        """
        Using conditions to search for match data without paginating
        the default setting is using the descending order according to the primary key
        :param kwargs: filtering conditions
        :return: all rows.
        """
        return self.filter(*kwargs).order_by(desc(self.primaryKey)).query.all()

    @staticmethod
    def session_commit():
        """
        the manipulation commit for model
        In Flask-SQLAlchemy, the manipulation of db towards the database have to be committed before having efforts
        """
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            reason = str(e)
            return reason
