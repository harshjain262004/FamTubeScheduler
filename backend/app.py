from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from youtube import *
from Db import *
from flask_cors import CORS

# Initializing the Backend app, CORS, and BackgroundScheduler

app = Flask(__name__)
CORS(app)
app.secret_key = "Youtube API project"

# BackgroundScheduler to run the YoutubeAPIScript every minute
scheduler = BackgroundScheduler()
scheduler.add_job(YoutubeAPIScript, 'interval', minutes=1)
scheduler.start()

@app.route('/', methods=['GET','POST'])
def homepage():
    return "Famtube Scheduler"

# Main Requirement API endpoint to be able to fetch videos from the database
# The API endpoint should be able to take the following parameters: page, limit, sort
# The API should return the videos in the order of their published date asc, dec based on sort value
# Modular to fetch videos for any search query (Commented out, since only 1 query "cricket" in db)
@app.route('/api/getVideos', methods=['GET'])
def api():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        # query = request.args.get("query",None) only needed when multiple yt queries are there, currently only 1
        sort = request.args.get("sort","desc")
        if sort not in ["asc", "desc"]:
            return jsonify({"error": "Invalid sort value}"}), 400
        if page < 1 or limit < 1:
            return jsonify({"error": "Invalid page or limit"}), 400
        if sort == "desc":
            videos = fetchVideos(page, limit)
            return jsonify({"page": page, "limit": limit, "videos": videos})
        else:
            videos = fetchVideosAsc(page, limit)
            return jsonify({"page": page, "limit": limit, "videos": videos})
        # if query:
        #     videos = fetchVideosQuery(page, limit, query)
        #     return jsonify({"page": page, "limit": limit, "videos": videos})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# The API should return the total number of videos in the database
@app.route('/api/getTotalVideo', methods=['GET'])
def totalVideos():
    try:
        total = getTotalVideos()
        return jsonify({"total": total})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)