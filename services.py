from contants import JobType, JobStatus
from models.job import Job, ScheduledJob, EventJob, JobLog
from werkzeug.exceptions import BadRequest
from datetime import datetime
from database import db_session
from task import TaskScheduler

def create_job(request_json):
    if 'type' in request_json and request_json['type'] == JobType.SCHEDULED_JOB.name:
        job = ScheduledJob(**request_json)
        cronlist = request_json.get("scheduler", "").split(" ")
        TaskScheduler.add_cron_task(job.id, job.params, minute=cronlist[0],
                                    hour=cronlist[1],
                                    day_of_week=cronlist[2],
                                    day_of_month=cronlist[3],
                                    month_of_year=cronlist[4])
    elif 'type' in request_json and request_json['type'] == JobType.EVENT_JOB.name:
        job = EventJob(**request_json)
    else:
        raise BadRequest(description="Invalid Job Type")
    job.save()
    return job

def edit_job(job_id, data):
    job = get_job_by_id(job_id)
    for key, val in data.items():
        setattr(job, key, val)
    job.save()
    return job

def get_jobs():
    return EventJob.query.all() + ScheduledJob.query.all()

def get_job_by_id(job_id):
    return ScheduledJob.query.filter(ScheduledJob.id == job_id).first() or EventJob.query.filter(EventJob.id == job_id).first()

def get_job_logs():
    return JobLog.query.all()

def trigger_event_job(request_json):
    event_name = request_json.get("event_name", None)
    if event_name:
        job = EventJob.query.filter(EventJob.event_name == event_name).first()
        job_log = JobLog(job_id=job.id, status=JobStatus.RUNNING.name, timestamp=datetime.utcnow())
        job_log.save()
        # Push the task to run asynchronously. Status will be updated inside run_task
        TaskScheduler.invoke_celery_task(job_log.id, job.params)
        return job_log

