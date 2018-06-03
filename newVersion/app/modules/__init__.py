from flask import Flask
from .repositorys import UserRepository, JobRepository

modules = Flask(__name__)
