from app.models.BaseModel import BaseModel
from app import db


class User(BaseModel):
    """
    用户类，对应数据表tbl_user
    逻辑主键:user_id
    """
    __tablename__ = 'tbl_user'
    primaryKey = 'user_id'

    user_id = db.Column(db.BIGINT, primary_key=True)
    user_name = db.Column(db.String(200))
    user_username = db.Column(db.String(200))
    user_password = db.Column(db.String(200))

    def __init__(self, user_name=None, user_username=None, user_password=None):
        self.user_name = user_name
        self.user_username = user_username
        self.user_password = user_password

    def getByName(self, username):
        """
        根据账号查询用户
        :param username: 账号
        :return: User
        """
        return self.query.filter(User.user_name == username).first()
