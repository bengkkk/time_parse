import json
import os

import recognizers_suite as Recognizers
from flask import Flask
from flask import request
from recognizers_suite import Culture

PORT = os.getenv("PORT")

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/v1/upload_time", methods=['POST'])
def run_job():
    upload_time = request.form.get("upload_time")
    if not upload_time:
        return {
            "code": 400,
            "msg": "upload_time not found."
        }
    upload_time = Recognizers.recognize_datetime(upload_time, Culture.Chinese)
    upload_time = upload_time[0].__dict__['resolution']['values'][0]['timex']
    return {
        "code": 200,
        "msg": upload_time
    }


@app.route("/api/v1/upload_times", methods=['POST'])
def upload_times():
    upload_times = request.form.get("upload_times")
    if not upload_times:
        return {
            "code": 400,
            "msg": "upload_times not found."
        }
    upload_times = json.loads(upload_times)['upload_times']
    results = {}
    for upload_time in upload_times:
        upload_time_1 = Recognizers.recognize_datetime(upload_time, Culture.Chinese)
        upload_time_1 = upload_time_1[0].__dict__['resolution']['values'][0]['timex']
        results[upload_time] = upload_time_1
    return {
        "code": 200,
        "msg": results
    }


if __name__ == '__main__':
    app.run("0.0.0.0", PORT)
