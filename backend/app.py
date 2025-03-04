from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import time
from youtube import *
from Db import *

app = Flask(__name__)
app.secret_key = "Youtube API project"

scheduler = BackgroundScheduler()
scheduler.add_job(YoutubeAPIScript, 'interval', minutes=1)
scheduler.start()

@app.route('/', methods=['GET','POST'])
def homepage():
    return "Youtube API project"

@app.route('/api', methods=['GET'])
def api():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        query = request.args.get("query",None)
        if page < 1 or limit < 1:
            return jsonify({"error": "Invalid page or limit"}), 400
        if query:
            videos = fetchVideosQuery(page, limit, query)
            return jsonify({"page": page, "limit": limit, "videos": videos})
        videos = fetchVideos(page, limit)
        return jsonify({"page": page, "limit": limit, "videos": videos})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)