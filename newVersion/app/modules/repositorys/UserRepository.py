from werkzeug.security import check_password_hash, generate_password_hash

from ..RepositoryBase import RepositoryBase
from app.models.user.User import User
from app.exceptions.BaseException import BaseException


class UserRepository(RepositoryBase):
    def model(self):
        return User()

    def targetModelClass(self):
        return User

    def verification(self, username, password):
        """
        login verification
        """
        model = User.query.filter(User.user_name == username).first()
        if model is None:
            return False
        return check_password_hash(model.user_password, password)

    def registered(self, username, password):
        user = User().getByName(username)
        if user is not None:
            raise BaseException('Username already exists')
        model = User(username, None, generate_password_hash(password))
        return model.create(model)

    def getByName(self, username):
        """
        getting the account details according to the username
        """
        model = User().getByName(username)
        return model