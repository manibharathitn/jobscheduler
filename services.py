from contants import JobType
from models.job import Job, ScheduledJob, EventJob, JobLog
from werkzeug.exceptions import BadRequest

def create_job(request_json):
    if 'type' in request_json and request_json['type'] == JobType.SCHEDULED_JOB.name:
        job = ScheduledJob(**request_json)
        # TODO: Add a celery scheduler
    elif 'type' in request_json and request_json['type'] == JobType.EVENT_JOB.name:
        job = EventJob(**request_json)
    else:
        raise BadRequest(description="Invalid Job Type")
    job.save()
    return job

def get_jobs():
    return Job.query.all()

def get_job_logs():
    return JobLog.query.all()