import json

from flask import render_template, session, redirect, url_for, request
import os
from app.modules.repositorys.UserRepository import UserRepository
from app.script import script
from lib.Helper import responseJson


@script.route('/', methods=['GET'])
@script.route('/login', methods=['GET'])
def index():
    return render_template('login.html')


@script.route('/login', methods=['POST'])
def login():
    """
    login
    """
    username = request.form.get('username')
    password = request.form.get('password')
    repository = UserRepository().verification(username, password)
    if repository:
        script.secret_key = os.urandom(24)
        session['username'] = username
        session.permanent = True  # Prevent browser from closing the session
        return redirect('/sampler')
    else:
        message = "Login failed."
        return render_template('login.html', message=message, username=username, password=password)


@script.route('register', methods=['POST'])
def register():
    """
    register
    """
    data = json.loads(request.get_data())
    if data['username'] == "":
        raise BaseException("Account cannot be empty")
    if data['password'] is None:
        raise BaseException("Password cannot be empty")
    result = UserRepository().registered(data['username'], data['password'])
    if result is not None:
        return responseJson(True, None)
    raise BaseException('registration failed')


@script.route('/logout')
def logout():
    """
    Logout
    """
    session.pop('username', None)
    return redirect(url_for('script.login'))


@script.before_request
def verificationLogin():
    if 'username' in session:
        pass
    else:
        if request.url_rule.rule != '/login' and request.url_rule.rule != '/register':
            return redirect(url_for('script.login'))
