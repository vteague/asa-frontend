from app.models.BaseModel import BaseModel
from app import db


class Job(BaseModel):
    """
    The basic table manipulation for job
    Name of Table：output_data
    Primary key：job_id
    """
    __tablename__ = 'output_data'  # provide the name for table
    primaryKey = 'job_id'

    job_id = db.Column(db.BIGINT, primary_key=True)
    user_id = db.Column(db.BIGINT)
    job_name = db.Column(db.String(200))
    job_type = db.Column(db.String(200))
    state = db.Column(db.String(200))
    seed = db.Column(db.String(200))
    status = db.Column(db.String(200))
    increment = db.Column(db.String(200))
    rounds = db.Column(db.String(200))
    ballots = db.Column(db.String(200))
    job_data = db.Column(db.String(200))

    def __init__(self, user_id=None, job_name=None, job_type=None, state=None, seed=None, status=None, increment=None,
                 rounds=None, ballots=None, job_data=None):
        self.user_id = user_id
        self.job_name = job_name
        self.job_type = job_type
        self.state = state
        self.seed = seed
        self.status = status
        self.increment = increment
        self.rounds = rounds
        self.ballots = ballots
        self.job_data = job_data

    def get(self, id):
        return Job.query.filter(Job.job_id == id).first()
