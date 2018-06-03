import sys
from flask import render_template, request
from lib.Helper import responseJson


class BaseException(Exception):
    """
    The base class for handling exception for monitoring the whole project
    """
    def __init__(self, message):
        super(BaseException, self).__init__(self) #transfer object of class BaseException to an object of class
        self.message = message
        sys.excepthook = self.handle()

    def handle(self):
        if request.headers.environ['HTTP_X_REQUESTED_WITH'].lower() != "xmlhttprequest":
            return render_template('error.html', message=self.message)
        else:
            return responseJson(False, message=self.message)
