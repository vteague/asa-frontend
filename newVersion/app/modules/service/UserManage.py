from flask import session

from app.modules.repositorys.UserRepository import UserRepository


class UserManage:
    @staticmethod
    def getCurrent():
        """
        Get the current logged in user
        :return: User
        """
        username = session.get('username')
        if username is None:
            raise BaseException('Failed to get user status.')
        user = UserRepository().getByName(username)
        if user is None:
            raise BaseException('Failed to get user data.')
        return user
