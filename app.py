from flask import Flask, render_template, request
from flask import json
from flask import jsonify
from contants import JobType
from services import *

from database import db_session

app = Flask(__name__)

@app.route('/create')
def create():
    return render_template("create.html", JobType=JobType)

@app.route('/manage')
def manage():
    return render_template("manage.html")

@app.route('/job', methods=['POST'])
def add_job():
    job = create_job(request.json)
    return jsonify(job=job.to_dict())

@app.route('/job/<job_id>', methods=['PUT'])
def put_job(job_id):
    job = edit_job(job_id, request.json)
    return jsonify(job=job.to_dict())

@app.route('/job', methods=['GET'])
def job_index():
    jobs = [job.to_dict() for job in get_jobs()]
    return jsonify(jobs=jobs)

@app.route('/job/<job_id>', methods=['GET'])
def get_job(job_id):
    job = get_job_by_id(job_id)
    return jsonify(job=job.to_dict())

@app.route('/job/<job_id>/edit', methods=['GET'])
def edit(job_id):
    job = get_job_by_id(job_id)
    return render_template("create.html", JobType=JobType, is_edit=True, job=job)

@app.route('/job/log', methods=['GET'])
def job_log_index():
    job_logs = [job_log.to_dict() for job_log in get_job_logs()]
    return jsonify(logs=job_logs)

@app.route('/job/log/latest', methods=['GET'])
def get_latest_job_logs():
    job_logs = [job_log.to_dict() for job_log in JobLog.get_latest_job_logs()]
    return jsonify(logs=job_logs)

@app.route('/event', methods=['POST'])
def trigger_job():
    job_log = trigger_event_job(request.json)
    return jsonify(jobLog=job_log.to_dict())

if __name__ == '__main__':
    from database import init_db
    init_db()
    app.run()


