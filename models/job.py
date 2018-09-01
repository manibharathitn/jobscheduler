from database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database import db_session
from contants import JobType

class BaseModel:
    def save(self):
        try:
            if not self.id:
                db_session.add(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise
        finally:
            # db_session.close()
            pass

    def to_dict(self):
        result_dict = {}
        for key,value in vars(self).items():
            if str(key) and "_" != str(key)[0] and key != 'job':
                if type(value) is datetime:
                    value = str(value)
                result_dict[key] = value
        return result_dict

class Job(BaseModel, Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    type = Column(String(80))
    priority = Column(Integer)
    params = Column(String(25))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'job'
    }


class ScheduledJob(Job):
    scheduler = Column(String(25))
    __mapper_args__ = {
        'polymorphic_identity': JobType.SCHEDULED_JOB.name
    }


class EventJob(Job):
    event_name = Column(String(25))
    __mapper_args__ = {
        'polymorphic_identity': JobType.EVENT_JOB.name
    }

class JobLog(BaseModel, Base):
    __tablename__ = 'joblog'
    job_id = Column(Integer, ForeignKey('job.id'), nullable=False)
    id = Column(Integer, primary_key=True)
    status = Column(String(10))
    timestamp = Column(DateTime, default=datetime.utcnow)
    job = relationship('Job')

    @classmethod
    def get_latest_job_logs(cls):
        subqry = db_session.query(func.max(JobLog.timestamp)).group_by(JobLog.job_id)
        qry = JobLog.query.filter(JobLog.timestamp.in_(subqry))
        return qry.all()




