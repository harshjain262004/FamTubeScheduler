import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import time

app = Flask(__name__)
app.secret_key = "Youtube API project"

def my_script():
    print("script at work on", time.time())

scheduler = BackgroundScheduler()
scheduler.add_job(my_script, 'interval', seconds=10)
scheduler.start()

@app.route('/', methods=['GET','POST'])
def homepage():
    return "Youtube API project"


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)