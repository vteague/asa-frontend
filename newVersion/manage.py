# -*- coding=utf-8 -*-
import os

from app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand   # load migrate

# set mysqlbd
import pymysql
pymysql.install_as_MySQLdb()

# set for the config, default for development
app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)  # registe migrate to flask

manager.add_command('db', MigrateCommand)   # use db for shell environment

if __name__ == '__main__':
    manager.run()