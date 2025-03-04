import os
import googleapiclient.discovery 
from datetime import datetime, timedelta,timezone
from dotenv import load_dotenv
load_dotenv()
from Db import getQueries, AddVideos

api_service_name = "youtube"
api_version='v3'
developer_key = os.environ["YOUTUBE_API_KEY_1"]
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=developer_key)


# for now cricket is hardcoded, we can make it dynamic by fetching queries from db
def YoutubeAPIScript():
    queries = getQueries()
    if len(queries) == 0:
        print("No queries present in the database")
        return "No queries present in the database"
    queries = [query[0] for query in queries]
    for query in queries:
        published_after = (datetime.now(timezone.utc) - timedelta(minutes=10)).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
        request = youtube.search().list(
            q="Cricket",
            part="snippet",
            maxResults=50,
            type="video",
            publishedAfter=published_after,
            order="date"
        )
        response = request.execute()
        AddVideos(response,query)
    print("Script Completion")
    return "Script Completion"

