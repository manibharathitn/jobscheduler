from flask import Flask, render_template, request
from flask import json
from contants import JobType
from services import *
app = Flask(__name__)

@app.route('/create')
def create():
    return render_template("create.html", JobType=JobType)

@app.route('/job', methods=['POST'])
def add_job():
    job = create_job(request.json)
    return json.dump(job)

@app.route('/job', methods=['GET'])
def job_index():
    return get_jobs()

@app.route('/job/log', methods=['GET'])
def job_log_index():
    return get_job_logs()

if __name__ == '__main__':
    # from database import init_db
    # init_db()
    app.run()


