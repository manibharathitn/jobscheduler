from celery.schedules import crontab
from celery import Celery
from models.job import JobLog
from contants import JobStatus
import random
from datetime import datetime


celery = Celery("jobscheduler", broker='amqp://guest@localhost:5672//')

class TaskScheduler():

    @classmethod
    def _run(cls, job_log_id, params):
        """
        :param job_id:
        :param params:
        :return:

        It is assumed that this method runs the task with the given job params and gets the result
        """
        result = random.choice([JobStatus.SUCCESS.name, JobStatus.FAILED.name])
        job_log = JobLog.query.filter(JobLog.id == job_log_id).first()
        job_log.status = result
        job_log.save()

    @classmethod
    def invoke_celery_task(cls, job_log_id, params):
        @celery.task()
        def run_task(job_log_id, params):
            cls._run(job_log_id, params)

        run_task.apply_async(args=(job_log_id, params))

    @staticmethod
    def add_cron_task(job_log_id, params, **cronlist):
        """
        :param cronlist: minute=mins, hour=hour, day_of_week=dow, day_of_month=dom, month_of_year=moy
        :return:
        """
        pass